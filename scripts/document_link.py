import os
import re
from urllib.parse import urlparse, parse_qs

import scrapelib


def Link(url):
    if url.startswith('https://metro.legistar.com/ViewReport.ashx'):
        return BoardReportLink(url)

    return DocumentLink(url)


class DocumentLink(object):
    '''
    https://metro.legistar1.com/metro/meetings/2021/10/2100_A_Operations%2C_Safety%2C_and_Customer_Experience_Committee_21-10-21_Agenda.pdf
    http://metro.legistar1.com/metro/attachments/6484cdc7-3c2a-4598-abc5-9d846771158e.pdf
    '''
    def __init__(self, url):
        self.url = url

    @property
    def content(self):
        s = scrapelib.Scraper(retry_attempts=2)
        response = s.get(self.url)
        return response.content

    @property
    def filename(self):
        '''
        Return the filename from the URL, less any percent signs from escaped
        characters (commas, spaces, etc.), as these will confuse Make.
        '''
        return re.sub(r'%', '', os.path.basename(self.url))


class BoardReportLink(DocumentLink):
    '''
    https://metro.legistar.com/ViewReport.ashx?M=R&N=TextL5&GID=557&ID=7936&GUID=LATEST&Title=Board+Report
    '''
    @property
    def filename(self):
        '''
        Parse the report ID out of the URL and use it to create a unique
        filename.
        '''
        board_report_id, = parse_qs(
            urlparse(self.url).query
        )['ID']

        return f'board_report_{board_report_id}.pdf'
