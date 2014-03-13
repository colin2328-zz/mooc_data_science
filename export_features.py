'''
Takes  seconds to execute
Created on July 8, 2013
@author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
@author: edited by Colin Taylor on March 13, 2014
'''



# Download it at http://sourceforge.net/projects/mysql-python/?source=dlp (32 bits) 
#                or http://www.codegood.com/archives/129 (64 bits)
# Tutorials: http://mysql-python.sourceforge.net/MySQLdb.html
#            http://zetcode.com/db/mysqlpython/
import MySQLdb as mdb 
import csv

def export_features(connection):
    '''
    
    '''
    
    number_of_weeks = 15 # if you change this, but the date the SQL query to dropout_feature_values.dropout_feature_value_week < number_of_weeks 
    missing_value = - 1
    features_set = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
    number_of_features = len(features_set)
    cursor = connection.cursor()    
    record_list = list()
    file_output = open('features.csv', 'wb')
    
    
    sql = '''\
        SELECT user_id, dropout_feature_value_week, dropout_feature_id, dropout_feature_value 
        FROM moocdb.dropout_feature_values 
        WHERE dropout_feature_values.dropout_feature_value_week < 15
        AND dropout_feature_values.dropout_feature_value_week >= 0
        ORDER BY dropout_feature_values.user_id  
        -- LIMIT 55000;
        '''     
    features  = {}
    cursor.execute(sql)
    for i in range(cursor.rowcount):        
        row = cursor.fetchone()
        user_id = row[0]
        feature_id = row[2]
        if not feature_id in features_set:
            continue

        feature_number = features_set.index(feature_id)
        week_number = row[1]
        feature_value = row[3]
        # create new students if not existing
        if not user_id in features:
            features[user_id] = [[missing_value for i in range(number_of_features)] for j in range(number_of_weeks)]
        
        features[user_id][week_number][feature_number] = feature_value
        
        if i % 10000 == 0:
            print str(float(i) / cursor.rowcount * 100) + '% done'
                
    
    # Add headers
    file_output.write('week_number,')
    for feature_number in features_set:
        file_output.write(' feature_' + str(feature_number) + ',')
    file_output.write('\n') 
    
    # Save all the features to a file
    for user_id in features:
        features[user_id]
        week_number = 0 
        for week_data in features[user_id]:
            week_data.insert(0, week_number) # http://stackoverflow.com/questions/8537916/whats-the-idiomatic-syntax-for-prepending-to-a-short-python-list
            writer = csv.writer(file_output)
            writer.writerow(week_data)
            week_number += 1
            
        
    
    
        
def main():
    '''
    This is the main function
    '''
    # connection = mdb.connect(user="root",passwd="edx2013", port=3316,db="moocdb")#, charset='utf8', use_unicode=True);
    connection = mdb.connect(user="root",passwd="", port=3306,db="moocdb")#, charset='utf8', use_unicode=True);

    export_features(connection)
    connection.close()
    
    
if __name__ == "__main__":
    main()


