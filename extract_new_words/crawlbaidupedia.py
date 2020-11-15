# -*- coding: utf-8 -*-
import time
import json

from selenium import webdriver

def get_infobox(driver):
	if driver.find_elements_by_class_name("basic-info") == []:
		return {}
	left = driver.find_element_by_class_name("basic-info").find_element_by_class_name("basicInfo-left")
	right = driver.find_element_by_class_name("basic-info").find_element_by_class_name("basicInfo-right")
	left_entry, left_answer = left.find_elements_by_tag_name("dt"), left.find_elements_by_tag_name("dd")
	right_entry, right_answer = right.find_elements_by_tag_name("dt"), right.find_elements_by_tag_name("dd")
	info_box = []
	for entry, answer in zip(left_entry, left_answer):
		info_box.append({"value": answer.text, "key": entry.text})
	for entry, answer in zip(right_entry, right_answer):
		info_box.append({"value": answer.text, "key": entry.text})
	return info_box

def get_subtitles(driver):
	subtitles = {}
	current_level2_title = ""
	for each in driver.find_elements_by_class_name("anchor-list"):
		potential_subtitles = each.find_elements_by_class_name("lemma-anchor")
		if len(potential_subtitles) == 3:
			lemma_anchor = potential_subtitles[2].get_attribute("name")
			subtitles[lemma_anchor] = []
			current_level2_title = lemma_anchor
		elif len(potential_subtitles) == 4:
			lemma_anchor = potential_subtitles[2].get_attribute("name")
			subtitles[current_level2_title].append(lemma_anchor)
	return subtitles

def get_content(driver):
	content = [each.text for each in driver.find_elements_by_class_name("para")]
	for each in driver.find_elements_by_class_name("para"):
		if each.find_elements_by_class_name("lemma-album") == []:
			content.append(each.text.replace("\u3000", " "))
	return content

def get_web_info(driver):
	title = driver.find_element_by_class_name('lemmaWgt-lemmaTitle-title').find_element_by_tag_name("h1").text
	try:
		summary = driver.find_element_by_class_name('lemma-summary').find_elements_by_class_name("para")
		summary = "".join([each.text for each in summary])
		infobox = get_infobox(driver)
		# subtitles = get_subtitles(driver)
		# content = get_content(driver)
		return {"abs": summary, "name": title, "infobox": infobox}
	except:
		return {"name": title}


if __name__ == "__main__":
	words = []
	didnt_find = []
	found = []
	driver = webdriver.Chrome()

	with open("word_reliable.txt", "r") as f:
		for line in f:
			words.append(line.strip())

	with open("baidu.json", "w", encoding="utf-8") as f:

		for each in words:
			url = "https://baike.baidu.com/item/" + each
			driver.get(url)
			if driver.find_elements_by_class_name('wiki-lemma') == []:
				didnt_find.append(each)
				json.dump({"name":each}, f, ensure_ascii=False)
				f.write("\n")
				continue
			found.append(each)
			json.dump(get_web_info(driver), f, ensure_ascii=False)
			f.write("\n")
			time.sleep(2)
	
	driver.close()

	assert len(found) + len(didnt_find) == len(words)
	
	with open("found_words.txt", "w") as f:
		for each in found:
			f.write(each + "\n")
	with open("didnt_find.txt", "w") as f:
		for each in didnt_find:
			f.write(each + "\n")
