from TS_transform import Fast_T2S
import wikipedia

wikipedia.set_lang("zh")
words = []
with open("didnt_find.txt", 'r') as f:
	for line in f:
		words.append(line.strip())

print("finish loading words")

still_not_found = []
with open("wiki.json", "w", encoding="utf-8") as f:

	for each in words:
		try:
			content = wikipedia.page(each)
			content = content.split("\n\n\n")[0]
			json.dump({"name":each, "abs": Fast_T2S(content)}, f, ensure_ascii=False)
			f.write("\n")
			print(each + "has finished")
		except:
			print("didnt find " + each)
			still_not_found.append(each)

with open("still_not_found.txt", 'w') as f:
	for each in still_not_found:
		f.write(each + "\n")