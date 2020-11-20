import re
import json

with open("baidu.json", 'r') as fr:
	with open("baidu_cleaned.json", 'w') as fw:
		for line in fr:
			data = json.loads(line.strip())
			if 'abs' in data:
				data['abs'] = re.sub(r'\[[0-9]*\]', "", data['abs'])
			json.dump(data, fw, ensure_ascii=False)
			fw.write("\n")
