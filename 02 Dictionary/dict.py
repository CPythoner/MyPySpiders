# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 2017

@author: WangQiang
"""

import urllib.request
from bs4 import BeautifulSoup
from colorama import init,Fore

init(autoreset=True)
root_url = 'http://www.iciba.com/'

while True:
	word = input('请输入想要查询的单词（或"q"退出）：\n')
	if word == 'q':
		break
	else:
		url = root_url +  urllib.parse.quote(word)	# 解决url中带有中文编译失败的问题
		response = urllib.request.urlopen(url)

		html = response.read()
		soup = BeautifulSoup(html, 'lxml')

		tag_soup = soup.find(class_='base-list switch_part')

		if tag_soup == None:	# 防止输入的单词没有释义
			print(Fore.GREEN + '输入的单词不存在，重新输入.')
		else:
			meanings = tag_soup.find_all(class_='clearfix')
			for i in range(len(meanings)):
				translation = meanings[i].get_text()
				print(Fore.CYAN + translation.strip())	# 去掉字符串开头和结尾的空行
				print(Fore.RED + '='*30)