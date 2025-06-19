from flask import Flask, request, render_template_string
from io import StringIO
import contextlib
import asyncio

from xt import get_unique_urls, run_batch, DEFAULT_QUERY_LIST, run_xt

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Google Search Crawler</title>
<h1>Google Search Crawler</h1>
<form method="post">
  Query list (comma separated):<br>
  <input type="text" name="queries" style="width:400px" value="{{ queries | default('') }}">
  <input type="submit" value="Run">
</form>
{% if output %}
<h2>Output</h2>
<pre>{{ output }}</pre>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    queries = ''
    if request.method == 'POST':
        queries = request.form.get('queries', '')
        query_list = [q.strip() for q in queries.split(',') if q.strip()]
        if not query_list:
            query_list = DEFAULT_QUERY_LIST
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            urls = get_unique_urls(query_list)
            asyncio.run(run_batch(urls))
        output = buf.getvalue()
    return render_template_string(HTML_TEMPLATE, output=output, queries=queries)

if __name__ == '__main__':
    app.run(debug=True)
