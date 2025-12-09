import re

URL_RE = re.compile(r'https?://\S+')
WHITESPACE_RE = re.compile(r'\s+')
USER_RE = re.compile(r'u/\w+|@\w+')
SUB_RE = re.compile(r'r/\w+')

def clean(text: str) -> str:
    if not text:
        return ''
    t = URL_RE.sub('', text)
    t = USER_RE.sub('[user]', t)
    t = SUB_RE.sub('[sub]', t)
    t = t.strip()
    t = WHITESPACE_RE.sub(' ', t)
    return t
