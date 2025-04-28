**Start Use！**  **Start Use！**  **Start Use！**

**First Please update Chrome to the latest version and download the corresponding version of the driver from https://googlechromelabs.github.io/chrome-for-testing/.**

**Please note that it is the chromedriver. See the image below**

![image](https://github.com/user-attachments/assets/13a68c41-a290-408e-80da-b1cfb222b258)

**You need to modify the proxy port in the code to your own proxy port, as shown below.**

![image](https://github.com/user-attachments/assets/d5774651-7da3-4e55-baae-e2ff1f7e27c5)

To extract papers from **ICLR, NeurIPS, and ICML**, run '**ml_get_paper.py**'. 

To extract papers from **CVPR, ICCV, ECCV and WACV**, run '**cv_get_paper.py**'. 

If you want to view high-scoring papers from ICLR, run '**get_iclr_pre.py**

After using a crawler to fetch PDFs, you can also use the '**make_paper_to_label.py**' script to categorize all PDFs according to keywords.

**Finally, read more articles and publish more papers.**

______________________________________________________________________________________________________________________________________________________________________
**News  2024.11.19：**

Add the crawling of ICLR top-ranked papers by average score index.

**News  2024.7.10：**


This update change the crawling logic to make it faster!!!


**News  2024.6.6：**

This update has enhanced the stability of web scraping!



**News  2024.4.12：**


The conference crawler now includes support for **ECCV**.

The crawler now supports the three major computer vision conferences **(CVPR, ICCV, ECCV)** and the three major machine learning conferences **(NeurIPS, ICML, ICLR)**.

To extract papers from **ICLR, NeurIPS, and ICML**, run '**ml_get_paper.py**'. 

To extract papers from **CVPR, ICCV, ECCV, and WACV**, run '**cv_get_paper.py**'. 

______________________________________________________________________________________________________________________________________________________________________

**News  2024.2.25：**

The latest version of the script has been written and can now crawl paper from ICML, ICLR, NeurIPS, CVPR, ICCV, and WACV after continuous debugging. **Please update Chrome to the latest version and download the corresponding version of the driver from https://googlechromelabs.github.io/chrome-for-testing/.**

To extract papers from ICLR, NeurIPS, and ICML, run '**ml_get_paper.py**'. 
To extract papers from CVPR, ICCV, and WACV, run '**cv_get_paper.py**'. 

After using a crawler to fetch PDFs, you can also use the '**make_paper_to_label.py**' script to categorize all PDFs according to keywords.

**Finally, read more articles and publish more papers.**

Welcome to star!

______________________________________________________________________________________________________________________________________________________________________










**News  2024.2.2：**
Due to the recent updates on OpenReview, the web scraper is currently not very effective. I will soon be on winter break and plan to maintain the code during this period, making it more versatile and adaptable.


______________________________________________________________________________________________________________________________________________________________________


**"This is the first repository I've uploaded, and I'm very excited.**

**Motivation:**
When trying to keep up with top AI conferences, extracting content based on keywords is highly inefficient. So, 
with the intention of creating a tool that allows input of conference names and keywords to automatically extract titles and package them, I wrote this repository.

For users in China, modifying the proxy settings can lead to faster downloads.

**How to use:**
To extract papers from cvpr, iccv, and wacv, run 'cv_get_paper.py'. You only need to modify the 'key_word_list' and 'conference_name_list'. 
This script scrapes the website: https://openaccess.thecvf.com.

To extract papers from iclr, NeurIPS, and icml, run 'ml_get_paper.py'. You will need to download the Chrome browser and the Chrome driver. 
Modify the 'driver' to the address of your Chrome driver. After that, you only need to modify the 'key_word_list' and 'conference_name_list'.
This script scrapes the website: https://openreview.net."  For papers from other conferences on this website, just make minor modifications to
the URL（the function of crete_url()） and it should work seamlessly.

Finally,Welcome to star on GitHub!

______________________________________________________________________________________________________________________________________________________________________

**Future word:**
Implement downloading based on keywords in the abstract, and enhance download speed(**Because I am not familiar with distributed crawling, this is quite challenging for me and it might not be updated in the future.**).

