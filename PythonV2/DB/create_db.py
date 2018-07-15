import pymysql
from DB.tables import create_table_tags
from DB.tables import insert_default_data_to_table_tags
from DB.tables import create_table_posts
from DB.tables import create_table_video
from DB.tables import create_table_single_photo
from DB.tables import create_table_logs_publications
from local_data import db

if __name__ == '__main__':
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        create_table_tags.create_table_tags(connection)
        insert_default_data_to_table_tags.insert_default_data_to_table_tags(connection)
        create_table_single_photo.create_table_single_photo(connection)
        create_table_posts.create_table_posts(connection)
        create_table_video.create_table_video(connection)
        create_table_logs_publications.create_table_logs_publications(connection)

    except Exception as e:
        print(e)

    finally:
        connection.close()
