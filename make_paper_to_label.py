import os
import shutil

def contains_keyword(keyword, text):
    return keyword.lower() in text.lower()


def contains_keyword_list(keyword, text_list):
    for text in text_list:
        if contains_keyword(text,keyword):
            return True
    return False

def get_all_files_and_directories(folder_path):
    all_items = os.listdir(folder_path)
    files = []
    directories = []
    for item in all_items:
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            files.append(item)
        elif os.path.isdir(item_path):
            directories.append(item)
    return files, directories

def find_max_paper_dir(conference_dir,keyword):
    _ , paper_type_list = get_all_files_and_directories('./paper/{}'.format(conference_dir))
    max_paper_len = 0
    for paper_type in paper_type_list:
        papers , _ = get_all_files_and_directories('./paper/{}/{}/{}'.format(conference_dir,paper_type,keyword))
        if len(papers) > max_paper_len:
            max_paper_len = len(papers)
            max_paper_type = paper_type
    return max_paper_type



if __name__ =='__main__':
    dir_move='./new_move_paper_dir'
    auto = True
    if auto:
        _,keyword_list = get_all_files_and_directories('./paper/CVPR2023')
    else:
        keyword_list = ['Gaussian'] #['Anomaly Detection','Diffusion','expert','Bayesian','Time Series']
    for keyword in keyword_list:
        dir_mo = '{}/{}'.format(dir_move,keyword)
        if os.path.exists(dir_mo) is not True:
            os.makedirs(dir_mo)

        _,conference_list = get_all_files_and_directories('./paper')

        for conference_dir in conference_list:
            try:
                if contains_keyword_list(conference_dir, ["ICLR", "ICML", "NeurIPS"]) is True:
                    max_paper_type = find_max_paper_dir(conference_dir,keyword)
                    paper_list, _ = get_all_files_and_directories('./paper/{}/{}/{}'.format(conference_dir,max_paper_type,keyword))
                    for paper in paper_list:
                        shutil.copy('./paper/{}/{}/{}/{}'.format(conference_dir,max_paper_type, keyword, paper), dir_mo)
                else:
                    paper_list,_ = get_all_files_and_directories('./paper/{}/{}'.format(conference_dir,keyword))
                    for paper in paper_list:
                        shutil.copy('./paper/{}/{}/{}'.format(conference_dir, keyword, paper), dir_mo)
            except:
                continue

