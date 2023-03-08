#!/usr/bin/env python3

from bs4 import BeautifulSoup
from bs4.builder import XMLParsedAsHTMLWarning
import warnings
import re
import sys
import urllib.request
import shutil
import os.path
from sty import fg

import nodes

reset = fg.rs

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

# Regular Expressions for transforms
combine_ws = re.compile(r'\s+')
function_re = re.compile(r'([a-zA-Z0-9_~]+)\(')
operator_re = re.compile(r'(operator([+\-*\/%^&|~!=<>,()[\]]{1,3}|\s+new|\s+delete))\(')
reference_re = re.compile(r'#([^_]+)_([^_]+)$')
enum_re = re.compile(r'^([A-Z0-9_]+)$')

def text_content(element, clean=True):
	if clean:
		return combine_ws.sub(' ', ''.join(element.strings)).strip()
	else:
		return ''.join(element.strings).strip()

def has_class(element, name):
	return element.has_attr('class') and name in element['class']

def has_all_classes(element, names):
	for name in names:
		if not has_class(element, name):
			return False
	return True

def has_any_classes(element, names):
	for name in names:
		if has_class(element, name):
			return True
	return False

def contains_blocks(element):
	for child in element.children:
		if child.name == 'p':
			return True
		if child.name == 'dl':
			return True
		if child.name == 'pre':
			return True
	return False

class Document:
	def __init__(self, infile, outfile, debugfile):
		with open(infile) as file:
			print(f'Processing {infile} => {outfile}...')
			self.soup = BeautifulSoup(file, 'lxml')
		self.outfile = outfile
		self.debugfile = debugfile
	
	def __str__(self):
		contents = ''
		if self.is_class:
			contents += f':::{{cpp:class}} {self.title}\n:::\n\n'
		
		contents += str(self.section)
		return contents
	
	def add_class_name(self, match):
		return f'{self.title}::{match.group(1)}('
	
	def process(self):
		main = self.soup.select_one('body > div.section')
		self.title = text_content(main.select_one(':scope > div.titlepage'))
		self.is_class = False

		self.section = main_section = nodes.SectionContainer(self.title, 1)
		
		for child in main.children:
			# skip the following...
			if child.name == 'div':
				if has_class(child, 'titlepage'):
					continue
				if has_class(child, 'classheader'):
					self.is_class = True
					continue
			if child.name == 'a' and has_class(child, 'indexterm'):
				continue
			
			# otherwise content to add...
			if child.name == 'div' and has_class(child, 'section'):
				# typically contains sub-sections, which will often
				# be abi-groups
				main_section += self.process_section(child)
			else:
				# generally for non-class pages...
				main_section += self.process_block(child)
	
	# generally grouping of abi-sections... e.g.
	# - Constructor and Destructor
	# - Hook Functions
	# - Member Functions
	def process_section(self, element):
		title = text_content(element.select_one(':scope > div.titlepage'))
		section = nodes.SectionContainer(title, 2)
		for child in element.children:
			if child.name == 'div' and has_class(child, 'section'):
				section += self.process_subsection(child)
			elif child.name == 'div' and has_class(child, 'titlepage'):
				continue
			else:
				section += self.process_block(child)
		return section
	
	# a bunch of blocks with class declarations (fields, methods)
	def process_subsection(self, element):
		title = text_content(element.select_one(':scope > div.titlepage'))
		#print('title:', title)
		needs_abi_group = False
		section = nodes.SectionContainer(title, 3)
		#print('subsection:', title, 'result:', section)

		classes = [
			'constructorsynopsis',
			'destructorsynopsis',
			'methodsynopsis',
			'fieldsynopsis',
			'funcsynopis'
		]

		maybe_enum = element.select_one(':scope > div.titlepage h4.title > a')
		if maybe_enum:
			match = enum_re.search(maybe_enum['id'])
			if match:
				print(fg.li_cyan, 'WARNING: section for enum:', reset, match.group(1))
				section += nodes.Block(f'{{cpp:enumerator}} {match.group(1)}')
				needs_abi_group = True

		for child in element.children:
			if child.name == 'div' and has_class(child, 'titlepage'):
				continue
			elif child.name == 'code' and has_any_classes(child, classes):
				needs_abi_group = True
				section += self.process_declaration(child)
			elif child.name == 'div' and has_class(child, 'synopsisgroup'):
				needs_abi_group = True
				for child_code in child.select(':scope > code'):
					section += self.process_declaration(child_code)
			elif child.name == 'a' and has_class(child, 'indexterm'):
				continue
			else:
				section += self.process_block(child)
		
		if needs_abi_group:
			section.set_directive('{abi-group}', 4)
			section.output_title(False)

		return section
	
	# adds a class name, and removes global keyword
	# doesn't work correctly for fieldsynopsis
	def process_declaration(self, element):
		declaration = text_content(element)

		if has_class(element, 'c'):
			add_class_name = False
		else:
			add_class_name = True

		if declaration.startswith('global') and 'operator' in declaration:
			declaration = declaration[len('global'):].strip()
		elif declaration.endswith('global'):
			declaration = declaration[0:-len('global')].strip()
		else:
			if 'operator' in declaration and add_class_name:
				declaration = operator_re.sub(self.add_class_name, declaration)
			elif add_class_name:
				declaration = function_re.sub(self.add_class_name, declaration)
		
		declaration = declaration.replace(';', '').strip()

		#print('  ', declaration)

		# this should do the right thing... check BMessage
		if has_class(element, 'fieldsynopsis'):
			return nodes.Block(f'{{cpp:member}} {declaration}')
		else:
			return nodes.Block(f'{{cpp:function}} {declaration}')
	
	# not 100% sure on the return type...
	def process_block(self, element):
		if element.name == 'p':
			return f'{self.process_inline(element)}'
		if element.name == 'div' and has_class(element, 'admonition'):
			title = text_content(element.select_one(':scope > div.title'))
			# this is terrible... but works...
			kind = ''.join([cls for cls in element['class'] if cls != 'admonition'])
			
			admonition = nodes.BlockContainer(f'{{admonition}} {title}\n:class: {kind}')
			# what about other children?
			for child in element.select(':scope p'):
				admonition += self.process_block(child)
			return admonition
		if element.name == 'pre':
			if has_class(element, 'cpp'):
				code = nodes.Block('{code} cpp')
			elif has_class(element, 'c'):
				code = nodes.Block('{code} c')
			elif has_class(element, 'screen'):
				code = nodes.Block('{code} sh')
			else:
				print(fg.li_red, 'Unknown code listing:', fg.li_cyan, element['class'], reset)
				code = nodes.Block('{code}')
			code += text_content(element, clean=False)
			return code
		if element.name == 'table':
			num_headers = len(list(element.select(':scope > thead > tr')))
			table = nodes.Table(num_headers)
			for row in element.select('tr'):
				table += nodes.TableRow()
				for column in row.select(':scope > th, :scope > td'):
					if contains_blocks(column):
						cell = nodes.BlockContainer()
						for block in column.children:
							cell += self.process_block(block)
						table += cell
					else:
						table += self.process_inline(column)
			return table
		if element.name == 'ul':
			unordered_list = nodes.UnorderedList()
			for item in element.select(':scope > li'):
				list_item = nodes.ListItem()
				if contains_blocks(item):
					for block in item.children:
						list_item += self.process_block(block)
				else:
					list_item += self.process_inline(item)
				unordered_list += list_item
			return unordered_list
		if element.name == 'ol':
			ordered_list = nodes.OrderedList()
			for index, item in enumerate(element.select(':scope > li'), start=1):
				list_item = nodes.ListItem()
				if contains_blocks(item):
					for block in item.children:
						list_item += self.process_block(block)
				else:
					list_item += self.process_inline(item)
				ordered_list += list_item
			return ordered_list
		
		classes = [
			'mediaobject',
			'orderedlist',
			'informaltable',
			'calloutlist',
		]
		if element.name == 'div' and has_any_classes(element, classes):
			wrapper = nodes.BlockContainer()
			for child in element.children:
				wrapper += self.process_block(child)
			return wrapper
		
		if element.name == 'div' and has_class(element, 'section'):
			title = text_content(element.select_one(':scope > div.titlepage'))
			section = nodes.SectionContainer(title, 4)
			for child in element.children:
				if child.name == 'div' and has_class(child, 'titlepage'):
					continue
				else:
					section += self.process_block(child)
			return section
		
		if element.name == 'img':
			alt_text = None
			if element.has_attr('alt'):
				alt_text = element['alt']
			src = element['src'][2:]
			url = f'https://www.haiku-os.org/legacy-docs/bebook/{src}'
			path = f'./_static/images/{os.path.basename(src)}'
			print(fg.li_magenta, 'img url:', reset, url, 'saved to:', path)
			if not os.path.exists(path):
				with urllib.request.urlopen(url) as response:
					with open(path, 'w+b') as file:
						shutil.copyfileobj(response, file)
			if alt_text is None:
				return nodes.Text(f'![]({path})')
			else:
				return nodes.Text(f'![{alt_text}]({path})')
		
		if element.name == 'dl':
			deflist = nodes.DefinitionList()
			for child in element.select(':scope > dt, :scope > dd'):
				if child.name == 'dt':
					deflist += nodes.DefinitionTerm(self.process_inline(child))
				else:
					defdata = nodes.DefinitionData()						
					if contains_blocks(child):
						for block in child.children:
							defdata += self.process_block(block)
					else:
						defdata += self.process_inline(child)
					deflist += defdata
			return deflist
		
		if element.name == 'a' and has_class(element, 'indexterm'):
			return None

		# for non-class pages, there are a lot of div wrappers

		print(fg.li_red, 'unhandled block:', element.name, reset)
		print(fg.li_cyan, element, reset)
		
		#return self.process_inline(element)
		return nodes.Text()
	
	def process_inline(self, element):
		if not hasattr(element, 'contents'):
			return nodes.Text(element.string.strip())
		
		content = ''
		for child in element.children:
			if not hasattr(child, 'contents'):
				content += child.string
			# elif child.name == 'p':
			# 	content += str(self.process_inline(child)).strip().replace('\n', ' ')
			elif child.name == 'code':
				highlight = None
				is_enum = False
				is_expr = False
				className = ''
				if child.has_attr('class'):
					className = child['class'][0]
				if className == 'methodname':
					highlight = 'hmethod'
				elif className == 'classname':
					highlight = 'hclass'
				elif className == 'parameter':
					highlight = 'hparam'
				elif className == 'varname':
					highlight = 'hparam'
				elif className == 'constant':
					is_enum = True
					enum = text_content(child)
					if enum == 'NULL' or enum == 'true' or enum == 'false':
						is_expr = True
				
				if is_expr:
					content += f'{{cpp:expr}}`{text_content(child)}`'
				elif is_enum:
					content += f'{{cpp:enumerator}}`{text_content(child)}`'
				elif highlight != None:
					content += f'{{{highlight}}}`{text_content(child)}`'
				else:
					content += text_content(child)
			elif child.name == 'a':
				content += self.process_link(child)
			elif child.name == 'span':
				if 'code' in child['class']:
					content += f'`{text_content(child)}`'
				elif 'term' in child['class']:
					for grandchild in child.children:
						if not hasattr(grandchild, 'contents'):
							content += text_content(grandchild)
						elif grandchild.name == 'code' and 'constant' in grandchild['class']:
							# cpp:epxr for `true`, `false`, etc.
							content += f'{{cpp:enumerator}}`{text_content(grandchild)}`'
						else:
							content += text_content(grandchild)
				elif 'type' in child['class']:
					content += f'{{htype}}`{text_content(child)}`'
				elif 'keycap' in child['class']:
					content += f'{{hkey}}`{text_content(child)}`'
				elif has_any_classes(child, ['emphasis', 'italic']):
					content += f'_{self.process_inline(child)}_'
				else:
					print(fg.li_red, 'WARNING:', reset, 'unable to handle span with classes:', fg.li_cyan, child['class'], reset)
					print('    ', text_content(child))
					content += text_content(child)
			# elif child.name == 'div' or child.name == 'table':
			# 	content += '\n'.join(str(self.process_block(child)))
			elif child.name == 'em':
				content += f'_{self.process_inline(child)}_'
			elif child.name == 'acronym':
				# no acronym support in markdown...
				print(fg.li_yellow, 'WARNING: missing acronym support in markdown', reset)
				content += text_content(child)
			elif child.name == 'br':
				content += '\n\n'
			else:
				print(fg.li_red, 'WARNING: unable to handle child of type:', fg.li_cyan, child.name, reset)
				print('    ', child.parent)
				content += text_content(child)
	
		return nodes.Text(content.strip())
	
	def process_link(self, element):
		match = reference_re.search(element['href'])
		ref_type = 'ref'

		code = element.select_one(':scope > code')
		if code is not None:
			if has_class(code, 'methodname'):
				ref_type = 'cpp:func'
			elif has_class(code, 'classname'):
				ref_type = 'cpp:class'
			elif has_class(code, 'constant'):
				ref_type = 'cpp:enumerator'
			elif has_class(code, 'varname'):
				ref_type = 'cpp:var'
			elif has_class(code, 'function'):
				# a global function, perhaps this should be `c:func` instead?
				ref_type = 'cpp:func'
		else:
			span = element.select_one(':scope > span')
			if span is not None:
				if has_class(span, 'type'):
					# don't actually know the specific kind of type here...
					# could be an enum, or a struct, or maybe even a
					# typedef?
					ref_type = 'cpp:any'
				
		content = text_content(element)

		if match and not (code is not None and has_any_classes(code, ['constant', 'varname', 'function'])):
			# if element.has_attr('title') == False:
			# 	print(fg.li_cyan, 'missing title', reset, element)
			# else:
			# 	print(fg.li_green, element['title'], reset)
			ref_class = match.group(1)
			ref_method = match.group(2)
			content_matches = content.replace('()', '') == f'{ref_class}::{ref_method}' or content.replace('()', '') == ref_method
			if ref_method == 'Constructor':
				ref_method = f'{ref_class}()'
			if content_matches:
				if '::' in content:
					return f'{{cpp:func}}`{ref_class}::{ref_method}()`'
				else:
					return f'{{cpp:func}}`~{ref_class}::{ref_method}()`'
			else:
					return f'{{cpp:func}}`{content} <{ref_class}::{ref_method}>`'
		else:
			if ref_type == 'ref':
				print(fg.li_red, 'WARNING:', reset, 'unable to parse reference:', reset, fg.li_green, element, reset)
			return f'{{{ref_type}}}`{content}`'
	
if __name__ == '__main__':
	document = Document(sys.argv[1], sys.argv[2], None)
	document.process()
	#print('document:', document)
	with open(sys.argv[2], 'w') as file:
		print(document, file=file)
