from local_data import db


def create_table_logs_publications(connection):
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE logs_publications(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        text TEXT NOT NULL,
                        type_publication ENUM('{0}', '{1}', '{2}', '{3}', '{4}', '{5}'),
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                  )""".format(db.TypePublication.posts,
                              db.TypePublication.humor,
                              db.TypePublication.video,
                              db.TypePublication.select,
                              db.TypePublication.update,
                              db.TypePublication.auth)

            cursor.execute(sql)

        connection.commit()
        print('Successfull create table "logs_publications"')

    except Exception as e:
        print('Create table "logs_publications". Exception: {0}'.format(e))
