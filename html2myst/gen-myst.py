import os
import subprocess
import html2myst

if __name__ == '__main__':
	with open('sources.txt', 'r') as file:
		for line in file:
			if len(line) == 0:
				continue
			if line[0] == '#':
				continue
			
			parts = line.split(' ')

			if len(parts) != 2:
				continue

			source = parts[0].strip()
			dest = parts[1].strip()

			#subprocess.run(["python", "html2myst/html2myst.py",
			#f"_source_html/{source}", dest])
			
			# or run it directly...
			document = html2myst.Document(f"_source_html/{source}", dest, None)
			document.process()

			# outlining sets the correct level of block fences
			# after building the tree
			if (hasattr(document, 'section') is False):
				continue

			document.section.outline(0)
			
			os.makedirs(os.path.dirname(dest), exist_ok=True)
			with open(dest, 'w', encoding='utf8', newline='\n') as outfile:
				print(str(document).replace("\r\n", "\n").replace('\r','\n'), file=outfile)

			