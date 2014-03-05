#!/bin/bash
# Please list new populate scripts in the order they should be run in sql_files.txt
files=$(cat sql_files.txt)
out_file="progress.txt"

function print_and_save {
	echo $1
	echo $1 >> $2
}

> ${out_file}
for file in ${files[@]}
do 
	start_time=$(date +%s)
	print_and_save "Running ${file} on $(date)" ${out_file}
	mysql -u root -e "source ${file}"
	end_time=$(date +%s)
	total_time=$((${start_time} - ${end_time}))
	print_and_save "Finished Running ${file} in ${total_time} seconds" ${out_file}
done

# echo $(mysql -u root -e "select * from moocdb.dropout_feature_values")
