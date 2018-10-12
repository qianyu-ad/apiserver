import re



html_tag = re.compile('<[^>]*>')


def filter_tag(content, slice_count=150):
    content = re.sub(html_tag, '', content)
    return content[:slice_count]

filter_funcs = {
    'filter_tag': filter_tag,
}
