#!/bin/bash

if $_ gt 0; then
	cd $1
fi

find . -name "*.zip" | while read filename; do unzip -o -d "`dirname "$filename"`" "$filename"; done;
