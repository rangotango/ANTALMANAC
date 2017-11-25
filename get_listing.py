import urllib.request
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    listing = False
    res = []

    def handle_starttag(self, tag, attrs):
        if self.listing and tag == 'option':
            for attr in attrs:
                if attr[0]=='value':
                    self.res.append(attr[-1])

    def handle_endtag(self, tag):
        if tag =='select':
            self.listing=False

    def handle_data(self, data):
        if data == 'Include All Departments':
            self.listing = True

if __name__ == '__main__':
    out_file = open('listing.txt','w')
    raw_info = urllib.request.urlopen('https://www.reg.uci.edu/perl/WebSoc')
    p = MyHTMLParser()
    p.feed(raw_info.read().decode(encoding='utf-8'))
    for i in p.res:
        out_file.write(i+'\n')
    print(len(p.res))
    raw_info.close()
    out_file.close()
    
