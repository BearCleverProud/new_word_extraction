from transformers import AutoTokenizer, AutoModel
import torch
import argparse
import json
import sys


tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")  
model = AutoModel.from_pretrained("bert-base-chinese")

def infobox_to_string(infobox):
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
			faq.append(json.loads(line))
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

	faq = read_json("baidu.json")
	inp = input("你好呀我是笨笨，我知道所有关于计算机的词语哦，有什么问题都可以问我哦！～\n")
	name_embeddings = torch.load(args.model_file) if args.model_file else calculate_embedding(args.json_file)
	while inp != "exit":
		tmp = tokenizer(inp)
		sent_embed = model(torch.tensor(tmp['input_ids']).unsqueeze(0), \
			torch.tensor(tmp['attention_mask']).unsqueeze(0))[0].squeeze(0).max(dim=0)[0]
		sim = torch.tensor([cos_sim(each, sent_embed) for each in name_embeddings])
		best_match = torch.argmax(sim).item()

		if "abs" in faq[best_match]:
			print("你说的是这个吗？" + faq[best_match]['name'])
			print(faq[best_match]["abs"])
			if "infobox" in faq[best_match]:
				print(infobox_to_string(faq[best_match]['infobox']))
			print()
		else:
			print("你说的是这个吗？" + faq[best_match]['name'])
			print("笨笨也不知道呢。。。。。。要不你自己查一下？？")
			print()
		inp = input("你好呀我是笨笨，我知道所有关于计算机的词语哦，有什么问题都可以问我哦！～\n")
	print("拜拜👋，想我了就来找我哦～")





