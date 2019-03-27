import requests
from datetime import datetime
from datetime import time
from datetime import timedelta

def main():
    #https://aa.usno.navy.mil/data/docs/api.php
    if False:
        times = []
        startdate = datetime(2019,1,1)
        loopdate = startdate
        for i in range(365):
            
            #date_str =loopdate.strftime('%D') 
            date_str = loopdate.strftime('%m/%d/%Y').lstrip("0").replace(" 0", " ") #'1/1/2019'
            print(date_str)
            loc_str = 'Battle Lake, MN'
            r_url = r'https://api.usno.navy.mil/rstt/oneday?date={}&loc={}'.format(date_str,loc_str)
            print(r_url)
            
            r = requests.get(url=r_url)
            
            print(r.text)
        
            begin, end = parseResponseToTimeDelta(response=r)
            
            FMT = '%H:%M:%S'
            tdelta = datetime.strptime(str(end), FMT) - datetime.strptime(str(begin), FMT)
            times.append(tdelta)
            loopdate = startdate + timedelta(i)
        
        print(times)
        time_sum = sum(times, timedelta())
        print(time_sum)
   
    time_sum = timedelta(202, 80280)
    total_hours = time_sum.total_seconds()/3600
    
    #random calcs:
    wattage = 9
    kwh_price = 0.109
    total_cost = total_hours*(wattage/1000)*kwh_price
    print(f'It costs ${total_cost:.2f} a year ({total_hours} hours) to power something from dusk to dawn that draws {wattage}W at ${kwh_price:.2f} per kWh. ')
    #It costs $4.78 a year (4870.3 hours) to power something from dusk to dawn that draws 9W at $0.11 per kWh. 
    
    #datetime.timedelta(202, 80280)
    
    x=1

def parseResponseToTimeDelta(response):
    rjson = response.json()
    begin_civil = extractValueFromDictionaryListByKey(rjson["sundata"], 'phen', 'BC', 'time')
    end_civil = extractValueFromDictionaryListByKey(rjson["sundata"], 'phen', 'EC', 'time')
    
    begin_time = parseTimeFromString(begin_civil)
    end_time = parseTimeFromString(end_civil)
    return begin_time, end_time
    

def parseTimeFromString(date_str):
    parts = date_str.split(' ')
    hour = int(parts[0].split(':')[0])
    minute = int(parts[0].split(':')[1])
    ampm = parts[1]
    if ampm == 'p.m.':
        hour += 12
    return time(hour, minute)
        
def extractValueFromDictionaryListByKey(phenomenon_list_json, target_key, target_value, value_key):
    for json_dict in phenomenon_list_json:
        if json_dict[target_key] == target_value:
            return json_dict[value_key]
    return None


if __name__=='__main__':
    main()
