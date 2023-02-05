
var contents = '';

// start of the tree to parse
var mainSection = document.querySelector('body > div.section');

// first instance is the class name
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

			//console.log(child);
			//console.log(child.innerText);

			if (child.matches('div.titlepage'))
				continue;
			
			if (child.matches('code')) {
				// probably the function...
				var text = child.innerText
					.replaceAll('\n', ' ')
					.replaceAll(/[\t \xa0]+/g, ' ') // tab, space, nbsp
					.replace(/;$/, '');
				text = text.replace(/([a-zA-Z0-9_]+)\(/,
						(match, name, offset, string, groups) => {
							return `${className}::${name}(`;
						});
				contents += `:::{cpp:function} ${text}\n:::\n`;
				continue;
			}

			contents += '\n';
			dumpNode(child);
		}		

		contents += '::::\n\n';
	}
}

function dumpNode(element)
{
	if (element.matches('p'))
	{
		// paragraph, with possible nested formatting...
		dumpParagraph(element);
	}

	if (element.matches('table'))
	{
		// output a table
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
}

console.log(contents.replace(/[\n\t \xa0]+::::/, '::::'));
