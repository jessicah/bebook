#!/bin/bash

set -e

PYTHON3="sem -j+0 python3"
PYTHON3="python3.12"

while read params; do
	if [[ "$params" =~ .*\.md ]]; then
		$PYTHON3 html2myst/html2myst.py _source_html/$params
	fi
done <sources.txt

sem --wait
