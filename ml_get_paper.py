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

def create_web(paper_list,conference_name,keyword_list,id_name,paper_tppe,patience=20):
    for key_word in keyword_list:
        paper_dir_father = "./paper/{}/{}/{}/".format(conference_name,id_name,key_word)


        if os.path.exists(paper_dir_father) is not True:
            os.makedirs(paper_dir_father)

        for i in tqdm(range(len(paper_list))):
            if paper_tppe==True:
                paper_name = paper_list[i].text.strip()
            elif paper_tppe==False:
                paper_name = paper_list[i].find('h4').text.strip()
            paper_name = remove_symbols(paper_name)

            if contains_keyword(key_word, paper_name):
                try:
                    paper_down_dir = paper_list[i].find('a', class_='pdf-link')['href']
                except:
                    paper_down_dir = paper_list[i].find('h4').find('a', class_='pdf-link')['href']

                paper_down_dir = 'https://openreview.net{}'.format(paper_down_dir)
                for pat in range(patience):
                    try:
                        response = requests.get(paper_down_dir)
                        with open("{}/{}.pdf".format(paper_dir_father, paper_name), "wb") as pdf_file:
                            pdf_file.write(response.content)
                        break

                    except:
                        print('请求失败，暂停100秒')
                        time.sleep(100)
                        pass




def crete_url(conference_name):
    try:
        if contains_keyword('iclr',conference_name):
            url ='https://openreview.net/group?id=ICLR.cc/{}/Conference'.format(conference_name[-4:])
        elif contains_keyword('icml',conference_name):
            url='https://openreview.net/group?id=ICML.cc/{}/Conference'.format(conference_name[-4:])
        elif contains_keyword('NeurIPS',conference_name):
            url="https://openreview.net/group?id=NeurIPS.cc/{}/Conference".format(conference_name[-4:])
    except:
        print('目前仅支持icml iclr neurips三个会议，更多会议的爬虫仅需简单修改代码即可完成')

    return url


def contains_keyword_list(keyword, text_list):
    for text in text_list:
        if contains_keyword(text,keyword):
            return True

    return False



if __name__ =='__main__':
    keyword_list = ['shot','Diffusion']#['Diffusion','Anomaly Detection','Time Series','Bayesian','Out of Distribution']
    options = Options()
    driver = webdriver.Chrome(service=Service('./chromedriver-win64/chromedriver.exe'), options=options)
    os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890"
    os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890"
    sleep_patience=1
    conference_names = ['ICLR2024','ICLR2023','ICLR2022']

    for conference_name in conference_names:
        url = crete_url(conference_name)

        # 打开目标页面
        driver.get(url)
        time.sleep(3)


        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')
        paper_level = soup.find('div', class_='mobile-full-width').find('ul', class_='nav nav-tabs').find_all('li', role='presentation')
        id_names=[]
        for level in paper_level:
            id_names.append(level.find('a')['aria-controls'])

        for id_name in id_names[:4]:
            if contains_keyword_list(id_name, ["poster","notable", "accept", "oral", "spotlight"]) is not True:
                continue


            button_element_type = driver.find_element(By.XPATH, "//*[@id='notes']/div/div[1]/ul/li/a[@aria-controls='{}']".format(id_name))
            driver.execute_script("window.scrollTo(0, 0);")
            button_element_type.click()
            time.sleep(2)





            for i in range(1000):
                # 获取当前页面的 HTML
                i = i+1
                if i>1:
                    try :
                        try:
                            next_page_button = driver.find_element(By.XPATH,'//*[@id="{}"]/div/div/nav/ul/li/a[text()={}]'.format(id_name,i))
                        except:
                            next_page_button = driver.find_element(By.XPATH,"//*[@id='{}']/nav/ul/li/a[text()='{}']".format(id_name,i))
                        next_page_button.click()
                        time.sleep(2)
                        print('会议：{}__{}加载第{}页'.format(conference_name,id_name,i))

                    except Exception as e:
                        print('*'*20)
                        print('会议：{}__{}加载第{}页'.format(conference_name,id_name,i))
                        print('*'*20)
                        break

                page_content = driver.page_source
                soup = BeautifulSoup(page_content, 'html.parser')



                try:
                    paper_list = soup.find_all('div',id=id_name)[0].find_all('ul', class_='list-unstyled list-paginated')[0].find_all('h4')
                    paper_tppe = True
                except:
                    paper_list = soup.find_all('div',id=id_name)[0].find_all('li',class_='note')
                    paper_tppe = False

                create_web(paper_list,conference_name,keyword_list,id_name,paper_tppe)


