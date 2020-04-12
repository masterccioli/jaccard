#!/bin/bash
# Read a string with spaces using for loop

save_path=wd_files/windowed_10.txt

for value in bee honey bicycle pedal tv remote knife scalpel glasses binoculars door gate fence wall dog cat wasp book chapter doctor nurse
do
    var="`grep -o "\w* \w* \w* \w* \w* \w* \w* \w* \w* \w* ${value} \w* \w* \w* \w* \w* \w* \w* \w* \w* \w*" ../apply_to_fluency/tasa_underscored_animals.txt`"
	
	echo $value
	echo "$var" >> $save_path

done

save_path=wd_files/windowed_9.txt

for value in bee honey bicycle pedal tv remote knife scalpel glasses binoculars door gate fence wall dog cat wasp book chapter doctor nurse
do
    var="`grep -o "\w* \w* \w* \w* \w* \w* \w* \w* \w* ${value} \w* \w* \w* \w* \w* \w* \w* \w* \w*" ../apply_to_fluency/tasa_underscored_animals.txt`"
	
	echo $value
	echo "$var" >> $save_path

done

save_path=wd_files/windowed_8.txt

for value in bee honey bicycle pedal tv remote knife scalpel glasses binoculars door gate fence wall dog cat wasp book chapter doctor nurse
do
    var="`grep -o "\w* \w* \w* \w* \w* \w* \w* \w* ${value} \w* \w* \w* \w* \w* \w* \w* \w*" ../apply_to_fluency/tasa_underscored_animals.txt`"
	
	echo $value
	echo "$var" >> $save_path

done

save_path=wd_files/windowed_7.txt

for value in bee honey bicycle pedal tv remote knife scalpel glasses binoculars door gate fence wall dog cat wasp book chapter doctor nurse
do
    var="`grep -o "\w* \w* \w* \w* \w* \w* \w* ${value} \w* \w* \w* \w* \w* \w* \w*" ../apply_to_fluency/tasa_underscored_animals.txt`"
	
	echo $value
	echo "$var" >> $save_path

done

save_path=wd_files/windowed_6.txt

for value in bee honey bicycle pedal tv remote knife scalpel glasses binoculars door gate fence wall dog cat wasp book chapter doctor nurse
do
    var="`grep -o "\w* \w* \w* \w* \w* \w* ${value} \w* \w* \w* \w* \w* \w*" ../apply_to_fluency/tasa_underscored_animals.txt`"
	
	echo $value
	echo "$var" >> $save_path

done

save_path=wd_files/windowed_5.txt

for value in bee honey bicycle pedal tv remote knife scalpel glasses binoculars door gate fence wall dog cat wasp book chapter doctor nurse
do
    var="`grep -o "\w* \w* \w* \w* \w* ${value} \w* \w* \w* \w* \w*" ../apply_to_fluency/tasa_underscored_animals.txt`"
	
	echo $value
	echo "$var" >> $save_path

done

save_path=wd_files/windowed_4.txt

for value in bee honey bicycle pedal tv remote knife scalpel glasses binoculars door gate fence wall dog cat wasp book chapter doctor nurse
do
    var="`grep -o "\w* \w* \w* \w* ${value} \w* \w* \w* \w*" ../apply_to_fluency/tasa_underscored_animals.txt`"
	
	echo $value
	echo "$var" >> $save_path

done

save_path=wd_files/windowed_3.txt

for value in bee honey bicycle pedal tv remote knife scalpel glasses binoculars door gate fence wall dog cat wasp book chapter doctor nurse
do
    var="`grep -o "\w* \w* \w* ${value} \w* \w* \w*" ../apply_to_fluency/tasa_underscored_animals.txt`"
	
	echo $value
	echo "$var" >> $save_path

done

save_path=wd_files/windowed_2.txt

for value in bee honey bicycle pedal tv remote knife scalpel glasses binoculars door gate fence wall dog cat wasp book chapter doctor nurse
do
    var="`grep -o "\w* \w* ${value} \w* \w*" ../apply_to_fluency/tasa_underscored_animals.txt`"
	
	echo $value
	echo "$var" >> $save_path

done

save_path=wd_files/windowed_1.txt

for value in bee honey bicycle pedal tv remote knife scalpel glasses binoculars door gate fence wall dog cat wasp book chapter doctor nurse
do
    var="`grep -o "\w* ${value} \w*" ../apply_to_fluency/tasa_underscored_animals.txt`"
	
	echo $value
	echo "$var" >> $save_path

done