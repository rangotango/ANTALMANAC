from pathlib import Path
import time
from datetime import datetime, date, timedelta
import fCourse_Page_Parser
STORE_PATH = Path('C:\\Users\\rangu_uhpmatw\\Documents\\ANTALMANAC\\W18')
NUM_CODES = 10

def fetch_old():
    yesterdate = date.today()-timedelta(1)
    in_file = (STORE_PATH/Path(str(yesterdate.month)+'-'+str(yesterdate.day)+'.txt')).open('r')
    return in_file

def start_blank(*name):
    hora = date.today()
    if len(name) == 0:
        file_name = str(hora.month)+'-'+str(hora.day)+'.txt'
    else:
        file_name = name[0]+'.txt'
    out_file = (STORE_PATH/Path(file_name)).open('w')
    return out_file

def update():
    in_file = fetch_old()
    out_file = start_blank('tempx')
    doggo = fCourse_Page_Parser.SingleResultParser()
    done = False
    while not done:
        search = []
        checkpt = in_file.tell()
        for i in range(NUM_CODES):
            c_code = in_file.readline().strip()
            if c_code == '=====':
                done = True
                break
            search.append(c_code)
            for j in range(4):
                in_file.readline()
        
        poop = doggo.fetch(search)
        in_file.seek(checkpt)
        for i in range(NUM_CODES):
            if_code = in_file.readline().strip()
            if if_code == '=====':
                break
            code = if_code
            out_file.write(code+'\n')
            
            past_max_rec = in_file.readline().strip()
            past_max = past_max_rec.split()[-1]
            
            if poop[code][0] != past_max:
                out_file.write(past_max_rec+' ('+str(date.today())+') '+poop[code][0]+'\n')
            else:
                out_file.write(past_max_rec+'\n')

            past_enr = in_file.readline().strip()
            out_file.write(past_enr + ' ' + str(poop[code][1]) + '\n')
        
            past_req = in_file.readline().strip()
            out_file.write(past_req + ' ' + str(poop[code][3]) + '\n')
        
            past_wl = in_file.readline().strip()
            if past_wl == 'n/a':
                out_file.write('n/a\n')
            elif past_wl.split()[-1] != 'n/a':
                out_file.write(past_wl + ' ' + str(poop[code][2]) + '\n')
            else:
                out_file.write(past_wl + '\n')
                
        out_file.flush()
    in_file.close()
    out_file.write('=====')
    out_file.close()

if __name__ == '__main__':
    print(datetime.now())
    update()
    print(datetime.now())
