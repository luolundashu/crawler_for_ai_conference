import requests
from bs4 import BeautifulSoup
import os
import time
from tqdm import tqdm

def contains_keyword(keyword, text):
    return keyword.lower() in text.lower()

def create_web(web,conference_name,key_word):
    web = web.find('a')['href']
    parts = web.split('/')
    name = parts[-1].split('.')[0]
    web = 'https://openaccess.thecvf.com/content/{}/papers/{}.pdf'.format(conference_name,name)
    print('{}正在下载'.format(conference_name))
    name = name.split('_')[1:-1]
    name = ' '.join(name)


    paper_dir_father = './paper/{}/{}'.format(conference_name,key_word)
    if os.path.exists(paper_dir_father) is not True:
        os.makedirs(paper_dir_father)

    if contains_keyword(key_word, name):
        response = requests.get(web)
        with open("{}/{}.pdf".format(paper_dir_father,name), "wb") as pdf_file:
            pdf_file.write(response.content)
            time.sleep(1)
    return name


if  __name__ =='__main__':
    os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890"
    os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890"

    key_word_list=['Anomaly Detection','Time Series','Bayesian','Out of Distribution','Diffusion']
    conference_name_list=['ICCV2019'] #目前可选ICCV CVPR WACV

    for conference_name in conference_name_list:


        if 'WACV' in conference_name:
            url = "https://openaccess.thecvf.com/{}".format(conference_name)
        else:
            url = "https://openaccess.thecvf.com/{}?day=2019-11-01".format(conference_name)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        paper_group = soup.body.find_all("div",recursive=False)[2].dl
        paper_name_all = paper_group.find_all('dt')
        lenth_web=len(paper_name_all)

        for key_word in key_word_list:
            for i in tqdm(range(lenth_web)):
                name = create_web(paper_name_all[i],conference_name,key_word)
                tqdm.write('会议{}__关键词{}__{}/{}分析完成'.format(conference_name,key_word,i,lenth_web))
