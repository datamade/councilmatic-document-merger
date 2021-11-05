import os
import sys

import convertapi


_, infile = sys.argv
filename, _ = os.path.splitext(os.path.basename(infile))
outfile = os.path.join('attachments', f'{filename}.pdf')

convertapi.api_secret = 'Wooc5YgefMq2dbce'
convertapi.convert('pdf', {'File': infile}, from_format = 'xps')\
          .save_files(outfile)
