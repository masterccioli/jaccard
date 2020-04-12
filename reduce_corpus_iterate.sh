#!/bin/bash
# Read a string with spaces using for loop
n=1
word_character_front=''
word_character_end=''

while [ $n -le 10 ]
do
	word_character_end='\s\w*'$word_character_end
	word_character_front='\w*\s'$word_character_front
	echo $n
	for value in bee honey bicycle pedal tv remote knife scalpel glasses binoculars door gate fence wall dog cat wasp book chapter doctor nurse
	do
		#grep -o "${word_character_front}${value}${word_character_end}" ../apply_to_fluency/tasa_underscored_animals.txt
		#value="$word_character_front${value)$word_character_end"
		var="`grep -o "${word_character_front}${value}${word_character_end}" ../apply_to_fluency/tasa_underscored_animals.txt`"
		echo $value
		echo "$var" >> wd_files/windowed_$n.txt
	done
	echo
	n=$(( n+1 ))
done
# grep -o '\w* bee \w*' ../apply_to_fluency/tasa_underscored_animals.txt
#grep -o '\w* \w* \w* \w* \w* \w* \w* \w* \w* \w* 