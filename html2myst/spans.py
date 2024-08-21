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

class Item:
	def __init__(self):
		pass

	def __str__(self):
		return ''

	def walk(self, depth):
		print(f'{indent(depth)} Empty Item')

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

	def walk(self, depth):
		print(f'{indent(depth)} Text')

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
