import re
import time
import random
from datetime import datetime

now = datetime.now()

min_st = (2013,1,1,0,0,0,0,0,0)
max_et = (now.year, now.month, now.day, 23,59,59,0,0,0)

start_time = time.mktime(min_st)
end_time = time.mktime(max_et)

dt_cache = {}


def random_date():
    r = random.randint(start_time, end_time)
    date = time.localtime(r)
    date_str = time.strftime('%Y-%m-%d %H:%M:%S', date)
    return date_str


html_tag = re.compile('<[^>]*>')


def filter_tag(content):
    content = re.sub(html_tag, '', content)
    return content


def filter_rd_date(dt):
    global dt_cache
    if dt not in dt_cache:
        rd_dt = random_date()
        if len(dt_cache) > 100:
            dt_cache = {}
        dt_cache[dt] = rd_dt
        return rd_dt
    else:
        return dt_cache[dt]


filter_funcs = {
    'filter_tag': filter_tag,
    'filter_rd_date': filter_rd_date,
}
