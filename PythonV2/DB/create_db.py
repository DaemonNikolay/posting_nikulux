import pymysql
from local_data import db


def create_table_tags(connection):
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE tags(
                        id int AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR (20)
                    )"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull create table "tags"')

    except Exception as e:
        print('Create table tags. Exception: {0}'.format(e))


def create_table_single_photo(connection):
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE single_image(
                        id int UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                        path VARCHAR(25) NOT NULL,
                        message VARCHAR(50),
                        caption VARCHAR(50),
                        tag int NOT NULL,
                        FOREIGN KEY (tag) REFERENCES tags(id) ON UPDATE CASCADE ON DELETE RESTRICT
                    )"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull create table "single_photo"')

    except Exception as e:
        print('Create table single_photo. Exception: {0}'.format(e))


if __name__ == '__main__':
    connection = pymysql.connect(host=db.host,
                                 user=db.user,
                                 db=db.db,
                                 password=db.password,
                                 charset=db.charset)

    create_table_tags(connection)
    create_table_single_photo(connection)

    connection.close()
