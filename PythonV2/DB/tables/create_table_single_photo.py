def create_table_single_photo(connection):
    try:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE single_image(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        attachments VARCHAR(255) NOT NULL,
                        caption_photo VARCHAR(50),
                        tag INT NOT NULL DEFAULT 1,
                        used ENUM('0', '1') DEFAULT '0',
                        FOREIGN KEY (tag) REFERENCES tags(id) ON UPDATE CASCADE ON DELETE CASCADE 
                    )"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull create table "single_photo"')

    except Exception as e:
        print('Create table "single_photo". Exception: {0}'.format(e))
