import json
import pickle
from openpyxl import load_workbook,Workbook


terms = []
with open("../baidu_academy/ccfpedia_term.json", 'r') as f:
	for line in f:
		content = json.loads(line.strip())
		terms.append(content["name"])


pickle.dump(terms, open("all_words.pkl", "wb"))