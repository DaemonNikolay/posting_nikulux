def create_table_video(connection):
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE video(
                          id INT AUTO_INCREMENT PRIMARY KEY,
                          message VARCHAR(255),
                          attachments VARCHAR(255),
                          tag INT NOT NULL,
                          used ENUM('0', '1') DEFAULT '0',
                          FOREIGN KEY (tag) REFERENCES tags(id) ON UPDATE CASCADE ON DELETE CASCADE 
                      )"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull create table "video"')

    except Exception as e:
        print('Create table "video". Exception: {0}'.format(e))