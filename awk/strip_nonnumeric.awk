#!/usr/bin/awk -f
{outfile=FILENAME ".numeric"}
/^[[:digit:]]/ { print > outfile; next; }
