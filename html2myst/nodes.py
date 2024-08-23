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
		if (len(last) + len(token)) > 75:
			lines.append(f'{indent}{token} ')
		else:
			lines[-1] += token + ' '
	content = '\n'.join(list(map(str.rstrip, lines)))
	return content.replace('\r', '\n')

class Item:
	def __init__(self):
		self.directive = None
		self.depth = 0
		self.extent = 0
		pass

	def __str__(self):
		return ''

	def walk(self, depth):
		print(f'{indent(depth)} Empty Item')

	def outline(self, depth):
		return depth, False

	def fence(self):
		return ':' * (self.extent - self.depth + 3)

class Text(Item):
	def __init__(self, content=''):
		super().__init__()
		# could we do some line wrapping here?
		if isinstance(content, Text):
			content = str(content)
		self.content = fit_to_lines(content)

	def __str__(self):
		return str(self.content)

	def walk(self, depth):
		print(f'{indent(depth)} Text')

class Block(Text):
	def __init__(self, directive=None):
		super().__init__()
		if isinstance(directive, str):
			self.directive = directive
		else:
			self.directive = None
		self.strip = True

	def outline(self, depth):
		if self.directive is not None:
			self.depth = depth
			self.extent = depth
		return self.extent, self.directive is not None

	def walk(self, depth):
		print(f'{indent(depth)} Block')

	def __str__(self):
		return self.wrap_content()

	def __iadd__(self, content):
		if isinstance(content, Text):
			self.content += str(content)
		else:
			self.content += content
		return self

	def set_directive(self, directive):
		self.directive = directive

	def wrap_content(self):
		if self.directive is None:
			return self.content
		else:
			if len(self.content.strip()) == 0:
				return f'{self.fence()}{self.directive}\n{self.fence()}'
			else:
				return f'{self.fence()}{self.directive}\n{self.content}\n{self.fence()}'

class BlockContainer(Block):
	def __init__(self, directive=None):
		super().__init__(directive)
		self.blocks = []

	def outline(self, depth):
		self.depth = depth
		self.extent = depth
		new_depth = depth + 1 if self.directive is not None else depth
		for block in self.blocks:
			if not isinstance(block, str):
				new_extent, has_directive = block.outline(new_depth)
				if has_directive:
					self.extent = max(self.extent, new_extent)
		return self.extent, self.directive is not None

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

class TableRow(BlockContainer):
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
			if isinstance(block, Block):
				self.content += self.wrap(block)
			else:
				wrapped = fit_to_lines(str(block), '  ')
				if index == 0:
					self.content += f'{self.prefix} {wrapped[2:]}\n'
				else:
					self.content += f'{wrapped}\n'
		return super().wrap_content()

	def wrap(self, block):
		# a block (pre) can contain explicit line breaks using '\r',
		# so use `splitlines()` instead of `split('\n')`
		lines = str(block).splitlines()
		content = ''
		for index, line in enumerate(lines):
			if index == 0 and len(line) == 0:
				content += f'{self.prefix}\n'
			elif index == 0:
				content += f'{self.prefix} {line}\n'
			else:
				content += f'  {line}\n'
		return content

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
			if isinstance(block, Block):
				self.content += self.wrap(block)
			else:
				wrapped = fit_to_lines(str(block), '  ')
				if index == 0:
					self.content += f'{self.prefix} {wrapped[2:]}\n\n'
				else:
					self.content += f'{wrapped}\n\n'
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

class DefinitionTerm(Text):
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

class Image(Text):
	def __init__(self, path, title=None):
		self.path = path
		self.title = title

	def __str__(self):
		if self.title is None:
			return f'![]({self.path})'
		else:
			return f'![{self.title}]({self.path})'

	def walk(self, depth):
		print(f'{indent(depth)} Image')

class Bold(Text):
	def __init__(self, body=''):
		# unwrap a nested bold, else we end up with
		# incorrect formatting
		if isinstance(body, Bold):
			self.content = body.content
		else:
			self.content = body

	def __str__(self):
		return f'**{str(self.content)}**'

	def walk(self, depth):
		print(f'{indent(depth)} Bold')

class Italics(Text):
	def __init__(self, body=''):
		# unwrap a nested italics, else we end up with
		# incorrect formatting
		if isinstance(body, Bold):
			self.content = body.content
		else:
			self.content = body

	def __str__(self):
		return f'_{str(self.content)}_'

	def walk(self, depth):
		print(f'{indent(depth)} Italics')
