'''
Download specified attachments into the attachments/ directory and return
space-delimited list of attachment filenames.
'''
import json
import os
import sys

import scrapelib


s = scrapelib.Scraper(retry_attempts=1)
filenames = []

for attachment_link in json.loads(
    os.environ['attachment_links'].replace('\'', '"')
):
    attachment = s.get(attachment_link)

    if 'https://metro.legistar.com/ViewReport.ashx' in attachment_link:
        filename = 'root.pdf'
    else:
        filename = os.path.basename(attachment_link)
    with open(os.path.join('attachments', filename), 'wb') as file:
        file.write(attachment.content)

    filenames.append(os.path.join('attachments', filename))

sys.stdout.write(' '.join(filenames))
