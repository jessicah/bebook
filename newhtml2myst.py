#!/usr/bin/env python3

from bs4 import BeautifulSoup
from bs4.builder import XMLParsedAsHTMLWarning
import warnings
import re
import sys

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

# Regular Expressions for transforms
combine_ws = re.compile(r'\s+')
function_re = re.compile(r'([a-zA-Z0-9_~]+)\(')
operator_re = re.compile(r'(operator([+\-*\/%^&|~!=<>,()[\]]{1,3}|\s+new|\s+delete))\(')
reference_re = re.compile(r'#([^_]+)_([^_]+)')

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

class Item:
	def __init__(self):
		pass
	
	def __str__(self):
		return ''

class Text(Item):
	def __init__(self, content=''):
		# could we do some line wrapping here?
		lines = ['']
		for token in content.replace('\n', ' ').split(' '):
			last = lines[-1]
			if (len(last) + len(token) + 1) > 75:
				lines.append(token)
			else:
				lines[-1] += ' ' + token
		#self.content = content.replace('\n', ' ')
		self.content = '\n'.join(list(map(str.strip, lines)))
	
	def __str__(self):
		return str(self.content)

class Block(Text):
	def __init__(self, directive=None):
		super().__init__()
		if isinstance(directive, tuple):
			self.directive, self.colons = directive
		elif isinstance(directive, str):
			self.directive = directive
			self.colons = ':::'
		else:
			self.directive = None
		self.strip = True
	
	def __str__(self):
		return self.wrap_content()
	
	def __iadd__(self, content):
		if isinstance(content, Text):
			self.content += str(content)
		else:
			self.content += content
		return self
	
	def set_directive(self, directive, colons=3):
		self.directive, self.colons = directive, ':' * colons
	
	def wrap_content(self):
		if self.directive is None:
			return self.content
		else:
			if len(self.content.strip()) == 0:
				return f'{self.colons}{self.directive}\n{self.colons}'
			else:
				return f'{self.colons}{self.directive}\n{self.content}\n{self.colons}'

class BlockContainer(Block):
	def __init__(self, directive=None):
		super().__init__(directive)
		self.blocks = []
	
	def __str__(self):
		self.content = '\n\n'.join([str(block) for block in self.blocks])
		return super().wrap_content()
	
	def __add__(self, others):
		self.blocks.extend(others)
		return self
	
	def __iadd__(self, other):
		self.blocks.append(other)
		return self

class SectionContainer(BlockContainer):
	def __init__(self, title_text, level):
		super().__init__()

		self.title = f'{"#" * level} {title_text}'
		self.add_title = True
	
	def output_title(self, add_title):
		self.add_title = add_title
	
	def __str__(self):
		body = super().__str__()

		if self.add_title:
			return f'{self.title}\n\n{body}'
		else:
			return body

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

		self.section = main_section = SectionContainer(self.title, 1)
		
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
		section = SectionContainer(title, 2)
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
		section = SectionContainer(title, 3)
		#print('subsection:', title, 'result:', section)

		classes = [
			'constructorsynopsis',
			'destructorsynopsis',
			'methodsynopsis',
			'fieldsynopsis',
			'funcsynopis'
		]

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
		
		if declaration.startswith('global') and 'operator' in declaration:
			declaration = declaration[len('global'):].strip()
		elif declaration.endswith('global'):
			declaration = declaration[0:-len('global')].strip()
		else:
			if 'operator' in declaration:
				declaration = operator_re.sub(self.add_class_name, declaration)
			else:
				declaration = function_re.sub(self.add_class_name, declaration)
		
		declaration = declaration.replace(';', '').strip()

		# this should do the right thing... check BMessage
		if has_class(element, 'fieldsynopsis'):
			return Block(f'{{cpp:member}} {declaration}')
		else:
			return Block(f'{{cpp:function}} {declaration}')
	
	# not 100% sure on the return type...
	def process_block(self, element):
		if element.name == 'p':
			return self.process_inline(element)
		if element.name == 'div' and has_class(element, 'admonition'):
			title = text_content(element.select_one(':scope > div.title'))
			# this is terrible... but works...
			kind = ''.join([cls for cls in element['class'] if cls != 'admonition'])
			
			admonition = BlockContainer(f'{{admonition}} {title}\n:class: {kind}')
			# what about other children?
			for child in element.select(':scope p'):
				admonition += self.process_block(child)			
			return admonition
		if element.name == 'pre':
			code = Block('{code}')
			code += text_content(element, clean=False)
			return code
		if element.name == 'table':
			num_headers = len(list(element.select(':scope > thead > tr')))
			directive = [
				'{list-table}',
				'---',
				f'header-rows: {num_headers}',
				'align: left',
				'widths: auto',
				'---'
			]
			directive = '\n'.join(directive)
			table = BlockContainer(f'{directive}')
			for row in element.select('tr'):
				table += '-'
				for column in row.select('th, td'):
					if len(list(column.select(':scope > p'))) == 1:
						table += f'\t- {self.process_block(list(column.children)[0])}'
					else:
						table += f'\t- {self.process_inline(column)}'
			return table
		if element.name == 'ul':
			unordered_list = BlockContainer()
			for item in element.select(':scope > li'):
				if len(list(item.select(':scope > p'))) == 1:
					unordered_list += f'- {self.process_block(list(item.children)[0])}'
				else:
					unordered_list += f'- {self.process_inline(item)}'
			return unordered_list
		
		if element.name == 'div' and has_class(element, 'informaltable'):
			wrapper = BlockContainer()
			for child in element.children:
				wrapper += self.process_block(child)
			return wrapper
		
		if element.name == 'div' and has_class(element, 'section'):
			title = text_content(element.select_one(':scope > div.titlepage'))
			section = SectionContainer(title, 4)
			for child in element.children:
				if child.name == 'div' and has_class(child, 'titlepage'):
					continue
				else:
					section += self.process_block(child)
			return section

		print('unhandled block:', element.name)
		print(element)
		
		#return self.process_inline(element)
		return Text()
	
	def process_inline(self, element):
		if not hasattr(element, 'contents'):
			return Text(element.string.strip())
		
		content = ''
		for child in element.children:
			if not hasattr(child, 'contents'):
				content += child.string
			# elif child.name == 'p':
			# 	content += str(self.process_inline(child)).strip().replace('\n', ' ')
			elif child.name == 'code':
				highlight = None
				is_enum = False
				className = ''
				if child.has_attr('class'):
					className = child['class'][0]
				if className == 'methodname':
					highlight = 'hmethod'
				elif className == 'classname':
					highlight = 'hclass'
				elif className == 'parameter':
					highlight = 'hparam'
				elif className == 'constant':
					is_enum = True
				
				if is_enum:
					content += f'{{cpp:enum}}`{text_content(child)}`'
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
							content += f'{{cpp:enum}}`{text_content(grandchild)}`'
						else:
							content += text_content(grandchild)
				elif 'type' in child['class']:
					content += f'{{htype}}`{text_content(child)}`'
				elif 'keycap' in child['class']:
					content += f'{{hkey}}`{text_content(child)}`'
				else:
					print('WARNING: unable to handle span with classes:', child['class'])
					print('    ', text_content(child))
					content += text_content(child)
			# elif child.name == 'div' or child.name == 'table':
			# 	content += '\n'.join(str(self.process_block(child)))
			elif child.name == 'em':
				content += f'_{self.process_inline(child)}_'
			elif child.name == 'acronym':
				# no acronym support in markdown...
				print('WARNING: missing acronym support in markdown')
				content += text_content(child)
			else:
				print('WARNING: unable to handle child of type:', child.name)
				print('    ', child.parent)
				content += text_content(child)
	
		return Text(content.strip())
	
	def process_link(self, element):
		match = reference_re.search(element['href'])
		ref_type = 'ref'

		code = element.select_one(':scope > code')
		if code is not None:
			if has_class(code, 'methodname'):
				ref_type = 'cpp:func'
			elif has_class(code, 'classname'):
				ref_type = 'cpp:class'
				
		content = text_content(element)

		if match:
			ref_class = match.group(1)
			ref_method = match.group(2)
			if '::' in content:
				return f'{{cpp:func}}`{ref_class}::{ref_method}`'
			else:
				return f'{{cpp:func}}`~{ref_class}::{ref_method}`'
		else:
			return f'{{{ref_type}}}`{content}`'
	
if __name__ == '__main__':
	document = Document(sys.argv[1], sys.argv[2], None)
	document.process()
	#print('document:', document)
	with open(sys.argv[2], 'w') as file:
		print(document, file=file)
