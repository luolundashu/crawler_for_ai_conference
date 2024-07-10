import requests
from bs4 import BeautifulSoup
import os
import time
from tqdm import tqdm
import re

from lxml import html
def contains_keyword(keyword, text):
    return keyword.lower() in text.lower()

def remove_symbols(input_string):
    # 使用正则表达式去除特定符号，保留连字符（-）
    cleaned_string = re.sub(r'[^\w\s-]', '', input_string)
    return cleaned_string

def create_web(web,conference_name,key_word_list):
    web = web.find('a')['href']
    parts = web.split('/')
    name = parts[-1].split('.')[0]
    web = 'https://openaccess.thecvf.com/content/{}/papers/{}.pdf'.format(conference_name,name)
    name = name.split('_')[1:-1]
    name = ' '.join(name)

    for key_word in key_word_list:
        paper_dir_father = './paper/{}/{}'.format(conference_name,key_word)
        if os.path.exists(paper_dir_father) is not True:
            os.makedirs(paper_dir_father)
        if contains_keyword(key_word, name):
            #response = requests.get(web,verify=False)
            for pat in range(20):
                try:
                    response = requests.get(web)
                    with open("{}/{}.pdf".format(paper_dir_father,name), "wb") as pdf_file:
                        pdf_file.write(response.content)
                        time.sleep(3)
                    break
                except:
                    print('请求失败，暂停100秒')
                    time.sleep(100)
                    pass
    #return name




def create_eccv_web(paper_name,paper_pdf,conference_name,paper_year_dic,key_word_list,patience=20):

    paper_name =paper_name.a.text.replace('\n','')
    paper_pdf =paper_pdf.a['href']
    for key_word in key_word_list:
        if contains_keyword(key_word, paper_name):
            if paper_name not in paper_year_dic['{}'.format(conference_name[-4:])]:
                return
            pdf_web = 'https://www.ecva.net/{}'.format(paper_pdf) #eccv_2022


            paper_dir_father = './paper/{}/{}'.format(conference_name,key_word)
            if os.path.exists(paper_dir_father) is not True:
                os.makedirs(paper_dir_father)

            for pat in range(patience):
                try:
                    response = requests.get(pdf_web)
                    with open("{}/{}.pdf".format(paper_dir_father, remove_symbols(paper_name)), "wb") as pdf_file:
                        pdf_file.write(response.content)
                        time.sleep(3)
                    break
                except:
                    print('请求失败，暂停100秒')
                    time.sleep(100)
                    pass

    #return paper_name

if  __name__ =='__main__':
    os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890"
    os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890"

    key_word_list=['unmixing','self']#'Diffusion','Time Series','Bayesian','Out of Distribution'
    conference_name_list=['CVPR2024'] #目前可选ICCV CVPR WACV

    for conference_name in conference_name_list:
        if 'ECCV' not in conference_name:
            if 'WACV' in conference_name:
                url = "https://openaccess.thecvf.com/{}".format(conference_name)
            else:
                url = "https://openaccess.thecvf.com/{}?day=all".format(conference_name)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            paper_group = soup.body.find_all("div",recursive=False)[2].dl
            paper_name_all = paper_group.find_all('dt')
            lenth_web=len(paper_name_all)

            #for key_word in key_word_list:
            for i in tqdm(range(lenth_web)):
                create_web(paper_name_all[i],conference_name,key_word_list)
                tqdm.write('会议{}__{}/{}分析完成'.format(conference_name,i,lenth_web))


        elif 'ECCV' in conference_name:
            response = requests.get('https://www.ecva.net/papers.php')
            soup = BeautifulSoup(response.content, "html.parser")
            root = html.fromstring(str(soup))

            paper_year_dic = {}
            for i in range(3):
                papers = root.xpath('/html/body/main/div[2]/div[{}]'.format(i + 1))[0].text_content()
                years = str(root.xpath('/html/body/main/div[2]/comment()[{}]'.format(i + 2))[0])[10:14]
                paper_year_dic['{}'.format(years)] = papers

            paper_name_list = soup.find_all('dt', class_='ptitle')
            paper_pdf_list = soup.find_all('dd')[1::2]

            for i in tqdm(range(len(paper_name_list))):
                create_eccv_web(paper_name_list[i], paper_pdf_list[i], conference_name, paper_year_dic, key_word_list)
                tqdm.write(
                    '会议{}__{}/{}分析完成'.format(conference_name, i, len(paper_name_list)))


