## New Word Extraction

This repo will consist of three parts:

1. Codes for crawling papers' abstract, keyword, authors, titles from [Baidu Academic](https://xueshu.baidu.com) using a user defined query, forked from [this website](https://github.com/eveningqn/baiduSpider) with some modifications
2. Codes to extract new words from all the information we got from last step(Need Tuning)
3. Dialog bot to explain the new words(To be done)



There should be a `data/` folder where the crawled files will be stored in `.pkl` format.

Requirements:

```
selenium == 3.141.0
urllib3 == 1.24.3
openpyxl == 3.0.5
smoothNLP ==0.4.0
ltp == 4.0.10
torch == 1.6.0
elasticsearch == 7.10.0
transformers == 3.3.1
```

You can install it through `pip install -r requirement.txt`, and also a chrome web driver will be needed



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

**Paper Crawling Process**

To crawl papers from [Baidu Academic](https://xueshu.baidu.com), run `python3 baidySpider.py`

**Extract New Words from Crawled Paper**

To extract new words from the data, run `python3 extract_new_words.py`. You will need to prepare a word list to filter out some of the words are not newly invented, of course, you are free to delete the filtering procedure.

**Crawl Explainations from Wikipedia and BaiduBaike**

To crawl [Wikipedia](https://www.wikipedia.org) using the keywords from above procedures, run`python3 crawlwikipedia.py`

To crawl [BaiduBaike](https://baike.baidu.com) using the keywords from above procedures, run`python3 crawlbaidupedia.py`

**Run Dialogue Bot**

You should install and run `elasticsearch` before run the `python` script.

For MaxOS users, we recommend them to use `brew install elasticsearch`, and then type in `elasticsearch` in your command line, then this service will be deployed in your local machine. 

First time run: You want to run `python dialog_bot.py --json_file [yourfile]` to create the model file, which takes a while. The model is the BERT representation of all the keywords. The format of Json file could be found in the file `crawlbaidupedia.py` at `line 51-55`

Then: You will just run by `python dialog_bot.py --model_file [your model]` to interactively chat with the chatbot.

Enjoy chatting!

