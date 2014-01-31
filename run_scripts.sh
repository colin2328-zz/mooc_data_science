#!/bin/bash
# Please list new populate scripts in the order they should be run
# files=(create_dropout_feature_values.sql users_populate_user_last_submission_id.sql users_populate_dropout_week.sql populate_feature_1_dropout.sql)
files=(problems_populate_problem_week.sql populate_feature_204_pset_grade.sql)
for file in ${files[@]}
do 
	echo "Running $file"
	mysql -u root -e "source ${file}"
done

# echo $(mysql -u root -e "select * from mock.dropout_feature_values")
