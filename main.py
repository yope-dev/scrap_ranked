import requests
from bs4 import BeautifulSoup
import random
from openpyxl import Workbook
import time
from concurrent.futures import ThreadPoolExecutor


MAX_THREADS = 10
START_PAGE = 1
AMOUNT_OF_PAGES = 100

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
]


class Repository:
    def __init__(self, name, link, website, forks, stars, trendshift_id, lang_id, description):
        self.name = name
        self.link = link
        self.website = website
        self.forks = forks
        self.stars = stars
        self.trendshift_id = trendshift_id
        self.lang_id = lang_id
        self.description = description

    def __str__(self):
        return (f"Repository Name: {self.name}\n"
                f"Link: {self.link}\n"
                f"Website: {self.link}\n"
                f"Forks: {self.forks}\n"
                f"Stars: {self.stars}\n"
                f"Trendshift ID: {self.link}\n"
                f"Lang ID: {self.link}\n"
                f"Description: {self.description}\n")


def get_random_headers():
    user_agent = random.choice(user_agents)
    headers = {
        "User-Agent": user_agent,
        "Accept": "*/*",
    }
    return headers


def save_repositories_to_excel(file_name):
    global repositories
    wb = Workbook()
    ws = wb.active
    ws.title = "Repositories"
    headers = ["Name", "Link", "Trendshift ID", "Lang ID", "Stars", "Forks", "Description"]
    ws.append(headers)
    for repo in repositories:
        ws.append([repo.name, repo.link, repo.trendshift_id, repo.lang_id,repo.stars, repo.forks, repo.description])
    wb.save(file_name)


def get_info(index):
    global repositories
    page = requests.get(f'https://trendshift.io/repositories/{index}', headers=get_random_headers())
    if page.status_code != 200:
        return
    soup = BeautifulSoup(page.text, 'html.parser')
    git_hub_link = ''
    website = ''
    links = soup.find_all(attrs={'target': '_blank'}, href=True)
    for link in links:
        text = link.get_text().lower()
        if text == 'visit vithub':
            git_hub_link = link['href']
        elif text == 'website':
            website = link['href']
    name = ''
    if git_hub_link != '':
        name = git_hub_link[git_hub_link.rfind('/')+1:]
    else:
        try:
            name = soup.find(class_='flex items-center text-indigo-400 text-lg justify-between mb-1').find('div').get_text()
        except:
            name = ''
    descr = ''
    try:
        if soup.find(class_='text-sm text-gray-500'):
            descr = soup.find(class_='text-sm text-gray-500').get_text()
    except:
        descr = ''
    forks = 0
    stars = 0
    try:
        lang_id = soup.find(class_='text-gray-500 flex items-center text-xs md:text-sm').get_text()
    except:
        lang_id = -1
    for test in soup.find_all(class_='flex items-center'):
        if test.find('svg'):
            if test.find('svg').find(d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"):
                stars = test.get_text()
            elif test.find('svg').find(d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z"):
                forks = test.get_text()
    repositories.append(Repository(name, git_hub_link, website, forks, stars, index, lang_id, descr))


if __name__ == '__main__':
    start_time = time.time()
    repositories = []
    threads = []
    print('Scraping data from Trendshift.io...')
    with ThreadPoolExecutor(MAX_THREADS) as executor:
        futures = [executor.submit(get_info, i) for i in range(AMOUNT_OF_PAGES)]
    print('Saving data to repositories.xlsx...')
    save_repositories_to_excel('repositories.xlsx')
    print(f"Done!\nTime taken to run the script: {(time.time()-start_time):.2f} seconds")





