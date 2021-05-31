import os
import shutil
from pdf2image import convert_from_path
from utils import Config
from pdf2image.exceptions import PDFPageCountError

# make sure imagemagick is installed
if not shutil.which('convert'): # shutil.which needs Python 3.3+
  print("ERROR: you don\'t have imagemagick installed. Install it first before calling this script")
  sys.exit()

# create necessary directories
pdf_dir = os.path.join('data', 'pdf')
if not os.path.exists(Config.thumbs_dir): os.makedirs(Config.thumbs_dir)
if not os.path.exists(Config.tmp_dir): os.makedirs(Config.tmp_dir)

# fetch all pdf filenames in the pdf directory
files_in_pdf_dir = os.listdir(pdf_dir)
pdf_files = [x for x in files_in_pdf_dir if x.endswith('.pdf')] # filter to just pdfs, just in case

# iterate over all pdf files and create the thumbnails
for i,p in enumerate(pdf_files):
  pdf_path = os.path.join(pdf_dir, p)
  thumb_path = os.path.join(Config.thumbs_dir, p + '.jpeg')

  if os.path.isfile(thumb_path): 
    print("skipping %s, thumbnail already exists." % (pdf_path, ))
    continue

  print("%d/%d processing %s" % (i, len(pdf_files), p))

  try:
      images = convert_from_path(pdf_path, dpi=200, last_page=4, fmt="jpeg", output_file="thumbs", output_folder=os.path.join(Config.tmp_dir), size=(None, 312))
      tmp_thumb = os.path.join(Config.tmp_dir, '*.jpg')
      cmd = "montage -mode concatenate -quality 80 -tile x1 %s %s" % (tmp_thumb, thumb_path)
      # print(cmd)
      os.system(cmd)
      cmd_remove = "rm %s" % (tmp_thumb)
      os.system(cmd_remove)

  except PDFPageCountError:
      missing_thumb_path = os.path.join('static', 'missing.jpg')
      os.system('cp %s %s' % (missing_thumb_path, thumb_path))
      print('missing')
