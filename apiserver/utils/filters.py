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

filter_funcs = {
    'filter_tag': filter_tag,
}
