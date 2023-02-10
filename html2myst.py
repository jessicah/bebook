#!/usr/bin/env python3

from bs4 import BeautifulSoup
from bs4.builder import XMLParsedAsHTMLWarning
import warnings
import re
import sys

combine_ws = re.compile(r'\s+')
function_re = re.compile(r'([a-zA-Z0-9_~]+)\(')
operator_re = re.compile(r'(operator[+\-*\/%^&|~!=<>,()[\]]{1,3})\(')
reference_re = re.compile(r'#([^_]+)_([^_]+)')

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

className = ''

def text(elem, clean=True):
	if clean:
		return combine_ws.sub(' ', ''.join(elem.strings)).strip()
	else:
		return ''.join(elem.strings).strip()

def find_class(elem, tagname, cls):
	elem.find(tagname, class_=cls, recursive=False)

def findall_class(elem, name, cls):
	elem.find_all(name, class_=cls, recursive=False)

def has_class(elem, name):
	return elem.has_attr('class') and name in elem['class']

def add_class_name(match):
	return f'{className}::{match.group(1)}('


nodeNames = []

abigroups = []

def process_link(anchor):
	match = reference_re.search(anchor['href'])
	refType = 'ref'

	code = anchor.select_one(':scope > code')
	if code is not None:
		className = code['class'][0]
		if className == 'methodname':
			refType = 'cpp:func'
		elif className == 'classname':
			refType = 'cpp:class'
			
	textContent = text(anchor)

	if match:
		refClass = match.group(1)
		refMethod = match.group(2)
		if '::' in textContent:
			return f'{{cpp:func}}`{refClass}::{refMethod}`'
		else:
			return f'{{cpp:func}}`~{refClass}::{refMethod}`'
	else:
		return f'{{{refType}}}`{textContent}`'

def process_function(code):
	function = text(code)

	if function.startswith('global') and 'operator' in function:
		function = function[len('global'):].strip()
	elif function.endswith('global'):
		function = function[0:-len('global')]
	else:
		function = function_re.sub(add_class_name, function)
		function = operator_re.sub(add_class_name, function)
	
	function = function.replace(';', '')

	return f':::{{cpp:function}} {function}\n:::'

def process_content(node):
	if not hasattr(node, 'contents'):
		# node is text content, return as-is
		return node.string
	
	content = ''
	for child in node.children:
		if not hasattr(child, 'contents'):
			content += child.string
		elif child.name == 'p':
			content += process_content(child).strip().replace('\n', ' ')
		elif child.name == 'code':
			highlight = None
			is_enum = False
			className = '' if not hasattr(child, 'class') else child['class'][0]
			if className == 'methodname':
				highlight = 'hmethod'
			elif className == 'classname':
				highlight = 'hclass'
			elif className == 'parameter':
				highlight = 'hparam'
			elif className == 'constant':
				is_enum = True
			
			if is_enum:
				content += f'{{cpp:enum}}`{text(child)}`'
			elif highlight != None:
				content += f'{{{highlight}}}`{text(child)}`'
			else:
				content += text(child)
		elif child.name == 'a':
			content += process_link(child)
		elif child.name == 'span':
			if 'code' in child['class']:
				content += f'`{text(child)}`'
			elif 'term' in child['class']:
				for grandchild in child.children:
					if not hasattr(grandchild, 'contents'):
						content += text(grandchild)
					elif grandchild.name == 'code' and 'constant' in grandchild['class']:
						content += f'{{cpp:enum}}`{text(grandchild)}`'
					else:
						content += text(grandchild)
			elif 'type' in child['class']:
				content += f'{{htype}}`{text(child)}`'
			elif 'keycap' in child['class']:
				content += f'{{hkey}}`{text(child)}`'
				print('keycap', text(child))
			else:
				print('WARNING: unable to handle span with classes:', child['class'])
				print('    ', text(child))
				content += text(child)
		elif child.name == 'div' or child.name == 'table':
			content += '\n'.join(process_block(child))
		else:
			print('WARNING: unable to handle child of type:', child.name)
			content += text(child)
	
	return content

def process_block(node):
	lines = []
	if (node.name == 'p'):
		lines.append(process_content(node))
	elif node.name == 'div' and has_class(node, 'admonition'):
		title = text(node.select_one(':scope > div.title'))
		kind = ''.join([cls for cls in node['class'] if cls != 'admonition'])
		lines.append(f':::{{admonition}} {title}')
		lines.append(f':class: {kind}')

		for child in node.select(':scope p'):
			lines.append(process_content(child))
		
		lines.append(':::')
	elif node.name == 'pre':
		lines.append(':::{code}')
		lines.append(text(node, clean=False))
		lines.append(':::')
	elif node.name == 'table':
		lines.append(':::{list-table}')
		lines.append('---')
		lines.append('header-rows: 1')
		lines.append('align: left')
		lines.append('widths: auto')
		lines.append('---')
		lines.append('')
		rows = node.select('tr')
		for row in rows:
			lines.append('-')
			lines.append('')
			for column in row.select('th, td'):
				lines.append(f'\t- {process_content(column)}')
				lines.append('')
		lines.append(':::')
	elif node.name == 'ul':
		for item in node.select('li'):
			lines.append(f'- {process_content(item)}')
			lines.append('')
	else:
		lines.append(process_content(node))
	
	return lines

def main():
	global className
	lines = []

	with open(sys.argv[1]) as file:
		soup = BeautifulSoup(file, 'lxml')

	print(f'Processing {sys.argv[1]}...')

	mainSection = soup.select_one('body > div.section')

	className += text(mainSection.select_one(':scope > div.titlepage'))
	lines.append(f':::{{cpp:class}} {className}')
	lines.append(':::')
	lines.append('')
	#print(className)
	lines.append(f'# {className}')

	sections = mainSection.select(':scope > div.section')

	for section in sections:
		sectionName = text(section.select_one(':scope > div.titlepage'))
		#print('  ', sectionName)
		lines.append(f'## {sectionName}')

		for subSection in section.select(':scope > div.section'):
			lines.append('::::{abi-group}\n\n')
			for node in subSection.children:
				# just to figure out node types we're seeing...
				if node.name not in nodeNames:
					nodeNames.append(node.name)
				
				# known children...
				# - div
				#	- admonition (:::{admonition})
				#	- synopsisgroup (group of :::{cpp:function})
				# - p: formatted paragraph content
				# - ul: formatted list
				# - table: (:::{list-table})
				# - code: (:::{cpp:function})
				# - pre: (:::{code})
				if node.name == 'div' and has_class(node, 'titlepage'):
					continue
				elif node.name == 'code':
					#print('	', process_function(node))
					lines.append(process_function(node))
					lines.append('')
				elif node.name == 'div' and has_class(node, 'synopsisgroup'):
					for code in node.select(':scope > code'):
						#print('	', process_function(code))
						lines.append(process_function(code))
					lines.append('')
				else:
					lines.extend(process_block(node))
					lines.append('')
		
			lines.append('::::\n\n')			
			
	#print('\n'.join(lines).replace('\n\n', '\n'))
	with open(sys.argv[2], 'w') as file:
		file.write('\n'.join(lines).replace('\n\n', '\n'))

if __name__ == "__main__":
	main()


