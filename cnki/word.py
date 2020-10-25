import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pickle
#import time

def get_list(find):
    subject = "I138"
    r = requests.post(url="https://search.cnki.com.cn/api/FileterResultApi/ArticleFileter?searchType=MulityTermsSearch&ArticleType=&ReSearch=&ParamIsNullOrEmpty=true&Islegal=false&Content="
                          + find + "&Theme=&Title=&KeyWd=&Author=&SearchFund=&Originate=&Summary=&PublishTimeBegin=&PublishTimeEnd=&MapNumber=&Name=&Issn=&Cn=&Unit=&Public=&Boss=&FirstBoss=&Catalog=&Reference=&Speciality=&Type=&Subject="
                          + subject + "&SpecialityCode=&UnitCode=&Year=&AuthorFilter=&BossCode=&Fund=&Level=&Elite=&Organization=&Order=&Page=&PageIndex=&ExcludeField=Year&ZtCode=&Smarts=")
    #print(r.json())
    initialyear = r.json()[0].get('FilterName')
    if int(initialyear) >= 2019:
        paper_count = r.json()[int(initialyear)-2019].get('ArticleCount')
    #print(paper_count)
    browser = webdriver.Chrome()
    num = 0
    current_page = 185
    newsList = []
    rare = paper_count-20*(current_page-1)
    while num <= rare:
        url = "https://search.cnki.com.cn/Search/ListResult?searchType=MulityTermsSearch&ArticleType=&ReSearch=&ParamIsNullOrEmpty=true&Islegal=false&Content=" \
              + find + "&Theme=&Title=&KeyWd=&Author=&SearchFund=&Originate=&Summary=&PublishTimeBegin=&PublishTimeEnd=&MapNumber=&Name=&Issn=&Cn=&Unit=&Public=&Boss=&FirstBoss=&Catalog=&Reference=&Speciality=&Type=&Subject=" \
              + subject + "&SpecialityCode=&UnitCode=&Year=2019&AuthorFilter=&BossCode=&Fund=&Level=&Elite=&Organization=&Order=1&Page=" \
              + str(current_page) + "&PageIndex=&ExcludeField=&ZtCode=&Smarts="
        # data = urllib.request.urlopen(url).read()
        ##data = requests.post(url=url,verify=False)
        #print(data)
        ##print(data.json())
        # print(Url)
        browser.get(url=url)
        data = browser.page_source
        # data = data.decode("utf-8", "ignore")
        soup = BeautifulSoup(data, "lxml")
        news_list = soup.find_all('p', {"class": "tit clearfix"})
        #print(len(news_list))
        keyword_list = soup.find_all('p', {"class": "info_left left"})
        #print(len(keyword_list))
        k = 0
        for news in news_list:
            #start = time.time()
            newsurl = news.find('a').get("href")
            m = newsurl
            keyword = keyword_list[k]
            k += 1
            #print(keyword)
            if not keyword.find('a'):
                num += 1
                continue
            keyword = keyword.find('a').get("data-key").replace("/", " ")
            #print(keyword)
            newsurl = "http:" + newsurl
            #print(newsurl)
            if newsurl == "http://www.cnki.com.cn/404.htm":
                num += 1
                continue
            if not getPaper(newsurl, browser):
                num += 1
                continue
            title, abstract = getPaper(newsurl, browser)
            #end=time.time()
            #print(end-start)
            num += 1
            #new = [newsurl, title, keyword, abstract]
            newsList.append({"title": title, "abstract": abstract, "keyword": keyword})
            #print(new)
            #newsList.append(new)
        #print(newsList)

        print(current_page)
        if current_page % 2 == 0:
            f = open("newword_0.pkl", "wb+")
            #f.write(pickle.dumps(newsList))
            pickle.dump(newsList, f)
            #newsList = []
        current_page += 1

        '''
        b = datetime.now()  # 获取当前时间
        durn = (b - a).seconds  # 两个时间差，并以秒显示出来
        print(durn)
        '''



def getPaper(Url,browser):
    #data = urllib.request.urlopen(Url).read()
    #data = data.decode("utf-8", "ignore")
    ##data = requests.get(Url)
    browser.get(url=Url)
    #time.sleep(0.5)
    data = browser.page_source
    soup = BeautifulSoup(data, "lxml")
    title = soup.find('h1').get_text()
    #print(title)
    #author = soup.find('div', {"style":"text-align:center; width:740px; height:30px;"}).get_text().replace('  \xa0','')
    #print(author)
    if not soup.find('div', {"style": "text-align:left;word-break:break-all"}):
        return
    abstract = soup.find('div', {"style": "text-align:left;word-break:break-all"}).get_text()[6:]
    #print(abstract)
    return title, abstract

if __name__ == '__main__':
    find = "%E8%AE%A1%E7%AE%97%E6%9C%BA"
    #a = datetime.now()  # 获得当前时间
    get_list(find)