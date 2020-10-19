## New Word Extraction

This repo will consist of three parts:

1. Codes for crawling papers' abstract, keyword, authors, titles from [Baidu Academic](https://xueshu.baidu.com) using a user defined query, forked from [this website](https://github.com/eveningqn/baiduSpider) with some modifications
2. Codes to extract new words from all the information we got from last step(To be done)
3. Dialog bot to explain the new words(To be done)



You can construct your own `name_list.xlsx` to crawl specific website you would like to, just follow the format, and note that there should not be any blank rows. The URLs could be set with a filter by copying the URLs from your browser.



Usage:

Run `python3 baidySpider.py`