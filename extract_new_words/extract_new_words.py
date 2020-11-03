from smoothnlp.algorithm.phrase import extract_phrase
import pickle
import os

root_dir = "../baidu_academy/data/"
files = [f for f in os.listdir(root_dir) if not f.startswith('.')]
aggregated_list = []
for each in files:
	aggregated_list.append(pickle.load(open(root_dir + each, 'rb')))

corpus = []
keywords = []
for each_file in aggregated_list:
	for each in each_file:
		corpus.append(each["title"])
		corpus.append(each["abstract"])
		keywords.extend(each["keyword"].split())
keywords = set(keywords)
result = set(extract_phrase(corpus,200,200,4,7,20))
print(result)
print("Original new word count: " + str(len(result)))
print("Words from keywords: " + str(len(keywords)))
all_words = set(pickle.load(open("all_words.pkl", "rb")))
filtered_words = []
for each in result:
	if each not in all_words:
		filtered_words.append(each)
keywords_filtered = []
for each in keywords:
	if each not in all_words:
		keywords_filtered.append(each)
print("Filtered new word count: " + str(len(filtered_words)))
print("Filtered from keywords: " + str(len(keywords_filtered)))
with open("words.txt", "w") as f:
	for each in filtered_words + keywords_filtered:
		f.write(each + "\n")
# print(filtered_words)