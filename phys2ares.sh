#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <Save File> <ROM file>"
    exit 1
fi

save_file="$1"
rom="$2"

extension="${save_file##*.}"

case "$extension" in
	fla)
		new_ext="flash"
		;;
	sra)
		new_ext="ram"
		;;
	eep)
		new_ext="eeprom"
		;;
	*)
		echo "Invalid Save File Type"
		echo "Usage: $0 <Save File> <ROM file>"
		exit 1
		;;
esac

new_file="${rom}.${new_ext}"

mv -- "$save_file" "$new_file"

echo "Renamed '$save_file' to '$new_file'"

