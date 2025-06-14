# Make sure to install the required packageschainlit and groq
import os, time
from openai import AsyncOpenAI
import chainlit as cl
from chainlit.types import InputAudioChunk
import re
import requests
from io import BytesIO
from groq import Groq

# Import threadpools to run the crawl_url function in a separate thread
from concurrent.futures import ThreadPoolExecutor

api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing API key. Please set GROQ_API_KEY or OPENAI_API_KEY as an environment variable.")

client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

# Instrument the OpenAI client
cl.instrument_openai()

settings = {
    "model": "llama3-8b-8192",
    "temperature": 0.5,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


def extract_urls(text):
    url_pattern = re.compile(r"(https?://\S+)")
    return url_pattern.findall(text)


def crawl_url(url):
    data = {
        "urls": [url],
        "include_raw_html": True,
        "word_count_threshold": 10,
        "extraction_strategy": "NoExtractionStrategy",
        "chunking_strategy": "RegexChunking",
    }
    response = requests.post("https://crawl4ai.com/crawl", json=data)
    response_data = response.json()
    response_data = response_data["results"][0]
    return response_data["markdown"]


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("session", {"history": [], "context": {}})
    await cl.Message(content="Welcome to the chat! How can I assist you today?").send()


@cl.on_message
async def on_message(message: cl.Message):
    user_session = cl.user_session.get("session")

    # Extract URLs from the user's message
    urls = extract_urls(message.content)

    futures = []
    with ThreadPoolExecutor() as executor:
        for url in urls:
            futures.append(executor.submit(crawl_url, url))

    results = [future.result() for future in futures]

    for url, result in zip(urls, results):
        ref_number = f"REF_{len(user_session['context']) + 1}"
        user_session["context"][ref_number] = {"url": url, "content": result}

    user_session["history"].append({"role": "user", "content": message.content})

    # Create a system message that includes the context
    context_messages = [
        f'<appendix ref="{ref}">\n{data["content"]}\n</appendix>'
        for ref, data in user_session["context"].items()
    ]
    if context_messages:
        system_message = {
            "role": "system",
            "content": (
                "You are a helpful bot. Use the following context for answering questions. "
                "Refer to the sources using the REF number in square brackets, e.g., [1], only if the source is given in the appendices below.\n\n"
                "If the question requires any information from the provided appendices or context, refer to the sources. "
                "If not, there is no need to add a references section. "
                "At the end of your response, provide a reference section listing the URLs and their REF numbers only if sources from the appendices were used.\n\n"
                "\n\n".join(context_messages)
            ),
        }
    else:
        system_message = {"role": "system", "content": "You are a helpful assistant."}

    msg = cl.Message(content="")
    await msg.send()

    # Get response from the LLM
    stream = await client.chat.completions.create(
        messages=[system_message, *user_session["history"]], stream=True, **settings
    )

    assistant_response = ""
    async for part in stream:
        if token := part.choices[0].delta.content:
            assistant_response += token
            await msg.stream_token(token)

    # Add assistant message to the history
    user_session["history"].append({"role": "assistant", "content": assistant_response})
    await msg.update()

    # Append the reference section to the assistant's response
    reference_section = "\n\nReferences:\n"
    for ref, data in user_session["context"].items():
        reference_section += f"[{ref.split('_')[1]}]: {data['url']}\n"

    msg.content += reference_section
    await msg.update()


@cl.on_audio_start
async def on_audio_start():
    # Initialize a fresh buffer for this audio session
    cl.user_session.set("audio_buffer", BytesIO())
    cl.user_session.set("audio_mime_type", None)
    return True


@cl.on_audio_chunk
async def on_audio_chunk(chunk: InputAudioChunk):
    buf = cl.user_session.get("audio_buffer")
    if chunk.isStart:
        # Set a filename so Whisper recognises the format
        buf.name = f"input_audio.{chunk.mimeType.split('/')[1]}"
        cl.user_session.set("audio_mime_type", chunk.mimeType)

    # Append the new data
    buf.write(chunk.data)


@cl.on_audio_end
async def on_audio_end():
    # Retrieve and reset buffer
    buffer: BytesIO = cl.user_session.get("audio_buffer")
    buffer.seek(0)
    audio_bytes = buffer.read()
    mime_type: str = cl.user_session.get("audio_mime_type") or "audio/wav"

    # Transcribe via Whisper through Groq
    resp = await client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=(buffer.name, audio_bytes, mime_type)
    )
    transcription = resp.text

    # Feed transcription back into the chat pipeline
    user_msg = cl.Message(author="You", content=transcription)
    await user_msg.send()
    await on_message(user_msg)


if __name__ == "__main__":
    from chainlit.cli import run_chainlit

    run_chainlit(__file__)