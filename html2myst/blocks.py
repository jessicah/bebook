import spans

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

### Actually, I want to dump the tree...

def indent(n):
	return ' ' * n

def fit_to_lines(text, indent=''):
	lines = [indent]
	for token in text.replace('\n', ' ').split(' '):
		last = lines[-1]
		if (len(last) + len(token) + 1) > 75:
			lines.append(f'{indent}{token}')
		else:
			lines[-1] += ' ' + token
	return '\n'.join(list(map(str.strip, lines)))

class Block:
	def __init__(self, directive=None):
		self.content = ''
		if isinstance(directive, tuple):
			self.directive, self.colons = directive
		elif isinstance(directive, str):
			self.directive = directive
			self.colons = ':::'
		else:
			self.directive = None
		self.strip = True

	def walk(self, depth):
		print(f'{indent(depth)} Block')

	def __str__(self):
		return self.wrap_content()

	def __iadd__(self, content):
		if isinstance(content, spans.Text):
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

	def walk(self, depth):
		print(f'{indent(depth)} Block Container:')
		for block in self.blocks:
			if isinstance(block, str):
				print(f'{indent(depth+2)} <string content>')
			else:
				block.walk(depth + 2)

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

	def walk(self, depth):
		print(f'{indent(depth)} Section Container:')
		for block in self.blocks:
			if isinstance(block, str):
				print(f'{indent(depth+2)} <string content>')
			else:
				block.walk(depth + 2)

	def output_title(self, add_title):
		self.add_title = add_title

	def __str__(self):
		body = super().__str__()

		if self.add_title:
			return f'{self.title}\n\n{body}'
		else:
			return body

class TableRow(Block):
	def walk(self, depth):
		print(f'{indent(depth)} Table Row')

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

	def walk(self, depth):
		print(f'{indent(depth)} Table:')
		for block in self.blocks:
			block.walk(depth + 2)

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

	def walk(self, depth):
		print(f'{indent(depth)} List Item:')
		for block in self.blocks:
			if isinstance(block, str):
				print(f'{indent(depth+2)} <string content>')
			else:
				block.walk(depth + 2)

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

	def walk(self, depth):
		print(f'{indent(depth)} Unordered List:')
		for block in self.blocks:
			block.walk(depth + 2)

class OrderedList(BlockContainer):
	def __str__(self):
		self.content = ''
		for index, list_item in enumerate(self.blocks, start=1):
			self.content += list_item.print(f'{index}.')
		return super().wrap_content().strip()

	def walk(self, depth):
		print(f'{indent(depth)} Ordered List:')
		for block in self.blocks:
			block.walk(depth + 2)

class DefinitionTerm(Block):
	def walk(self, depth):
		print(f'{indent(depth)} Definition Term')

class DefinitionData(BlockContainer):
	def walk(self, depth):
		print(f'{indent(depth)} Definition Data:')
		for block in self.blocks:
			if isinstance(block, str):
				print(f'{indent(depth+2)} <string content>')
			else:
				block.walk(depth + 2)

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

	def walk(self, depth):
		print(f'{indent(depth)} Definition List:')
		for block in self.blocks:
			block.walk(depth + 2)
