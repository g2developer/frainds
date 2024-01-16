import webbrowser

from utils import has


class WebSearch:
    cmm_target_lst = ['인터넷', 'internet']
    eg_lst1 = ['google', '구글', 'googling']
    eg_lst2 = ['naver', '네이버']
    eg_lst3 = ['bing', '빙으로', '빙에서']
    eg_lst4 = ['youtube', '유튜브', '유투브', '유튭으', '너튜브']
    

    cmm_lst = ['찾아', '검색', 'search']

    def __init__(self):
        pass

    def is_this_action(self, txt):
        is_target = has(txt, self.cmm_target_lst+self.eg_lst1+self.eg_lst2+self.eg_lst3)
        is_action = has(txt, self.cmm_lst)
        return is_target and is_action


    def action(self, data):
        search_engine = self.get_search_engine(data)
        keyword = self.get_keyword(data)
        print('')
        url = f'https://www.google.com/search?q={keyword}'
        if not search_engine or search_engine == 'google':
            url = f'https://www.google.com/search?q={keyword}'
        elif search_engine == 'naver':
            url = f'https://search.naver.com/search.naver?query={keyword}'
        elif search_engine == 'bing':
            url = f'https://www.bing.com/search?q={keyword}'
        elif search_engine == 'youtube':
            url = f'https://www.youtube.com/results?search_query={keyword}'

        webbrowser.open(url)

    def get_keyword(self, data: str):
        lst = data.split(' ')
        lst2 = []
        for i in lst:
            if has(i, self.cmm_target_lst) \
                    or has(i, self.eg_lst1) or has(i, self.eg_lst2) or has(i, self.eg_lst3):
                continue
            elif has(i, self.cmm_lst):
                continue
            elif i.replace(' ', '') == '좀':
                continue
            else:
                lst2.append(i.replace(' ', ''))
        keyword = ' '.join(lst2)
        return keyword

    def get_search_engine(self, data):
        search_engine = None
        if has(data, self.eg_lst1):
            search_engine = 'google'
        elif has(data, self.eg_lst2):
            search_engine = 'naver'
        elif has(data, self.eg_lst3):
            search_engine = 'bing'
        elif has(data, self.eg_lst4):
            search_engine = 'youtube'

        return search_engine
