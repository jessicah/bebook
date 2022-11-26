# Generating the Class API

Generating the public API:

```sh
readelf -aW /boot/system/develop/lib/libbe.so		\
	| c++filt										\
	| grep -e 'GLOBAL[ ]*DEFAULT'					\
	| grep -v -e 'UND' -e '@@'						\
	| awk '{ $1=$2=$3=$4=$5=$6=$7=""; print $0 }'	\
	| sort > api.txt
```

Generating class names:

```sh
grep api.txt -e '::' | awk -F'::' '{ print $1 }' \
	| sort | uniq > classes.txt
```

Generating member functions:

```sh
grep api.txt -e '::' | awk -F'::' '{ Print $2 }' \
	| sort | uniq > member-functions.txt
```

The goal is to use this, or something similar, to generate custom highlighting in pygments within
sphinx for code blocks. The original Be Book documentation used a convention for highlighting, as
follows:

- Class Names: green-ish
- Method Names: purple
- Function Names: blue-ish
- Parameters: rusty
- Types: something else
- Constants: blue
- Variable Names: black
