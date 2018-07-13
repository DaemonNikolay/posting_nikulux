def create_table_posts(connection):
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE posts(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        content VARCHAR(500) NOT NULL,
                        attachments VARCHAR(200),
                        url VARCHAR(255),
                        tag INT NOT NULL,
                        used ENUM('0', '1') DEFAULT '0',
                        FOREIGN KEY (tag) REFERENCES tags(id) ON UPDATE CASCADE ON DELETE CASCADE 
                    )"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull create table "posts"')

    except Exception as e:
        print('Create table "posts". Exception: {0}'.format(e))