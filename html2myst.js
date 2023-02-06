
var contents = '';

var mainSection = document.querySelector('body > div.section');

var className = document.querySelector('body > div.section > div.titlepage').innerText;

contents += `# ${className}\n\n`;

var sections = document.querySelectorAll('body > div.section > div.section');

for (var ix = 0; ix < sections.length; ++ix)
{
	var section = sections[ix];

	var sectionName = [...section.children].filter(el => el.matches('div.titlepage'));

	contents += `## ${sectionName[0].innerText}\n\n`;

	var subSections = [...section.children].filter(el => el.matches('div.section'));
	
	for (var iy = 0; iy < subSections.length; ++iy)
	{
		contents += '::::{abi-group}\n';

		var subSection = subSections[iy];

		for (var iz = 0; iz < subSection.children.length; ++iz)
		{
			var child = subSection.children[iz];

			if (child.matches('div.titlepage'))
				continue;
			
			if (child.matches('code')) {
				dumpDeclaration(child);
				continue;
			}

			if (child.matches('div.synopsisgroup')) {
				for (var iw = 0; iw < child.children.length; ++iw) {
					if (child.children[iw].matches('code')) {
						dumpDeclaration(child.children[iw]);
					}
				}
			}

			contents += '\n';
			dumpNode(child);
		}		

		contents += '::::\n\n';
	}
}

function dumpDeclaration(code)
{
	var text = code.innerText
		.replaceAll('\n', ' ')
		.replaceAll(/[\t \xa0]+/g, ' ') // tab, space, nbsp
		.replace(/;$/, '');
	if (text.startsWith('global') && text.indexOf('operator') >= 0) {
		// global operator overloading... return as-is
		contents += `:::{cpp:function} ${text.replace(/^global/, '')}\n:::\n`;
	} else {
		let isGlobal = text.endsWith('global');
		if (isGlobal) {
			// non-member functions, in the global namespace
			contents += `:::{cpp:function} ${text.replace(/global$/, '')}\n:::\n`;
		} else {
			text = text.replace(/([a-zA-Z0-9_]+)\(/,
					(match, name, offset, string, groups) => {
						return `${className}::${name}(`;
					})
					.replace(/(operator[+\-*\/%^&|~!=<>!,()[\]]{1,3})\(/,
					(match, name, offset, string, groups) => {
						return `${className}::${name}(`;
					});
			contents += `:::{cpp:function} ${text}\n:::\n`;
		}
	}
}

function dumpNode(element)
{
	if (element.matches('p'))
	{
		dumpParagraph(element);
	}
	else if (element.matches('div') && element.className.indexOf('admonition') >= 0)
	{
		let paragraphs = element.querySelectorAll('p');
		let title = element.querySelector('div.title');
		let type = element.className.replace('admonition', '').trim();

		contents += `:::{admonition} ${title.innerText}\n`;
		contents += `:class: ${type}\n`;

		for (let ix = 0; ix < paragraphs.length; ++ix) {
			dumpParagraph(paragraphs[ix]);
		}

		contents += '\n:::\n\n';
	}
	else if (element.matches('pre'))
	{
		contents += ':::{code}\n';
		contents += element.textContent;
		contents += '\n:::\n';
	}

	if (element.matches('table'))
	{
		// output a table... should be able to automate this too...
		contents += ':::{list-table}\n:::\n\n';
	}
}

function dumpParagraph(paragraph)
{
	for (var ix = 0; ix < paragraph.childNodes.length; ++ix)
	{
		var node = paragraph.childNodes[ix];
		
		if (node.nodeName == '#text')
		{
			contents += node.textContent;
		}
		else
		{
			dumpInline(node);
		}
	}

	contents += '\n\n';
}

function dumpInline(node)
{
	if (node.matches('code'))
	{
		var highlight = '';
		switch (node.className)
		{
			case 'methodname':	highlight = 'hmethod'; break;
			case 'classname':	highlight = 'hclass'; break;
			case 'parameter':	highlight = 'hparam'; break;
			default: break;
		}

		if (highlight.length > 0)
			contents += `{${highlight}}\`${node.textContent}\``;
		else
			contents += node.textContent;
	}
	else if (node.matches('a'))
	{
		var codeNode = node.firstChild;
		var type = '';
		switch (codeNode.className)
		{
			case 'methodname':	type = 'cpp:func'; break;
			case 'classname':	type = 'cpp:class'; break;
			default:			type = '...'; break;
		}

		var result = node.attributes['href'].value.match(/#([^_]+)_([^_]+)/);

		if (result != null)
		{
			let className = result[1];
			let methodName = result[2];

			if (codeNode.textContent.indexOf('::') < 0)
				contents += `{cpp:func}\`~${className}::${methodName}\``;
			else
				contents += `{cpp:func}\`${className}::${methodName}\``;
		}
		else
		{
			contents += `{${type}}\`${codeNode.textContent}\``;
		}
	}
	else if (node.matches('span'))
	{
		if (node.className == 'code')
			contents += `\`${node.textContent}\``;
		else
			contents += node.textContent;
	}
	else
	{
		contents += node.textContent;
	}
}

var lines = contents.split('\n');
for (let ix = 0; ix < lines.length; ++ix)
{
	lines[ix] = lines[ix].trimEnd();
}

contents = lines.join('\n')
	.replaceAll(/[\n]+\n/g, '\n\n');

console.log(contents);
