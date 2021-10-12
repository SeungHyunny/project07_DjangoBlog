from urllib.parse import quote_plus
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.shortcuts import render
import requests


def get_html_content(request):
    movie = request.GET.get('movie')
    movie = movie.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query={movie}').text
    return html_content

def movieSearch(request):
    result = None
    if 'movie' in request.GET:
        # fetch the weather from Google.
        html_content = get_html_content(request)
        soup = BeautifulSoup(html_content, 'html.parser')
        result = dict()
        try:
            result['name'] = soup.find("strong", attrs={"class" : "_text"}).text
            result['info'] = soup.find("span", attrs={"class" : "desc _text"}).text
            res1 = soup.find("div", {"class" : "detail_info"})
            result['img'] = res1.find("img")['src']
            
            ##################################################

            res2 = soup.find("div", {"class" : "cm_info_box scroll_img_vertical_105_148"}).select('li > div > a > div > img')
            result['poster'] = str(res2).replace(',',"").replace(']',"").replace('[',"")
            


        except:
            pass

    return render(request, 'blog/post_crawling.html', {'result': result})
