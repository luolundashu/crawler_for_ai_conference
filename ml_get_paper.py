from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import requests
import time
from tqdm import tqdm

def contains_keyword(keyword, text):
    return keyword.lower() in text.lower()


def create_web(paper_list,conference_name,key_word,url_name,patience=20):
    if contains_keyword('iclr', conference_name):
        paper_dir_father = "./paper/{}/{}/{}/".format(conference_name,url_name,key_word)
    elif contains_keyword('NeurIPS', conference_name):
        paper_dir_father = "./paper/{}/{}/".format(conference_name, key_word)
    elif contains_keyword('icml', conference_name):
        paper_dir_father = "./paper/{}/{}/".format(conference_name, key_word)

    if os.path.exists(paper_dir_father) is not True:
        os.makedirs(paper_dir_father)

    for i in tqdm(range(len(paper_list))):
        if contains_keyword('icml', conference_name):
            paper_name = paper_list[i].text.strip()
        else:
            paper_name = paper_list[i].find('h4').text.strip()
        paper_name = paper_name.replace('/', '')
        paper_name = paper_name.replace(':', '')
        if contains_keyword(key_word, paper_name):
            if contains_keyword('icml', conference_name):
                paper_down_dir = paper_list[i].find('a', class_='pdf-link')['href']
            else:
                paper_down_dir = paper_list[i].find('h4').find('a', class_='pdf-link')['href']
            paper_down_dir = 'https://openreview.net{}'.format(paper_down_dir)
            for pat in range(patience):
                response = requests.get(paper_down_dir)
                if response.status_code == 200:
                    with open("{}/{}.pdf".format(paper_dir_father,paper_name), "wb") as pdf_file:
                        pdf_file.write(response.content)
                        time.sleep(3)
                    break
                else:
                    print('第{}次尝试写入,地址{}'.format(pat,paper_down_dir))
                    if pat==patience-1:
                        print('{}为写入成功，网址{}'.format(pat,paper_down_dir))
                        continue



def crete_url(conference_name):
    if contains_keyword('iclr',conference_name):
        url ={
            'top_5':'https://openreview.net/group?id=ICLR.cc/{}/Conference#notable-top-5-'.format(conference_name[-4:]),
            'top_25':'https://openreview.net/group?id=ICLR.cc/{}/Conference#notable-top-25-'.format(conference_name[-4:]),
            'top_100':'https://openreview.net/group?id=ICLR.cc/{}/Conference#poster'.format(conference_name[-4:])
        }
    elif contains_keyword('icml',conference_name):
        url={"top_100":"https://openreview.net/group?id=ICML.cc/{}/Conference".format(conference_name[-4:])}
    elif contains_keyword('NeurIPS',conference_name):
        url={"top_100":"https://openreview.net/group?id=NeurIPS.cc/{}/Conference".format(conference_name[-4:])}

    return url

if __name__ =='__main__':
    keyword_list = ['Diffusion','Anomaly Detection','Time Series','Bayesian','Out of Distribution']
    conference_name_list =['ICML2023']
    options = Options()
    driver = webdriver.Chrome(service=Service('./chromedriver-win64/chromedriver.exe'), options=options)
    os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890"
    os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890"

    for conference_name in conference_name_list:
        url = crete_url(conference_name)
        for keyword in keyword_list:
            # 打开目标页面
            for url_name in url:

                driver.get(url[url_name])
                time.sleep(3)
                # 循环处理多个页面
                for i in range(1000):
                    # 获取当前页面的 HTML
                    i = i +1
                    if i>1:
                        try :
                            if contains_keyword('icml',conference_name):
                                next_page_button = driver.find_element(By.XPATH,
                                                                       '//li[not(@class="active")]/a[@role="button" and text()="{}"]'.format(
                                                                           i))
                            else:
                                next_page_button = driver.find_element(By.CSS_SELECTOR, 'li[data-page-number="{}"] a'.format(i))
                            next_page_button.click()
                            print('会议：{}__ 关键词{}加载第{}页'.format(conference_name,keyword,i))
                            time.sleep(3)
                        except Exception as e:
                            print('*'*20)
                            print('会议：{}__ 关键词{}已经全部爬取完成'.format(conference_name,keyword))
                            print('*'*20)
                            break

                    page_content = driver.page_source
                    soup = BeautifulSoup(page_content, 'html.parser')
                    if contains_keyword('icml',conference_name):
                        paper_list = soup.find_all('ul', class_='list-unstyled list-paginated')[0].find_all('h4')
                        create_web(paper_list, conference_name, keyword, url_name)
                    else:
                        paper_list = soup.find_all('li',class_='note')
                        create_web(paper_list,conference_name,keyword,url_name)


