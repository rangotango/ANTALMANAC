import urllib.request
from collections import OrderedDict
from html.parser import HTMLParser

def remove_white(string):
    temp = string.split()
    string = ''
    for i in temp:
        if i!='\xa0 ':
            string += ' '+i
    return string.strip()

def print_dict(d):
    for k,v in sorted(d.items(), key = lambda x: list(x[1].values())[0][0]):
        print('{} : {}'.format(k,dict(v)))
        
def into_flt(s):
    try:
        return float(s)
    except:
        return 0.0

class MyHTMLParser(HTMLParser):
    res = OrderedDict()
    look_light = False
    in_title_row = False
    get_num = False
    course_num = 0
    course_name = 'base'
    new_row = True
    col = 0
    course_code = ''

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0]=='class' and attr[1]=='CourseTitle':
                self.in_title_row = True
                self.get_num = True 
                break
        if tag=='tr' and attrs!=[] and attrs[0][0]=='valign' and attrs[0][1]=='top':
            if len(attrs) == 2 and attrs[1][0]=='bgcolor' and attrs[1][1]=='#FFFFCC':
                self.new_row = True
            else:
                self.look_light = True
        if self.look_light and tag == 'td' and attrs!=[] and attrs[0][0]=='bgcolor' and attrs[0][1]=='#DDEEFF':
            self.new_row = True
        if self.new_row and tag == 'td':
            self.col += 1
        
                
    def handle_endtag(self, tag):
        if self.in_title_row and tag=='font':
            self.in_title_row = False
        if tag =='tr':
            self.new_row = False
            self.look_light = False
            self.col=0
                

    def handle_data(self, data):
        if self.in_title_row:
            if self.get_num:        
                self.course_num = remove_white(str(data)).strip().split()[-1]
                self.get_num = False
            else:
                self.course_name = remove_white(str(data))
                if self.course_num not in self.res:
                    self.res[self.course_num]={}
                if self.course_name not in self.res[self.course_num]:
                    self.res[self.course_num][self.course_name]=[]
        if self.new_row:
            if self.col == 1:
                self.course_code = data
            if self.col == 4:
                if (into_flt(data)>0) or ('-' in data):
                    try:
                        self.res[self.course_num][self.course_name].append(self.course_code)
                    except:
                        print('found this \'{}\''.format(data))
                self.new_row = False
                self.look_light = False
                self.col=0
                        
    def my_reset(self):
        self.res.clear()
        self.in_title_row = False
        self.look_light = False
        self.get_num = False
        self.course_num = 0
        self.course_name = ''
        self.new_row = True
        self.col = 0
        self.course_code = ''

if __name__ == '__main__':
    raw_info = urllib.request.urlopen('https://www.reg.uci.edu/perl/WebSoc?YearTerm=2017-92&ShowFinals=1&ShowComments=1&Dept=COMPSCI&CourseNum=100-130')
#     raw_info = urllib.request.urlopen('https://www.reg.uci.edu/perl/WebSoc?YearTerm=2018-03&ShowFinals=1&ShowComments=1&Dept=AC+ENG')
    d=raw_info.read().decode()
#     print(d)
    p = MyHTMLParser()
    p.feed(d)
    raw_info.close()
    print_dict(p.res)
    
