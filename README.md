## New Word Extraction

This repo will consist of three parts:

1. Codes for crawling papers' abstract, keyword, authors, titles from [Baidu Academic](https://xueshu.baidu.com) using a user defined query, forked from [this website](https://github.com/eveningqn/baiduSpider) with some modifications
2. Codes to extract new words from all the information we got from last step(Need Tuning)
3. Dialog bot to explain the new words(To be done)



There should be a `data/` folder where the crawled files will be stored in `.pkl` format.

Requirements:

`selenium == 3.141.0`

`urllib3 == 1.24.3`

`openpyxl == 3.0.5`

`smoothNLP ==0.4.0`

and also a chrome web driver will be needed



You can construct your own `queries.xlsx` to crawl specific website you would like to, just follow the format below:



You can construct this with `openpyxl` automatically by just construct a list 

```python3
from openpyxl import load_workbook,Workbook
wb = Workbook()
sheet = wb.active
sheet.title = "Sheet1"
terms = ["computer architecture", "Software Engineering"]
for each in terms:
	url = "https://xueshu.baidu.com/s?wd=" + each
	sheet.append([each, url])

wb.save(r'queries.xlsx')
```

Please note that there should not be any blank rows. The URLs could be set with a filter by copying the URLs from your browser.



Usage:

To crawl [Baidu Academic](https://xueshu.baidu.com), Run `python3 baidySpider.py`

To extract new words from the data, run `python3 extract_new_words.py`. You will need to prepare a word list to filter out some of the words are not newly invented, of course, you are free to delete the filtering procedure.