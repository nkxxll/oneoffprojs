#!/bin/bash
# asciify - Convert non-ASCII characters to ASCII equivalents
# Version: 1.0.0
# Author: nkxxll

# Convert special characters to ASCII equivalents
# Useful for markdown/typst files that have issues with non-ASCII chars

# Read from stdin or file argument
if [ $# -eq 0 ]; then
    input=$(cat)
else
    input=$(cat "$1")
fi

# Apply character mappings
echo "$input" | sed \
    -e 's/–/-/g' \
    -e 's/—/--/g' \
    -e 's/−/-/g' \
    -e 's/→/->/g' \
    -e 's/←/<-/g' \
    -e 's/↔/<->/g' \
    -e 's/"/"/g' \
    -e 's/"/"/g' \
    -e 's/'\''/'"'"'/g' \
    -e 's/'\''/'"'"'/g' \
    -e 's/…/.../g' \
    -e 's/•/*/g' \
    -e 's/°/deg/g' \
    -e 's/×/x/g' \
    -e 's/÷/\//g' \
    -e 's/§/sec/g' \
    -e 's/¶/para/g' \
    -e 's/†/\*/g' \
    -e 's/‡/\*\*/g' \
    -e 's/É/E/g' \
    -e 's/é/e/g' \
    -e 's/È/E/g' \
    -e 's/è/e/g' \
    -e 's/Ê/E/g' \
    -e 's/ê/e/g' \
    -e 's/Ë/E/g' \
    -e 's/ë/e/g' \
    -e 's/Á/A/g' \
    -e 's/á/a/g' \
    -e 's/À/A/g' \
    -e 's/à/a/g' \
    -e 's/Â/A/g' \
    -e 's/â/a/g' \
    -e 's/Ä/A/g' \
    -e 's/ä/a/g' \
    -e 's/Ã/A/g' \
    -e 's/ã/a/g' \
    -e 's/Å/A/g' \
    -e 's/å/a/g' \
    -e 's/Ú/U/g' \
    -e 's/ú/u/g' \
    -e 's/Ù/U/g' \
    -e 's/ù/u/g' \
    -e 's/Û/U/g' \
    -e 's/û/u/g' \
    -e 's/Ü/U/g' \
    -e 's/ü/u/g' \
    -e 's/Ó/O/g' \
    -e 's/ó/o/g' \
    -e 's/Ò/O/g' \
    -e 's/ò/o/g' \
    -e 's/Ô/O/g' \
    -e 's/ô/o/g' \
    -e 's/Ö/O/g' \
    -e 's/ö/o/g' \
    -e 's/Õ/O/g' \
    -e 's/õ/o/g' \
    -e 's/Ø/O/g' \
    -e 's/ø/o/g' \
    -e 's/Í/I/g' \
    -e 's/í/i/g' \
    -e 's/Ì/I/g' \
    -e 's/ì/i/g' \
    -e 's/Î/I/g' \
    -e 's/î/i/g' \
    -e 's/Ï/I/g' \
    -e 's/ï/i/g' \
    -e 's/ç/c/g' \
    -e 's/Ç/C/g' \
    -e 's/č/c/g' \
    -e 's/Č/C/g' \
    -e 's/ñ/n/g' \
    -e 's/Ñ/N/g' \
    -e 's/š/s/g' \
    -e 's/Š/S/g' \
    -e 's/ž/z/g' \
    -e 's/Ž/Z/g' \
    -e 's/ź/z/g' \
    -e 's/Ź/Z/g' \
    -e 's/đ/d/g' \
    -e 's/Đ/D/g' \
    -e 's/ł/l/g' \
    -e 's/Ł/L/g' \
    -e 's/æ/ae/g' \
    -e 's/Æ/AE/g' \
    -e 's/œ/oe/g' \
    -e 's/Œ/OE/g' \
    -e 's/ß/ss/g' \
    -e 's/ẞ/SS/g'
