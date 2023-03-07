## Nodes for generating markdown

### Need to correclty handle nesting though...

### So, want to take the formatted child content,
### and then indent it as required... but what does
### that look like?

### Should the whole `__str__` be replaced with
### explicit functions, e.g. `print` for the
### ListItem type? This may allow passing in a
### formatter or value for indenting the content
### that `print` produces...

class Item:
	def __init__(self):
		pass
	
	def __str__(self):
		return ''

class Text(Item):
	def __init__(self, content=''):
		# could we do some line wrapping here?
		if isinstance(content, Text):
			content = str(content)
		lines = ['']
		for token in content.replace('\n', ' ').split(' '):
			last = lines[-1]
			if (len(last) + len(token) + 1) > 75:
				lines.append(token)
			else:
				lines[-1] += ' ' + token
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
		if other is not None:
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

class TableRow(Item): pass

class Table(BlockContainer):
	def __init__(self, num_headers=1):
		directive = [
				'{list-table}',
				'---',
				f'header-rows: {num_headers}',
				'align: left',
				'widths: auto',
				'---'
			]
		super().__init__('\n'.join(directive))
	
	def wrap(self, block):
		lines = str(block).split('\n')
		content = ''
		for index, line in enumerate(lines):
			if len(line) == 0:
				content += '\n'
			elif index == 0:
				content += f'\t- {line}\n'
			else:
				content += f'\t\t{line}\n'
		return content

	def __str__(self):
		self.content = ''
		for block in self.blocks:
			if isinstance(block, TableRow):
				self.content += '-\n'
			elif isinstance(block, BlockContainer):
				self.content += self.wrap(block)
			else:
				self.content += f'\t- {str(block)}\n\n'
		return super().wrap_content()

class ListItem(BlockContainer):
	def __str__(self):
		self.content = ''
		for index, block in enumerate(self.blocks):
			if index == 0:
				self.content += f'{self.prefix} {str(block)}\n'
			else:
				self.content += f'  {str(block)}\n'
		return super().wrap_content()
	
	def print(self, prefix):
		self.prefix = prefix
		self.content = ''
		for index, block in enumerate(self.blocks):
			if index == 0:
				self.content += f'{self.prefix} {str(block)}\n\n'
			else:
				self.content += f'  {str(block)}\n\n'
		return super().wrap_content()

class UnorderedList(BlockContainer):
	def __str__(self):
		self.content = ''
		for list_item in self.blocks:
			self.content += list_item.print('-')
		return super().wrap_content().strip()

class OrderedList(BlockContainer):
	def __str__(self):
		self.content = ''
		for index, list_item in enumerate(self.blocks, start=1):
			self.content += list_item.print(f'{index}.')
		return super().wrap_content().strip()

class DefinitionTerm(Text): pass
class DefinitionData(BlockContainer): pass

class DefinitionList(BlockContainer):
	def __str__(self):
		self.content = ''
		for item in self.blocks:
			if isinstance(item, DefinitionTerm):
				self.content += f'{str(item)}\n\n'
			else:
				for index, data in enumerate(item.blocks):
					if index == 0:
						self.content += f': {str(data)}\n\n'
					else:
						self.content += f'  {str(data)}\n\n'
		return super().wrap_content().strip()
