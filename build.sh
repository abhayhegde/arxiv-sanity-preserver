#!/bin/bash
python -m venv env/
source env/bin/activate
pip install -r requirements.txt
sqlite3 as.db < schema.sql
python fetch_papers.py
python download_pdfs.py
python parse_pdf_to_text.py
python pdf_thumbs.py
python analyze.py
python buildsvm.py
python make_cache.py
sudo service mongod start
python serve.py --prod --port 80
