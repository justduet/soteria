

import urllib.parse
import boto3
import hashlib
import re
from lib import pymysql


s3 = boto3.client('s3')


def calculate_hash(content):
    sha256 = hashlib.sha256()
    sha256.update(content)
    return sha256.hexdigest()


def lambda_handler(event, context):
    
    # get the object from the event, 
    # add hash + timestamp if it's not a thumbnail
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        
        print("key: " + key)
        if (re.search(r'\.(jpe?g|png)$', key) and not
            re.search(r'-([0-9]{1,6}x[0-9]{1,6}|scaled)\.(jpe?g|png)$', key)):
            
            # read the object's content
            # calculate the hash
            image_hash = calculate_hash(response['Body'].read())
            
            # save new file containing hash to s3
            new_key = key + '.hash'
            s3.put_object(Bucket=bucket, Key=new_key, Body=image_hash)
            
            
            # MySQL connection detail 
            # Connect to MySQL
            connection = pymysql.connect(
                host = 'ls-eb80f01475f58c75e5a6a7fb7198a542bc959961.c6sougbexbsi.us-west-2.rds.amazonaws.com',
                user = 'wpteriauser',
                password = 'Phei2eghpavCei4Quaeloh4huZaey4fuot4Iela',
                database = 'wpteria')

            # host=host, user=user, password=password, database=database)
            
            cursor = connection.cursor()
        
            ## find the post_id for this image in wordpress
            select_query = "SELECT ID FROM wp_posts WHERE post_type = 'attachment' AND guid LIKE %s"
            cursor.execute(select_query, ('%' + key))
            result_set = cursor.fetchall()
            post_id = result_set[0][0]
    
            # Check whether the image hash already exists in WordPress
            check_query = "SELECT * FROM wp_postmeta WHERE post_id = %s AND meta_key = 'custom_hash' AND meta_value = %s;"
            cursor.execute(check_query, (post_id, image_hash))
            existing_hash = cursor.fetchall()
            
            # If the image hash doesn't exist, insert it
            if not existing_hash:
                insert_query = "INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (%s, 'custom_hash', %s);"
                cursor.execute(insert_query, (post_id, image_hash))
            
            # Commit the changes
            connection.commit()

            
            return new_key

        # return (key)
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    