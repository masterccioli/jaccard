#!/bin/bash
# Read a string with spaces using for loop
n=1
word_character_front=''
word_character_end=''
echo $1
echo $2
while [ $n -le $1 ]
do
	word_character_end='\s\w*'$word_character_end
	word_character_front='\w*\s'$word_character_front
	

	n=$(( n+1 ))
done

echo $word_character_front
#grep -o "${word_character_front}${2}${word_character_end}" ../apply_to_fluency/tasa_underscored_animals.txt
#value="$word_character_front${value)$word_character_end"
var="`grep -o "${word_character_front}${2}${word_character_end}" ../apply_to_fluency/tasa_underscored_animals.txt`"
echo $value
echo "$var" >> wd_files/out.txt


#grep -o '\w* bee \w*' ../apply_to_fluency/tasa_underscored_animals.txt
#grep -o '\w* \w* \w* \w* \w* \w* \w* \w* \w* \w* 