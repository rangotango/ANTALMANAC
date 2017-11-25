from pathlib import Path
import time
from datetime import datetime, date, timedelta
import Course_Page_Parser, Seeder_Fetch_Write
STORE_PATH = Path('C:\\Users\\rangu_uhpmatw\\Documents\\ANTALMANAC\\W18')

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
    out_file = Seeder_Fetch_Write.start_blank()
    doggo = Course_Page_Parser.SingleResultParser()
    
    count = 0
    while True:
        if count == 20:
            count = 0
            time.sleep(2)
        else:
            count += 1
        code = in_file.readline().strip()
        if code == '=====':
            break
        doggo.my_reset()
        doggo.fetch(code)
        out_file.write(code+'\n')
        
        poop = doggo.return_data()
        
        past_max_rec = in_file.readline().strip()
        past_max = past_max_rec.split()[-1]
        if poop['m'] != past_max:
            out_file.write(past_max_rec+' ('+str(date.today())+') '+poop['m']+'\n')
        else:
            out_file.write(past_max_rec+'\n')

        past_enr = in_file.readline().strip()
        out_file.write(past_enr + ' ' + poop['e'] + '\n')
        
        past_req = in_file.readline().strip()
        out_file.write(past_req + ' ' + poop['r'] + '\n')
        
        past_wl = in_file.readline().strip()
        if past_wl == 'n/a':
            out_file.write('n/a\n')
        elif past_wl.split()[-1] != 'n/a':
            out_file.write(past_wl + ' ' + poop['w'] + '\n')
        else:
            out_file.write(past_wl + '\n')
    in_file.close()
    out_file.write('=====')
    out_file.close()

if __name__ == '__main__':
    print(datetime.now())
    update()
    print(datetime.now())
