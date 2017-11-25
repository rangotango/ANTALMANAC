from pathlib import Path
from datetime import datetime
import time
import urllib.request, urllib.parse
import Seeder_Page_Parser
import Course_Page_Parser
STORE_PATH = Path('C:\\Users\\rangu_uhpmatw\\Documents\\ANTALMANAC\\W18')

def start_blank(*name):
    hora = datetime.now()
    if len(name) == 0:
        file_name = str(hora.month)+'-'+str(hora.day)+'.txt'
    else:
        file_name = name[0]+'.txt'
    out_file = (STORE_PATH/Path(file_name)).open('w')
    return out_file

def get_listing():
    in_file = open('listing.txt')
    temp = in_file.readlines()
    in_file.close()
    return temp    

def create_course_ref():
    cf = start_blank('course_ref')
    data = start_blank()
    parser = Seeder_Page_Parser.MyHTMLParser()
    count = 0
    for dept in get_listing():
        if count == 20:
            count = 0
            time.sleep(2)
        else:
            count += 1
        base_url = 'https://www.reg.uci.edu/perl/WebSoc?'
        fields = [('YearTerm','2018-03'), ('Dept',dept.strip('\n'))]
        raw_info = 0
        while True:
            try:
                raw_info = urllib.request.urlopen(base_url + urllib.parse.urlencode(fields))
                parser.my_reset()
                parser.feed(raw_info.read().decode())
                break
            except:
                time.sleep(2)
        raw_info.close()

        cf.write(dept)
        for courses in parser.res.values():
            for codes in courses.values(): 
                for code in codes:
                    cf.write(code + ' ')
        cf.write('\n')
        
        doggo = Course_Page_Parser.SingleResultParser()
        for courses in parser.res.values():
            for codes in courses.values():
                for code in codes:
                    data.write(code+'\n')
                    doggo.my_reset()
                    doggo.fetch(code)
                    for i in doggo.return_data().values():
                        data.write(str(i)+'\n')
                data.flush()
                    
    data.write('=====')
    cf.close()
    data.close()

if __name__ == '__main__':
    print(datetime.now())
    create_course_ref()
    print(datetime.now())
