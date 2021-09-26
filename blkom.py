#! python
import requests
import os
import re
from bs4 import BeautifulSoup as bs
Base_URL = "https://www.animeblkom.net"
soup = lambda url : bs(requests.get(url).content,"html.parser")

def search(user_input):
    search_URL = Base_URL + "/search?query=" + user_input.strip()
    results = soup(search_URL).select(".info")
    tit_url = [(i.div.a.text, Base_URL + i.div.a["href"]) for i in results]
    return dict(tit_url)

def display_results(lists):
    choises = list(lists.keys())
    for i in range(len(choises)):
        print(f"{i + 1}. \x1b[33m{choises[i]}\x1b[0m")
    choise = int(input("\n\x1b[41m\x1b[37mChoose one \x1b[0m : "))
    return choises[choise - 1]

def select_episodes(media_url) : 
    media_htm = soup(media_url)
    episodes = [ Base_URL + i.a["href"] for i in media_htm.select(".episode-link") ]
    if not(episodes) : return [media_url]
    else :
        episodes_num = [ int(i.split("/")[-1]) for i in episodes ]
        start,end = [ input(f"\n {i} EP : ") for i in ["Start on","End in"] ]
        sel = lambda i,opt : opt if i == "" else episodes_num.index(int(i))
        return episodes[sel(start,0):sel(end,-2) + 1]

def download(links) : 
    for link in links :
        dow_htm = soup(link)
        dow_link = dow_htm.find("a",text="Blkom")["data-src"]
        title = dow_htm.select_one(".current").text.strip()
        print(f"\n\x1b[41m\x1b[37mDownloading \x1b[0m ===> {title}")
        os.system(f'''youtube-dl "{dow_link}" -R 10 -o "{title}" --no-part''')

def main() :
    main_page = search(input("Search : "))
    while main_page == {} : 
        print("\n\n----- \x1b[41mNo Results\x1b[0m ----\n\n")
        main_page = search(input("Search : "))
    selected = display_results(main_page)
    try : 
        os.mkdir(selected)
        os.chdir(selected)
    except FileExistsError : os.chdir(selected)
    episodes = select_episodes(main_page[selected])
    download(episodes)

try : main()
except KeyboardInterrupt : print("\n\nExit .....")