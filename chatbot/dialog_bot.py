from transformers import AutoTokenizer, AutoModel
import torch
import argparse
import json
import sys
from ltp import LTP
from elasticsearch import Elasticsearch
es = Elasticsearch()

dsl = {
    'query': {
        'match': {
            'name': ''
        }
    }
}

tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")  
model = AutoModel.from_pretrained("bert-base-chinese")

def infobox_to_string(infobox):
	string = "\n"
	for each in infobox:
		string += each["key"] + "\t" + each["value"] + "\n"
	return string

def cos_sim(v1, v2):
	return v1.dot(v2) / torch.norm(v1) / torch.norm(v2)

def read_json(filename):
	faq = []
	with open(filename, 'r') as f:
		for line in f:
			data = json.loads(line.lower().strip())
			faq.append(data)
			# print(data)
			# es.index(index='baidubaike', body=data)
	return faq

def calculate_embedding(filename):
	name_embeddings = []
	faq = read_json(filename)
	tokenized = [tokenizer(each['name']) for each in faq]
	i = 0
	for each in tokenized:
		result = model(torch.tensor(each['input_ids']).unsqueeze(0), \
		torch.tensor(each['attention_mask']).unsqueeze(0))[0].squeeze(0).max(dim=0)
		name_embeddings.append(result[0])
		i += 1
		if i % 100 == 0:
			print(str(i) + " out of " + str(len(tokenized)) + " have been calculated")
	torch.save(name_embeddings, 'name_embeddings.pt')
	return name_embeddings

def remove_stop(tok, stopwords):
	to_be_deleted = set()
	for each in tok:
		if each in stopwords:
			to_be_deleted.add(each)
	s = []
	for each in tok:
		if each not in to_be_deleted:
			s.append(each)
	return s

def search(query, faq):
	for each in faq:
		if query == each['name']:
			return each
	return None

def esearch(s):
	dsl['query']['match']['name'] = s
	results = es.search(body=dsl)['hits']['hits']
	return [each['_source']['name'] for each in results]

def print_info(i, faq):
	if "abs" in faq[i]:
		print()
		print("你说的是" + faq[i]['name'] + "吗？")
		print(faq[i]["abs"])
		if "infobox" in faq[i]:
			print(infobox_to_string(faq[i]['infobox']))
		print()
	else:
		print()
		print("你说的是" + faq[i]['name'] + "吗？")
		print("笨笨也不知道呢。。。。。。要不你自己查一下？？")
		print()

if __name__ == '__main__':

	parser = argparse.ArgumentParser('Chatbot System')
	parser.add_argument(
        '--gpu',
        type=int,
        default=None,
        help='gpu to run on')
	parser.add_argument(
        '--model_file',
        type=str,
        default=None,
        help='all the preprocessed queries')
	parser.add_argument(
        '--json_file',
        type=str,
        default=None,
        help='crawled from the web')
	args = parser.parse_args()
	parser.add_argument(
        '--stop_words',
        type=str,
        default='stopwords/hit_stopwords.txt',
        help='file containing the stop words')
	args = parser.parse_args()
	stopwords = set()
	with open(args.stop_words, 'r') as f:
		for line in f:
			stopwords.add(line.strip())
	ltp = LTP()

	faq = read_json("baidu.json")
	inp = input("你好呀我是笨笨，我知道所有关于计算机的词语哦，有什么问题都可以问我哦！～\n").lower()
	seg, hidden = ltp.seg([inp])
	seg = seg[0]
	tok = "".join(remove_stop(seg, stopwords))
	name_embeddings = torch.load(args.model_file) if args.model_file else calculate_embedding(args.json_file)

	while inp != "exit":

		r = search(tok, faq)

		if r:
			print()
			print("你说的是" + r['name'] + "吗？")
			if 'abs' in r:
				print(r["abs"])
			if "infobox" in r:
				print(infobox_to_string(r['infobox']))
			print()

		else:
			result = esearch(tok)
			tmp = tokenizer(tok)
			sent_embed = model(torch.tensor(tmp['input_ids']).unsqueeze(0), \
				torch.tensor(tmp['attention_mask']).unsqueeze(0))[0].squeeze(0).max(dim=0)[0]
			sim = torch.tensor([cos_sim(each, sent_embed) for each in name_embeddings])
			best_match = torch.argsort(sim, descending=True)[:2]
			best_match_name = [faq[each]['name'].lower() for each in best_match]
			not_found = True
			for idx, each in enumerate(best_match_name):
				if each in result:
					not_found = False
					print_info(best_match[idx].item(), faq)
					break
			if not_found:
				print_info(best_match[0].item(), faq)


		inp = input("你好呀我是笨笨，我知道所有关于计算机的词语哦，有什么问题都可以问我哦！～\n")
		seg, hidden = ltp.seg([inp])
		seg = seg[0]
		tok = "".join(remove_stop(seg, stopwords))
	print("拜拜👋，想我了就来找我哦～")





