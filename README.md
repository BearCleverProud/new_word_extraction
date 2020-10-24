## New Word Extraction

This repo will consist of three parts:

1. Codes for crawling papers' abstract, keyword, authors, titles from [Baidu Academic](https://xueshu.baidu.com) using a user defined query, forked from [this website](https://github.com/eveningqn/baiduSpider) with some modifications
2. Codes to extract new words from all the information we got from last step(To be done)
3. Dialog bot to explain the new words(To be done)



There should be a `data/` folder where the crawled files will be stored in `.pkl` format.

Requirements:

`selenium == 3.141.0`

`urllib3 == 1.24.3`

`openpyxl == 3.0.5`

and also a chrome web driver will be needed



You can construct your own `queries.xlsx` to crawl specific website you would like to, just follow the format below:



You can construct this with `openpyxl` automatically by 

`from openpyxl import load_workbook,Workbook`

`wb = Workbook()
sheet = wb.active
sheet.title = "Sheet1"`

`a = ["computer architecture", "https://xueshu.baidu.com/s?wd=computer+architecture&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=3&rsv_sug2=0&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_n=1&rsp=0"]`

`wb.save(r'queries.xlsx')`

Please note that there should not be any blank rows. The URLs could be set with a filter by copying the URLs from your browser.



Usage:

To crawl [Baidu Academic](https://xueshu.baidu.com), Run `python3 baidySpider.py`