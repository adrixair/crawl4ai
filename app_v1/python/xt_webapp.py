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
  <h3>Mots-clés :</h3>
  <div id="fields">
    {% for q in queries_list %}
      <input type="text" name="queries" style="width:300px; margin-bottom:4px;" value="{{ q }}">
    {% endfor %}
  </div>
  <button type="button" onclick="addField()">Ajouter un mot-clé</button>
  <input type="submit" value="Lancer">
</form>
{% if output %}
<h2>Terminal Output</h2>
<textarea rows="20" cols="80" readonly style="width:100%;">{{ output }}</textarea>
{% endif %}
<script>
function addField() {
  var div = document.getElementById('fields');
  var input = document.createElement('input');
  input.type = 'text';
  input.name = 'queries';
  input.style.width = '300px';
  input.style.marginBottom = '4px';
  div.appendChild(input);
}
</script>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    queries_list = []
    if request.method == 'GET':
        queries_list = DEFAULT_QUERY_LIST
    output = ''
    if request.method == 'POST':
        queries_list = request.form.getlist('queries')
        query_list = [q.strip() for q in queries_list if q.strip()]
        if not query_list:
            query_list = DEFAULT_QUERY_LIST
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            urls = get_unique_urls(query_list)
            asyncio.run(run_batch(urls))
        output = buf.getvalue()
    return render_template_string(HTML_TEMPLATE, output=output, queries_list=queries_list)

if __name__ == '__main__':
    app.run(debug=True)
