from flask import Flask, jsonify, request
import pymysql
import sys

REGION = 'us-east-2'

rds_host = 'xbias-backend.cytnlddqky1c.us-east-2.rds.amazonaws.com'
username = 'xBias_master'
password = 'Kr19972=14'
db_name = 'xbias_backend'

app=Flask(__name__)

# GET request to pull all the information from the database
@app.route('/xbias_backend/get_articles')
def get_entries_from_loggers():
	ret_json={}
	conn = pymysql.connect(rds_host, user = username, passwd = password, db= db_name, connect_timeout = 5)
	with conn.cursor() as cur:
		cur.execute("""SELECT * FROM article_table""")
		result = cur.fetchall()
		cur.close()
		i=1
		for row in result:
			temp_json_entry={
					'source_id': row[1],
					'source_name': row[2],
					'author': row[3],
					'title': row[4],
					'description': row[5],
					'url': row[6],
					'urlToImage': row[7],
					'publishedAt': row[8],
					'article_bias_score': row[9]
				}
			print(temp_json_entry)
			ret_json['entry_{n}'.format(n=i)]= temp_json_entry
			i+=1

		return(jsonify({'overall_entries': ret_json}))

# POST request to send an entry into the database
@app.route('/xbias_backend/create_entry_logger', methods=['POST'])
def create_entry():
	logging = request.get_json()
	conn = pymysql.connect(rds_host, user = username, passwd = password, db= db_name, connect_timeout = 10, autocommit=True)
	with conn.cursor() as cur:
		cur.execute("""CREATE TABLE IF NOT EXISTS article_entry_logger (article_entry_id VARCHAR(255), article_name VARCHAR(255), article_link VARCHAR(255), articles_news_org VARCHAR(255), article_bias_score FLOAT, device_id VARCHAR(255), device_interface VARCHAR(255), click_timestamp VARCHAR(255));""")
		cur.execute(
			"""
			INSERT INTO article_entry_logger (article_entry_id, article_name , article_link , articles_news_org , article_bias_score, device_id, device_interface, click_timestamp) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})
			""".format('"'+str(logging['article_entry_id'])+'"', '"' + str(logging['article_name']) + '"', '"' + str(logging['article_link']) + '"', '"' + str(logging['articles_news_org']) + '"', logging['article_bias_score'],  '"' +str(logging['device_id']) + '"', '"' + str(logging['device_interface']) + '"', '"' + str(logging['click_timestamp'])+'"')
		)
		cur.close()
		return("ENTRY_CREATED")


app.run()











