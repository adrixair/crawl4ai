from google import genai

# Configure la clé API
genai.Client(api_key="AIzaSyDqNHrjuRSFDyqym52Q29cChjnzHAAGsk0")

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${AIzaSyDqNHrjuRSFDyqym52Q29cChjnzHAAGsk0}" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Write a story about a magic backpack."
          }
        ]
      }
    ]
  }'