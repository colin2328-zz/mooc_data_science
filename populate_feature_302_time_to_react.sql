## time the script takes to run on moocdb db:  xx seconds
## date:  12/10/2013
## author: Josep Marc Mingot Hidalgo  
## email:  jm.mingot@gmail.com
## description of feature:
## Average time(in days) the student takes to react when a new resource is posted.
## Pretends to capture how fast a student is reacting to new content.
## name for feature: time_to_react
## would you like to be cited, and if so, how?
## Josep Marc Mingot Hidalgo
## Modified by Colin Taylor (3/5/2014) to insert into database with feature number 302


INSERT INTO dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
SELECT 
	302,
	e.user_id,
	FLOOR((UNIX_TIMESTAMP(e.observed_event_timestamp) - UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) AS week,
	AVG(e.difference) as avg_reacting_time
FROM
	(SELECT 
		a.user_id,
			a.url_id,
			a.observed_event_timestamp,
			d.resource_release_timestamp,
			(UNIX_TIMESTAMP(a.observed_event_timestamp) - UNIX_TIMESTAMP(d.resource_release_timestamp)) / 86400 AS difference
	FROM
		observed_events AS a
	LEFT JOIN (SELECT 
		b.resource_id, b.resource_release_timestamp, c.url_id
	FROM
		resources AS b
	LEFT JOIN (SELECT 
		resource_id, url_id
	FROM
		resources_urls) AS c ON b.resource_id = c.resource_id) AS d ON a.url_id = d.url_id) AS e
GROUP BY user_id , week;



