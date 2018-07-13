import pymysql
from local_data import db

def create_table_tags(connection):
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE tags(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        tag VARCHAR (40)
                    )"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull create table "tags"')

    except Exception as e:
        print('Create table "tags". Exception: {0}'.format(e))


def create_table_single_photo(connection):
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE single_image(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        attachments VARCHAR(255) NOT NULL,
                        caption_photo VARCHAR(50),
                        tag INT NOT NULL,
                        FOREIGN KEY (tag) REFERENCES tags(id) ON UPDATE CASCADE ON DELETE CASCADE 
                    )"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull create table "single_photo"')

    except Exception as e:
        print('Create table "single_photo". Exception: {0}'.format(e))


def create_table_posts(connection):
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE posts(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        message VARCHAR(255) NOT NULL,
                        attachments VARCHAR(255),
                        url VARCHAR(255),
                        tag INT NOT NULL,
                        FOREIGN KEY (tag) REFERENCES tags(id) ON UPDATE CASCADE ON DELETE CASCADE 
                    )"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull create table "posts"')

    except Exception as e:
        print('Create table "posts". Exception: {0}'.format(e))


if __name__ == '__main__':
    connection = pymysql.connect(host=db.host,
                                 user=db.user,
                                 db=db.db,
                                 password=db.password,
                                 charset=db.charset)

    create_table_tags(connection)
    create_table_single_photo(connection)
    create_table_posts(connection)

    connection.close()
