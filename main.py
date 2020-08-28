import requests
import re
import pandas as pd
from multiprocessing.pool import ThreadPool as Pool
import multiprocessing as mp
import sys

Dict = []
def work(i):
    ID = str(i)
    for j in range(5-len(ID)):
        ID = '0' + ID
    ID = '020' + ID
    
    try:
        raw = requests.get("https://diemthi.tuoitre.vn/kythi2020.html?FiledValue="+ID+"&MaTruong=DDT")
        data = raw.text
        sbd = re.search('<span id="ctl01_SoBD" class="diem">(.*)</span>', data).group(1)
        ten = re.search('<span id="ctl01_tenthisinh" class="diem">(.*)</span>', data).group(1)

        diem = re.search('<td class="color-red">(.*)</td>', data)

        diem = list(diem.group(1).replace('</td><td class="color-red">', ' ').split(' '))

        data = re.search('<td class="red">(.*)</td>', data).group(0)
        
        j = 0
        if '>Toán' in data:
            toan = diem[j]
            j = j + 1
        else:
            toan = None
        
        if '>văn' in data or '>Ngữ văn' in data:
            van = diem[j]
            j = j + 1
        else:
            van = None
        
        if '>Vật lí' in data:
            ly = diem[j]
            j = j + 1
        else:
            ly = None

        if '>Hóa học' in data:
            hoa = diem[j]
            j = j + 1
        else:
            hoa = None
        
        if '>Sinh học' in data:
            sinh = diem[j]
            j = j + 1
        else:
            sinh = None
        
        if '>KHTN' in data:
            khtn = diem[j]
            j = j + 1
        else:
            khtn = None
        
        if '>Lịch sử' in data:
            su = diem[j]
            j = j + 1
        else:
            su = None
        
        if '>Địa lí' in data:
            dia = diem[j]
            j = j + 1
        else:
            dia = None
        
        if '>GDCD' in data:
            cd = diem[j]
            j = j + 1
        else:
            cd = None
        
        if '>KHXH' in data:
            khxh = diem[j]
            j = j + 1
        else:
            khxh = None

        if '>Tiếng' in data:
            anh = diem[j]
            j = j + 1
        else:
            anh = None
        
        
        print(sbd + ' ' + ten)

        sbd.replace(' ', '')
        
        Dict.append([sbd, ten, toan, van, anh, ly, hoa, sinh, khtn, su, dia, cd, khxh])
    except Exception as e:
        print(e)
        pass

#74718

pool = Pool(mp.cpu_count() - 1)


for i in range(1, 74718):  
    pool.apply_async(work, (i,))

pool.close()
pool.join()


def save():
    print(Dict)
    df = pd.DataFrame(Dict, columns = ['sbd', 'ten', 'toan', 'van', 'ngoai ngu', 'ly', 'hoa', 'sinh', 'khtn', 'su', 'dia', 'gdcd', 'khxh'])

    df.to_csv("data.csv", encoding='utf-8-sig', index=False)

save()
