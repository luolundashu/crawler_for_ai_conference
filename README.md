News  2024.2.25：
The latest version of the script has been written and can now scrape paper from ICML, ICLR, NeurIPS, CVPR, ICCV, and WACV after continuous debugging. Please update Chrome to the latest version and download the corresponding version of the driver from https://googlechromelabs.github.io/chrome-for-testing/.

To extract papers from iclr, NeurIPS, and icml, run 'new_ml_get_paper.py'. To extract papers from cvpr, iccv, and wacv, run 'cv_get_paper.py'. 

Finally, read more articles and publish more papers.

Welcome to star!











News  2024.2.2：
Due to the recent updates on OpenReview, the web scraper is currently not very effective. I will soon be on winter break and plan to maintain the code during this period, making it more versatile and adaptable.

"This is the first repository I've uploaded, and I'm very excited.

Motivation:
When trying to keep up with top AI conferences, extracting content based on keywords is highly inefficient. So, 
with the intention of creating a tool that allows input of conference names and keywords to automatically extract titles and package them, I wrote this repository.

For users in China, modifying the proxy settings can lead to faster downloads.

How to use:
To extract papers from cvpr, iccv, and wacv, run 'cv_get_paper.py'. You only need to modify the 'key_word_list' and 'conference_name_list'. 
This script scrapes the website: https://openaccess.thecvf.com.

To extract papers from iclr, NeurIPS, and icml, run 'ml_get_paper.py'. You will need to download the Chrome browser and the Chrome driver. 
Modify the 'driver' to the address of your Chrome driver. After that, you only need to modify the 'key_word_list' and 'conference_name_list'.
This script scrapes the website: https://openreview.net."  For papers from other conferences on this website, just make minor modifications to
the URL（the function of crete_url()） and it should work seamlessly.

Finally,Welcome to star on GitHub!

Future word:
Implement downloading based on keywords in the abstract, and enhance download speed.

