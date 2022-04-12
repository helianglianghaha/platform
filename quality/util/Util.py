import datetime
import time
import json
import random

class Multithreading():


# 生成20位的唯一值  
def get_unique_value():
    try:
        t = time.time()
        nowTime = int(round(t * 1000))
        num = random.randint(1000000,9999999)
        return str(nowTime)+str(num)
       
    except Exception as e:
        raise e 
        return None

def get_now_date():
    try:
        t = datetime.datetime.now()
        nowTime = t.strftime('%Y-%m-%d')
        return nowTime
       
    except Exception as e:
        raise e 
        return None

def get_now_datetime():
    try:
        t = datetime.datetime.now()
        nowTime = t.strftime('%Y-%m-%d %H:%M:%S')
        return nowTime
       
    except Exception as e:
        raise e 
        return None
    
        

