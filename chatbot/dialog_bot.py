from transformers import AutoTokenizer, AutoModel
import torch
import argparse
import json
import sys
from ltp import LTP
# from elasticsearch import Elasticsearch

# es = Elasticsearch()
ltp = LTP()
tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")  
model = AutoModel.from_pretrained("bert-base-chinese")

dsl = {
    'query': {
        'match': {
            'name': ''
        }
    }
}

class ChatBot:
	def __init__(self, json_file, model_file):
		super(ChatBot, self).__init__()
		self.faq = read_json(json_file)
		self.name_embeddings = torch.load(model_file)
		self.stopwords = set()
		with open("stopwords/hit_stopwords.txt", 'r') as f:
			for line in f:
				self.stopwords.add(line.strip())

	def get_res(self, msg):
		seg, hidden = ltp.seg([msg])
		seg = seg[0]
		tok = "".join(remove_stop(seg, self.stopwords))
		r = search(tok, self.faq)
		s = ""

		if r:
			s += "\n"
			s += "你说的是" + r['name'] + "吗？\n"
			if 'abs' in r:
				s += r["abs"]
			if "infobox" in r:
				s += infobox_to_string(r['infobox'])
			s += "\n"
			return s

		else:
			tmp = tokenizer(tok)
			sent_embed = model(torch.tensor(tmp['input_ids']).unsqueeze(0), \
				torch.tensor(tmp['attention_mask']).unsqueeze(0))[0].squeeze(0).max(dim=0)[0]
			sim = torch.tensor([cos_sim(each, sent_embed) for each in self.name_embeddings])
			best_match = torch.argsort(sim, descending=True)
			return return_s(best_match[0].item(), self.faq)

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

# def esearch(s):
# 	dsl['query']['match']['name'] = s
# 	results = es.search(body=dsl)['hits']['hits']
# 	return [each['_source']['name'] for each in results]

def return_s(i, faq):
	s = ""
	if "abs" in faq[i]:
		s += "\n"
		s += "你说的是" + faq[i]['name'] + "吗？\n"
		s += faq[i]["abs"]
		if "infobox" in faq[i]:
			s += infobox_to_string(faq[i]['infobox'])
		s += "\n"
	else:
		s += "\n"
		s += "你说的是" + faq[i]['name'] + "吗？\n"
		s += "笨笨也不知道呢。。。。。。要不你自己查一下？？"
		s += "\n"
	return s

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
        default='name_embeddings.pt',
        help='all the preprocessed queries')
	parser.add_argument(
        '--json_file',
        type=str,
        default='baidu.json',
        help='crawled from the web')
	args = parser.parse_args()
	parser.add_argument(
        '--stop_words',
        type=str,
        default='stopwords/hit_stopwords.txt',
        help='file containing the stop words')
	args = parser.parse_args()

	bot = ChatBot(args.json_file, args.model_file)
	inp = input("你好呀我是笨笨，我知道所有关于计算机的词语哦，有什么问题都可以问我哦！～\n").lower()
	while inp != "exit":
		print(bot.get_res(inp))
		inp = input("你好呀我是笨笨，我知道所有关于计算机的词语哦，有什么问题都可以问我哦！～\n")
	print("拜拜👋，想我了就来找我哦～")






