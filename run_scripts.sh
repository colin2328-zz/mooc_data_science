#!/bin/bash
# Please list new populate scripts in the order they should be run
# files=(create_dropout_feature_values.sql users_populate_user_last_submission_id.sql users_populate_dropout_week.sql populate_feature_1_dropout.sql)
# files=(populate_feature_205_pset_grade_over_time.sql)
for file in ${files[@]}
do 
	echo "Running $file"
	mysql -u root -e "source ${file}"
done

# echo $(mysql -u root -e "select * from moocdb.dropout_feature_values")
