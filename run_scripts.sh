#!/bin/bash
# Please list new populate scripts in the order they should be run in sql_files.txt
files=$(cat sql_files.txt)
for file in ${files[@]}
do 
	echo "Running $file"
	mysql -u root -e "source ${file}"
done

# echo $(mysql -u root -e "select * from moocdb.dropout_feature_values")
