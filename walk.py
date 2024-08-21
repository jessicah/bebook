#!/usr/bin/env python3

from bs4 import BeautifulSoup
from bs4.builder import XMLParsedAsHTMLWarning
import warnings
import re
import sys

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

def text(node):
	return ''.join(node.strings).strip()

def walk(node, depth):
	if not hasattr(node, 'children'):
		return
	if depth == 8:
		return
	
	classes = []
	title = ''

	if node.has_attr('class'):
		classes = node['class']
		if 'titlepage' in classes:
			title = text(node)

	print(' ' * (depth * 3), node.name, classes, title)
	for child in node.children:
		walk(child, depth + 1)

def main():
	with open(sys.argv[1]) as file:
		soup = BeautifulSoup(file, 'lxml')

	print(f'Processing {sys.argv[1]}...')

	walk(soup.select_one('body > div.section'), 0)

if __name__ == "__main__":
	main()
