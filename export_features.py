'''
Takes  seconds to execute
Created on July 8, 2013
@author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com
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
    number_of_features = 20
    number_of_weeks = 15 # if you change this, but the date the SQL query to dropout_feature_values.dropout_feature_value_week < number_of_weeks 
    missing_value = - 1
    features_set = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 103, 104, 105, 109, 110, 111, 112]
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
        #print row
        user_id = row[0]
        feature_id = features_set.index(row[2])
        week_number = row[1]
        feature_value = row[3]
        # create new students if not existing
        if not user_id in features:
            features[user_id] = [[missing_value for i in range(number_of_features)] for j in range(number_of_weeks)]
        
        # 
        #print user_id, week_number, feature_id 
        features[user_id][week_number][feature_id] = feature_value
        
        if i % 10000 == 0:
            print str(float(i) / cursor.rowcount * 100) + '% done'
            
        
    #print features[2496]
    
    
    # Add headers
    file_output.write('week_number,')
    for feature_number in range(number_of_features):
        file_output.write(' feature_' + str(feature_number + 1) + ',')
    file_output.write('\n') 
    
    # Save all the features to a file
    for user_id in features:
        features[user_id]
        week_number = 0 
        for week_data in features[user_id]:
            week_data.insert(0, week_number) # http://stackoverflow.com/questions/8537916/whats-the-idiomatic-syntax-for-prepending-to-a-short-python-list
            #print week_data
            writer = csv.writer(file_output)
            writer.writerow(week_data)
            week_number += 1
            
        
    
    
        
def main():
    '''
    This is the main function
    '''
    connection = mdb.connect('127.0.0.1', 'root', 'edx2013', 'beatdb', port=3316) #, charset='utf8', use_unicode=True);
    export_features(connection)
    connection.close()
    
    
if __name__ == "__main__":
    main()


