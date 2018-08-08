def create_table_tags(connection):
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE tags(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        tag VARCHAR (40) UNIQUE 
                    )"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull create table "tags"')

    except Exception as e:
        print('Create table "tags". Exception: {0}'.format(e))
