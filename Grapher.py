from pathlib import Path
import time
from matplotlib import pyplot as plt
from matplotlib import style
from datetime import datetime, date, timedelta
STORE_PATH = Path('C:\\Users\\rangu_uhpmatw\\Documents\\ANTALMANAC\\W18')
GENESIS = date(2017,11,20)
NUM_CODES = 10

def fetch_cur_data():
    hora = date.today()
    return (STORE_PATH/Path(str(hora.month)+'-'+str(hora.day)+'.txt')).open('r')

def start_blank(*name):
    hora = date.today()
    if len(name) == 0:
        file_name = str(hora.month)+'-'+str(hora.day)+'.txt'
    else:
        file_name = name[0]+'.txt'
    out_file = (STORE_PATH/Path(file_name)).open('w')
    return out_file

def wkday_trans(day):
    if day == 0:
        return 'Mon'
    if day == 1:
        return 'Tue'
    if day == 2:
        return 'Wed'
    if day == 3:
        return 'Thu'
    if day == 4:
        return 'Fri'
    if day == 5:
        return 'Sat'
    if day == 6:
        return 'Sun'
    return 'Wtf'

def get_rela_dates(abs_dates):
    result = []
    week = 8
    day = 0
    for i in range(abs_dates):
        result.append('WK{}:{}'.format(week,wkday_trans(day)))
        day += 1
        if day == 7:
            day = 0
    return result

def process_wl(wl,num):
    if len(wl) == 1:
        return 0
    if wl[-1] == 'n/a':
        for i in range(num-len(wl)+1):
            wl.append(0)
    return [int(i) for i in wl]

def process_max(cap,num):
    if len(cap) == 1:
        return [int(cap[0]) for i in range(num)]
    result = []
    last_time = GENESIS
    for i in range(0,len(cap)-1,2):
        cur_time = cap[i+1]
        cp = cur_time.find('-')
        y = int(cur_time[1:cp])
        m = int(cur_time[cp+1:cur_time.find('-',cp+1)])
        d = int(cur_time[cur_time.find('-',cp+1)+1:-1])
        cur_time = date(y,m,d)
        gap = cur_time - last_time
        for j in range(gap.days):
            result.append(int(cap[i]))
        last_time = cur_time
    for i in range((date.today()-last_time).days+1):
        result.append(int(cap[-1]))
    return result

def graph_indiv(enr, req):
    return '\n'.join('{}/{}:{}'.format((GENESIS+timedelta(i)).month,(GENESIS+timedelta(i)).day,'|'*(int(enr[i])))for i in range(len(enr)))
        
def graph():
    in_file = fetch_cur_data()
    
    while True:
        print('what the damn do u want?')
        code = input()
        if code == 'fu':
            break

#         out_file = start_blank('Gs')
        in_file.seek(0)
        poss = True
        for line in in_file:
            if line == '=====':
                poss = False
                break
            if code == line.strip():
                break
    
        if not poss:
            print('wtf that dont exist')
            continue
    
        cap_rec = in_file.readline().strip().split()
        enr_rec = in_file.readline().strip().split()
        req_rec = in_file.readline().strip().split()
        wl_rec = in_file.readline().strip().split()
        num_rec = len(enr_rec)
        
        print('max: {}'.format(cap_rec))
        print('enr: {}'.format(enr_rec))
        print('req: {}'.format(req_rec))
        print('wl:  {}'.format(wl_rec))
        
        style.use('ggplot')
        
#         x = ['{}-{}'.format((GENESIS+timedelta(i)).month,(GENESIS+timedelta(i)).day) for i in range(len(enr_rec))]
        x = [i for i in range(num_rec)]
        plt.xticks(x,get_rela_dates(num_rec))
        
#         plt.axis([x[0],x[-1],0,(int(cap_rec[-1])+20)])
        y_m = process_max(cap_rec,num_rec)
        plt.plot(x,y_m,linewidth=2, label='Maximum')
        for i,j in zip(x,y_m):
            plt.annotate(str(j),xy=(i,j))
        
        y_e = [int(i) for i in enr_rec]
        plt.plot(x,y_e,linewidth=2, label='Enrolled')
        for i,j in zip(x,y_e):
            plt.annotate(str(j),xy=(i,j))

        y_r = [int(i) for i in req_rec]
        plt.plot(x,y_r,linewidth=2, label='Requested')
        for i,j in zip(x,y_r):
            plt.annotate(str(j),xy=(i,j))
            
        rendered_wl = process_wl(wl_rec,num_rec)
        if rendered_wl != 0:
            plt.plot(x,rendered_wl,linewidth=2,label='Waitlisted')      
            for i,j in zip(x,rendered_wl):
                plt.annotate(str(j),xy=(i,j))
  
        
        plt.title('Registration History for {}'.format(code))
        plt.ylabel('Number of People')
        plt.xlabel('Time (As of the End of the Day)')
        
        plt.legend()
        plt.grid(True,color='k')
        
        plt.show()
        
#         print(graph_indiv(enr_rec,req_rec))
#         out_file.write(code)
#         out_file.write(graph_indiv(enr_rec,req_rec))
#         out_file.write('\n')
#         out_file.close()
    in_file.close()

if __name__ == '__main__':
    print(datetime.now())
    graph()
    print(datetime.now())
