import re


html_tag = re.compile('<[^>]*>')

def filter_tag(content):
    content = re.sub(html_tag, '', content)
    return content


filter_funcs = {
    'filter_tag': filter_tag
}