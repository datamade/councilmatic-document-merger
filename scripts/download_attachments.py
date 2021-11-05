'''
Download specified attachments into the attachments/ directory and return
space-delimited list of attachment filenames.
'''
import json
import os
import sys

from document_link import Link


if __name__ == '__main__':
    ACCEPTED_FILETYPES = (
        '.pdf',
        '.xlsx',
        '.doc',
        '.docx',
        '.ppt',
        '.pptx',
        '.rtf',
    )

    filenames = []

    for attachment_link in json.loads(
        os.environ['attachment_links'].replace('\'', '"')
    ):
        link = Link(attachment_link)

        if link.filetype not in ACCEPTED_FILETYPES:
            continue

        with open(os.path.join('attachments', link.filename), 'wb') as file:
            file.write(link.content)

        filenames.append(os.path.join('attachments', link.filename))

    sys.stdout.write(' '.join(filenames))
