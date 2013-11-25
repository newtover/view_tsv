#!/usr/bin/env python

"""
Module contain only the TSVHandler class, which is a customized SimpleHTTPRequestHandler
that provides additional rendering for tsv files as HTML table.

The module can be run in the same way as SimpleHTTPServer with the additional PORT parameter.
"""

from cStringIO import StringIO
import json
import SimpleHTTPServer as _server

__version_info__ = (0, 1, 1)
__version__ = '.'.join(map(str, __version_info__))


tsv_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style type="text/css">
table {{border-collapse: collapse;}}
tr {{border: 1px solid #999; border-width: 0 0 1px 0;padding:2px;}}
td {{border-right: 1px solid #999; padding: 2px 4px;}}
tr:first-child td, td:first-child {{background-color:#ccc;font-weight:bold;text-align:center;}}
td:nth-child(2) {{max-width:60em;overflow-y:auto;}}
</style>
<script type="text/javascript">
var file_data = {json};
console.log(file_data);

function fillTable(){{
  var table = document.getElementById('data-table');
  var num_cols = file_data.max_col_count;
  var num_rows = file_data.rows.length;
  var h_row = table.insertRow(-1);
  for (var j = 0; j < num_cols + 1; j++) {{
      var cell = h_row.insertCell(-1);
      cell.innerText = String.fromCharCode(64+j);
  }}

  for (var i = 0; i < num_rows; i++) {{
      var h_row = table.insertRow(-1);
      var cell = h_row.insertCell(-1);
      cell.innerText = (i+1);
      var data_row = file_data.rows[i];
      for (var j = 0; j < num_cols; j ++) {{
          cell = h_row.insertCell(-1);
          cell.innerText = data_row[j];
      }}
  }}
}}

window.addEventListener("load", fillTable);
</script>
</head>
<body>
<table id="data-table">
</table>
<pre>{tsv}</pre>
</body>
</html>
"""

def escape_js_output(_str):
    """Escape < and & for safe rendering in HTML."""
    return _str.replace('<', '\u003c').replace('&', '\u0026')


class TSVHandler(_server.SimpleHTTPRequestHandler):
    """Handler for BaseHTTPServer.HTTPServer that provides alternative rendering for .tsv files as HTML table."""

    def __init__(self, request, client_address, server):
        _server.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
        # for default view when file encoding is not utf-8
        self.extensions_map['.tsv'] = 'text/plain'


    @property
    def file_encoding(self):
        """Used to decode tsv files."""
        # can be taken from cgi-params
        return 'utf-8'


    def _render_table(self, rows, encoding):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        max_col_count = max(len(cols) for cols in rows)
        file_data = {'max_col_count': max_col_count,
                     'encoding': encoding,
                     'rows': rows}
        html = tsv_html.format(tsv='',
                               json=escape_js_output(json.dumps(file_data)))
        out_file = StringIO()
        out_file.write(html)
        out_file.seek(0)
        return out_file


    def send_head(self):
        path = self.translate_path(self.path)
        if path.endswith('.tsv'):
            try:
                with open(path, 'rb') as orig_file:
                    encoding = self.file_encoding
                    tsv_contents = unicode(orig_file.read(), encoding)
                    rows = [line.split('\t') for line in tsv_contents.splitlines()]
                return self._render_table(rows, encoding)
            except UnicodeDecodeError:
                # default behaviour
                pass
        return _server.SimpleHTTPRequestHandler.send_head(self)



if __name__ == '__main__':
    _server.test(HandlerClass=TSVHandler)
