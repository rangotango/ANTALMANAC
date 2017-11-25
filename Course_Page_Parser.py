import urllib.request
import time
from html.parser import HTMLParser
from collections import OrderedDict
        
class SingleResultParser(HTMLParser):
    cap = 0
    enr = 0
    req = 0
    wl = 0
    code = ''
    in_row = False
    col = 0
    
    def my_reset(self):
        self.cap = 0
        self.enr = 0
        self.req = 0
        self.wl = 0
        self.code = ''
        self.in_row = False
        self.col = 0
        
    def set_code(self, c_code):
        self.code = c_code

    def handle_starttag(self, tag, attrs):
        if self.in_row and tag == 'td':
            self.col += 1
            
    def handle_endtag(self, tag):
        if tag == 'table':
            if not str(self.req).isnumeric() and self.req.strip() != 'n/a':
                self.req = self.wl
                self.wl = 'n/a'
            if '/' in str(self.enr):
                self.enr = int(self.enr[self.enr.find('/ ')+2:])

    def handle_data(self, data):
        if data == self.code:
            self.in_row = True
            self.col = 1
        if self.in_row:
            if self.col == 8:
                self.cap = data
            elif self.col == 9:
                self.enr = data
            elif self.col == 10:
                self.wl = data
            elif self.col == 11:
                self.req = data
                self.col = 0
                self.in_row = False
    
    def return_data(self):
        return OrderedDict([('m',str(self.cap)), ('e',str(self.enr)), ('r',str(self.req)), ('w',str(self.wl))])
    
    def fetch(self, code):
        self.set_code(code)
        base_url = 'https://www.reg.uci.edu/perl/WebSoc?'
        fields = [('YearTerm','2018-03'), ('CourseCodes',self.code)]
        raw_info = 0
        while True:
            try:
                raw_info = urllib.request.urlopen(base_url + urllib.parse.urlencode(fields))
                data = raw_info.read().decode()
                self.feed(data)
                break
            except:
                time.sleep(2)
        raw_info.close()
        return self.return_data()
                        
#if __name__ == '__main__':
#     raw_info = urllib.request.urlopen('https://www.reg.uci.edu/perl/WebSoc?YearTerm=2017-92&CourseCodes=38432')
#     raw_info = urllib.request.urlopen('https://www.reg.uci.edu/perl/WebSoc?YearTerm=2018-03&CourseCodes=34110')
 #   p = SingleResultParser()
#     p.set_code('36595')
  #  p.fetch('34110')
   # for i in p.return_data().values():
    #    print('thing: {}'.format(i))
