import webbrowser

def search(query, saerch_engine='google'):
    url = f'https://www.google.com/search?q={query}'
    if saerch_engine == 'google' or saerch_engine == '구글':
        url = f'https://www.google.com/search?q={query}'
    elif saerch_engine == 'naver' or saerch_engine == '네이버':
        url = f'https://search.naver.com/search.naver?query={query}'
    elif saerch_engine == 'bing' or saerch_engine == '빙':
        url = f'https://www.bing.com/search?q={query}'

    webbrowser.open(url)

search('컴퓨터', 'bing')
