#!/bin/bash

usage="
Syntax: ./grepScript.sh [-f | -l | -d | -o | -h]
Options:
-f      Filename with domains, one per line.
-l      DNS Log that will be parsed.
-d      EMPTY directory used for outputting temporary files and list of suspect source IPs.
-o	Dump output of command to a specified file. *OPTIONAL*
-h	Print this help page.
"

while getopts ":f:l:d:o:h" flag; do
    case ${flag} in
        f) filename=$OPTARG;;
        l) log=$OPTARG;;
        d) output=$OPTARG;;
	o) outFile=$OPTARG;;
	h) echo "$usage"
	   exit
	   ;;
	\?) echo "$usage"
	    exit
	    ;;
    esac
done

shift $((OPTIND -1))

cat $filename | sed 's/\www\.//g' > $output/tempDomainsForCleaning.txt
cat $output/tempDomainsForCleaning.txt | sed 's/\..*//' | sort -g | uniq > $output/uniqueDomainsForParsing.txt

parsingFile=$output/uniqueDomainsForParsing.txt

{
echo Starting to parse ...
numDomains=$(wc -l < $parsingFile)
count=1
while read p; do
	cat $log | grep $p > $output/$p.txt
	echo $count out of $numDomains finished
	temp=$(wc -l $output/$p.txt | awk '{print $1}')
	if (( temp != 0 ))
	then
		echo Hit on $p ...
		echo Source IPs are/is ...
		badSources=$(cat $output/$p.txt | awk '{print $9}' | sed '/^[[:space:]]*$/d' | sort -g | uniq)
		echo "$badSources"
		echo "$badSources" >> $output/tempBadSourceIPs.txt
	fi
	count=$((count+1))
done < $parsingFile
} 2>&1 | tee $outFile

cat $output/tempBadSourceIPs.txt | sort -g | uniq > $output/moreBadSourceIPs.txt
cat $output/moreBadSourceIPs.txt | grep -v '208.67.220.220\|208.67.222.222' > $output/badSourceIPs.txt
find $output -type f -not -name 'badSourceIPs.txt' -delete
