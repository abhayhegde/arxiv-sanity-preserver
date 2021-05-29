#!/bin/bash
sudo apt-get install python3.8
sudo apt-get install imagemagick poppler-utils
pip install -r requirements.txt
python fetch_papers.py
python download_pdfs.py
python parse_pdf_to_text.py
python thumb_pdf.py
python analyze.py
python buildsvm.py
python make_cache.py
