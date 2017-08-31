#!/usr/bin/awk -f
BEGIN {
    FS="[^a-zA-Z]+"
}
#    if (NR>=3) {print}
{
    if (NR>=3) 
      for (i=1; i<=NF; i++)
          words[$i]++
}
END {
    for (i in words)
         print i, words[i]
}
