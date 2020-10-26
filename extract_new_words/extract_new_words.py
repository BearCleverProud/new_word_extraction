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

result = extract_phrase(corpus,20,200,2,7,20)
print("Original new word count:" + str(len(result)))
all_words = set(pickle.load(open("all_words.pkl", "rb")))
print(result)
filtered_words = []
for each in result:
	if each not in all_words:
		filtered_words.append(each)
print("filtered new word count:" + str(len(filtered_words)))
print(filtered_words)