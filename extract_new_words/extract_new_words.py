from smoothnlp.algorithm.phrase import extract_phrase
import pickle
import os

root_dir = "../baidu_academy/data/"
files = [f for f in os.listdir(root_dir) if not f.startswith('.')]
aggregated_list = []
for each in files:
	aggregated_list.append(pickle.load(open(root_dir + each, 'rb')))

corpus = []
for each_file in aggregated_list:
	for each in each_file:
		corpus.append(each["title"])
		corpus.append(each["abstract"])
		corpus.append(each["keyword"])

result = extract_phrase(corpus,100,10,2,4,1)
print(result)