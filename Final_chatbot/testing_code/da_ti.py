from datetime import datetime,timedelta

def datetimenow(): #datetimenow
    dt= datetime.now()
    return dt

def day_today(): #datetimeweekday

    today= datetimenow().strftime('%A')
    return today

def current_time(): #datetimetime
    timern = datetimenow().hour
    return timern 

def day_tommorrow():
    tommorrow= datetimenow() + timedelta(days=1)
    return tommorrow.strftime('%A')

def day_aftertommorrow():
    parso= datetimenow() + timedelta(days=2)
    return parso.strftime('%A')

day_today()
current_time()
day_tommorrow()
day_aftertommorrow()