def insert_default_data_to_table_tags(connection):
    try:
        with connection.cursor() as cursor:
            sql = """INSERT INTO tags (tag) VALUES ('#it_umor_nikulux')"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull insert data to table "tags"')

    except Exception as e:
        print('Insert data to table "tags". Exception: {0}'.format(e))
