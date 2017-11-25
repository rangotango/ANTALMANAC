import urllib.request
import time
from collections import OrderedDict
from html.parser import HTMLParser
        
class SingleResultParser(HTMLParser):
    codes = []
    c_code = ''
    lim = 0
    index = 0
    result = OrderedDict()
    in_row = False
    col = 0
    
    def initialize(self, new_codes):
        if new_codes == []:
            return
        self.codes = sorted(new_codes)
        self.c_code = self.codes[0]
        self.lim = len(new_codes)
        self.index = 0
        self.result = OrderedDict()
        for code in self.codes:
            self.result[code]=['0','0','0','0']
        self.in_row = False
        self.col = 0
        
    def handle_starttag(self, tag, attrs):
        if self.in_row and tag == 'td':
            self.col += 1
            
    def handle_endtag(self, tag):
        if tag == 'table':
            for code, info in self.result.items():
                if not str(info[3]).isnumeric() and info[3].strip() != 'n/a':
                    self.result[code][3] = info[2]
                    self.result[code][2] = 'n/a'
                if '/' in str(info[1]):
                    self.result[code][1] = int(info[1][info[1].find('/ ')+2:])

    def handle_data(self, data):
        if data == self.c_code:
            self.in_row = True
            self.col = 1
        if self.in_row:
            if self.col == 8:
                self.result[self.c_code] = [data] #max
            elif self.col == 9:
                self.result[self.c_code].append(data) #enr
            elif self.col == 10:
                self.result[self.c_code].append(data) #wl
            elif self.col == 11:
                self.result[self.c_code].append(data) #req
                self.col = 0
                self.in_row = False
                self.index += 1
                if self.index != self.lim :
                    self.c_code = self.codes[self.index]
                else:
                    self.c_code = 'bloodyhell'
    
    def fetch(self, codes):
        self.initialize(codes)
        if self.codes == []:
            return {}
        base_url = 'https://www.reg.uci.edu/perl/WebSoc?'
        fields = [('YearTerm','2018-03'), ('CourseCodes',','.join(codes))]
        raw_info = 0
        while True:
            try:
                url = base_url + urllib.parse.urlencode(fields)
                print(url)
                raw_info = urllib.request.urlopen(url)
                data = raw_info.read().decode()
                self.feed(data)
                break
            except:
                time.sleep(2)
        raw_info.close()
        return self.result
                        
# if __name__ == '__main__':
#     p = SingleResultParser()
#     t = (p.fetch('38000 38001 38006 38026 38031 38047 38050 38052 38056 38061 38064 38066 38070 38072 38076 38077 38085 38091 38111 38113 38125 38127 38175 38195 38216 38294 38313 38382 38259 38271 38277 38432 38437 38457 38470 38471 38472 '.strip().split()))
#     with open('test.txt','w') as of:
#         for code, info in t.items():
#             of.write(code+'\n')
#             of.write('max: {}\n'.format(info[0]))
#             of.write('enr: {}\n'.format(info[1]))
#             of.write('wl: {}\n'.format(info[2]))
#             of.write('req: {}\n'.format(info[3]))
    
#   raw_info = urllib.request.urlopen('https://www.reg.uci.edu/perl/WebSoc?YearTerm=2017-92&CourseCodes=38432')
#     raw_info = urllib.request.urlopen('https://www.reg.uci.edu/perl/WebSoc?YearTerm=2018-03&CourseCodes=34110')

#     p.set_code('36595')
#     p.fetch('34110')
#     for i in p.return_data().values():
#     print('thing: {}'.format(i))

if __name__ == '__main__':
    p = SingleResultParser()
    print(p.fetch('20000,20001,20002,20006,20020,20022,20023,20025,20026,20027,20028,20029,20030,20031,20032,20034,20035,20036,20037,20038,20039,20040,20041,20042,20043,20044,20045,20046,20047,20048,20049,20050,20056,20057,20058,20059,20060,20061,20062,20063,20064,20065,20066,20067,20068,20069,20071,20072,20073,20074'.split(',')))
