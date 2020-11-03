import json
import pickle
from openpyxl import load_workbook,Workbook

wb = Workbook()
sheet = wb.active
sheet.title = "Sheet1"

content = ""
terms = []
with open("ccfpedia_term.json", 'r') as f:
	for line in f:
		content = json.loads(line.strip())
		terms.append(content["name"])
		if content["name"] == "C-RHIP":
			print(content)

# print(terms[20000:21000])
# for each in terms:
# 	url = "https://xueshu.baidu.com/s?wd=" + each + "&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&filter=sc_year%3D%7B2019%2C%2B%7D%28sc_c0%3A%3D%7B36%7D%29&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&bcp=2&sc_hit=1"
# 	sheet.append([each, url])

# wb.save(r'queries.xlsx')
