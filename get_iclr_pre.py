from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import requests
import time
from tqdm import tqdm
import re
from selenium.webdriver.common.action_chains import ActionChains

def contains_keyword(keyword, text):
    return keyword.lower() in text.lower()

def remove_symbols(input_string):
    # 使用正则表达式去除特定符号，保留连字符（-）
    cleaned_string = re.sub(r'[^\w\s-]', '', input_string)
    return cleaned_string

def count_paper_rate(web,driver_child,patient =10):
    paper_web = 'https://openreview.net/{}'.format(web)
    driver_child.get(paper_web)
    time.sleep(3)
    for pat in range(patient):
        try:
            rate_list = []
            for rate_idx in range(6):
                try:
                    try:
                        rate = driver_child.find_element(By.XPATH,'//*[@id="forum-replies"]/div[{}]/div[4]/div/div[9]/span'.format(rate_idx+1)).text[0]
                    except:
                        #我也不理解为什么突然的xpath是这样
                        rate = driver_child.find_element(By.XPATH,
                                                         '//*[@id="forum-replies"]/div[{}]/div[4]/div/div[10]/span'.format(
                                                             rate_idx + 1)).text[0]
                    rate_list.append(int(rate))
                except:
                    continue
            rate_average = sum(rate_list) / len(rate_list)
            break
        except:
            print('求论文分数失败，脚本将在3秒后继续请求')
            time.sleep(3)

    return rate_average



def create_web(paper_list,socre_thre,driver_child,conference_name,keyword_list,id_name,paper_tppe,patience=20):
    for key_word in keyword_list:
        paper_dir_father = "./paper_pre/{}/{}/{}/".format(conference_name,id_name,key_word)


        if os.path.exists(paper_dir_father) is not True:
            os.makedirs(paper_dir_father)

        for i in tqdm(range(len(paper_list))):
            if paper_tppe==True:
                paper_name = paper_list[i].text.strip()
            elif paper_tppe==False:
                paper_name = paper_list[i].find('h4').text.strip()

            paper_name = remove_symbols(paper_name)

            if contains_keyword(key_word, paper_name):
                paper_rate = count_paper_rate(paper_list[i].find('a')['href'],driver_child)
                if paper_rate>socre_thre:
                    try:
                        paper_down_dir = paper_list[i].find('a', class_='pdf-link')['href']
                    except:
                        paper_down_dir = paper_list[i].find('h4').find('a', class_='pdf-link')['href']

                    paper_down_dir = 'https://openreview.net{}'.format(paper_down_dir)
                    for pat in range(patience):
                        try:
                            response = requests.get(paper_down_dir)
                            with open("{}/{}_rate_{}.pdf".format(paper_dir_father, paper_name,paper_rate), "wb") as pdf_file:
                                pdf_file.write(response.content)
                            break

                        except:
                            print('请求失败，暂停100秒')
                            time.sleep(3)
                            pass







def contains_keyword_list(keyword, text_list):
    for text in text_list:
        if contains_keyword(text,keyword):
            return True

    return False



if __name__ =='__main__':
    options = Options()
    driver = webdriver.Chrome(service=Service('./chromedriver-win64/chromedriver.exe'), options=options)
    driver_child = webdriver.Chrome(service=Service('./chromedriver-win64/chromedriver.exe'), options=options)
    os.environ['HTTP_PROXY'] = "http://127.0.0.1:7897"
    os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7897"
    sleep_patience=1
    conference_name = 'ICLR2025'
    keyword_list = ['Distribution','Diffusion']
    url = 'https://openreview.net/group?id=ICLR.cc/2025/Conference#tab-active-submissions'
    socre_thre =5.5
    # 打开目标页面
    driver.get(url)
    time.sleep(3)

    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    # paper_level = soup.find('div', class_='mobile-full-width').find('ul', class_='nav nav-tabs').find_all('li',
    #                                                                                                       role='presentation')
    id_name = 'active-submissions'
    for i in range(1000):
        # 获取当前页面的 HTML
        i = i + 1
        if i > 1:
            try:
                try:
                    next_page_button = driver.find_element(By.XPATH,
                                                           '//*[@id="{}"]/div/div/nav/ul/li/a[text()={}]'.format(
                                                               id_name, i))
                except:
                    next_page_button = driver.find_element(By.XPATH,
                                                           "//*[@id='{}']/nav/ul/li/a[text()='{}']".format(
                                                               id_name, i))
                next_page_button.click()
                time.sleep(2)
                print('加载第{}页'.format( i))

            except Exception as e:
                print('*' * 20)
                print('加载第{}页'.format( i))
                print('*' * 20)
                break

        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')

        try:
            paper_list = \
            soup.find_all('div', id=id_name)[0].find_all('ul', class_='list-unstyled list-paginated')[
                0].find_all('h4')
            paper_tppe = True
        except:
            paper_list = soup.find_all('div', id=id_name)[0].find_all('li', class_='note')
            paper_tppe = False

        create_web(paper_list,socre_thre, driver_child, conference_name,keyword_list, id_name, paper_tppe)



