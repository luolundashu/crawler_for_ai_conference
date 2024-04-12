import requests
from bs4 import BeautifulSoup
import os
import time
from tqdm import tqdm
import re
from lxml import html
from lxml import html
def contains_keyword(keyword, text):
    return keyword.lower() in text.lower()

def remove_symbols(input_string):
    # 使用正则表达式去除特定符号，保留连字符（-）
    cleaned_string = re.sub(r'[^\w\s-]', '', input_string)
    return cleaned_string


def create_web(paper_name,paper_pdf,conference_name,paper_year_dic,key_word,patience=20):

    paper_name =paper_name.a.text.replace('\n','')
    paper_pdf =paper_pdf.a['href']
    if contains_keyword(key_word, paper_name):
        if paper_name not in paper_year_dic['{}'.format(conference_name[-4:])]:
            return
        pdf_web = 'https://www.ecva.net/{}'.format(paper_pdf) #eccv_2022


        paper_dir_father = './paper/{}/{}'.format(conference_name,key_word)
        if os.path.exists(paper_dir_father) is not True:
            os.makedirs(paper_dir_father)
        for pat in range(patience):
            response = requests.get(pdf_web)
            if response.status_code == 200:
                with open("{}/{}.pdf".format(paper_dir_father,remove_symbols(paper_name)), "wb") as pdf_file:
                    pdf_file.write(response.content)
                break
            else:
                print('第{}次尝试写入,地址{}'.format(pat,pdf_web))
                if pat==patience-1:
                    print('{}为写入失败，网址{}'.format(pat,pdf_web))
                    continue
    return paper_name


if  __name__ =='__main__':
    os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890"
    os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890"

    key_word_list=['patch','Anomaly Detection']
    conference_name_list=['ECCV2022','ECCV2020'] #目前可选ICCV CVPR WACV

    for conference_name in conference_name_list:
        response = requests.get('https://www.ecva.net/papers.php')
        soup = BeautifulSoup(response.content, "html.parser")
        root = html.fromstring(str(soup))

        paper_year_dic ={}
        for i in range(3):
            papers = root.xpath('/html/body/main/div[2]/div[{}]'.format(i+1))[0].text_content()
            years = str(root.xpath('/html/body/main/div[2]/comment()[{}]'.format(i+2))[0])[10:14]
            paper_year_dic['{}'.format(years)]=papers

        paper_name_list =soup.find_all('dt', class_='ptitle')
        paper_pdf_list = soup.find_all('dd')[1::2]
        for key_word in key_word_list:
            for i in tqdm(range(len(paper_name_list))):

                name = create_web(paper_name_list[i],paper_pdf_list[i],conference_name,paper_year_dic ,key_word)
                tqdm.write('会议{}__关键词{}__{}/{}分析完成'.format(conference_name,key_word,i,len(paper_name_list)))
