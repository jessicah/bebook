$lines = Get-Content .\sources.txt

ForEach ($line in $lines) {
	If ($line.StartsWith('#')) {
		Continue
	}

	$parts = $line.Split(' ')

	#If ((ls $parts[1]).Extension -Eq '.md')
	#{
		$part = $parts[0]
		$source = "_source_html/$part"
		$dest = $parts[1]

		& python html2myst/html2myst.py $source $dest
	#}
}
