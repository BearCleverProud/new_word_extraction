# -*- coding: utf-8 -*-
import time
import json

from selenium import webdriver

def get_info_box(driver):
	if driver.find_elements_by_class_name("basic-info") == []:
		return {}
	left = driver.find_element_by_class_name("basic-info").find_element_by_class_name("basicInfo-left")
	right = driver.find_element_by_class_name("basic-info").find_element_by_class_name("basicInfo-right")
	left_entry, left_answer = left.find_elements_by_tag_name("dt"), left.find_elements_by_tag_name("dd")
	right_entry, right_answer = right.find_elements_by_tag_name("dt"), right.find_elements_by_tag_name("dd")
	info_box = {}
	for entry, answer in zip(left_entry, left_answer):
		info_box[entry.text] = answer.text
	for entry, answer in zip(right_entry, right_answer):
		info_box[entry.text] = answer.text
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
	summary = driver.find_element_by_class_name('lemma-summary').find_elements_by_class_name("para")
	summary = [each.text for each in summary]
	info_box = get_info_box(driver)
	subtitles = get_subtitles(driver)
	content = get_content(driver)
	return title, summary, info_box, subtitles, content


if __name__ == "__main__":
	words = []
	didnt_find = []
	found = []
	driver = webdriver.Chrome()


	with open("words.txt", "r") as f:
		for line in f:
			words.append(line.strip())

	with open("baidu.json", "w", encoding="utf-8") as f:


		for each in words:
			url = "https://baike.baidu.com/item/" + each
			driver.get(url)
			if driver.find_elements_by_class_name('wiki-lemma') == []:
				didnt_find.append(each)
				continue
			found.append(each)
			json.dump(get_web_info(driver), f, ensure_ascii=False)
			f.write("\n")
			time.sleep(2)

	driver.close()
