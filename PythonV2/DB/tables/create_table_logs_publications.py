def create_table_logs_publications(connection):
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE logs_publications(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        text VARCHAR(255) NOT NULL,
                        type_publication ENUM('posts', 'humor', 'video'),
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                  )"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull create table "logs_publications"')

    except Exception as e:
        print('Create table "logs_publications". Exception: {0}'.format(e))
