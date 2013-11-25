view_tsv
========

Handler for BaseHTTPServer.HTTPServer that provides alternative rendering for .tsv files as HTML table.

Why did I even need it?

I work a lot with tab-separated files which contain search queries or sentences to translate in the first column and various meta-info in other columns. This results in files which are not easy viewable at the command line, or simple text editors. I could open the files in an Excel-like application, but (at least) Excel sometimes interprets the cell contents as it wants, so I decided to write something myself.

Put the view_tsv.py somewhere in site-packages (I usually use a .pth file for the small scripts like this, but I should better add a setup script), go to the directory where you have a .tsv file, and just run it as:

  $ python -m view_tsv 8000
  
Then open your browser at http://localhost:8000, browse to the .tsv file and enjoy the tabular view.
