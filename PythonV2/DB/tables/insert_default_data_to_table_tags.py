def insert_default_data_to_table_tags(connection):
    try:
        with connection.cursor() as cursor:
            sql = """INSERT INTO tags (tag) VALUES ('#it_umor_nikulux'),
                                                   ('#smart_nikulux'),
                                                   ('#java_video_nikulux'),
                                                   ('#it_video_nikulux'),
                                                   ('#c_sharp_video_nikulux'),
                                                   ('#android_video_nikulux'),
                                                   ('#js_tasks_video_nikulux'),
                                                   ('#ajax_video_nikulux'),
                                                   ('#node_js_video_nikulux'),
                                                   ('#linux_video_nikulux'),
                                                   ('#c_c_plus_plus_nikulux'),
                                                   ('#service_nikulux'),
                                                   ('#network_nikulux'),
                                                   ('#php_nikulux'),
                                                   ('#css_html_nikulux'),
                                                   ('#python_nikulux'),
                                                   ('#java_nikulux'),
                                                   ('#c_sharp_nikulux'),
                                                   ('#python_book_nikulux'),
                                                   ('#c_sharp_book_nikulux'),
                                                   ('#java_book_nikulux ')"""
            cursor.execute(sql)

        connection.commit()
        print('Successfull insert data to table "tags"')

    except Exception as e:
        print('Insert data to table "tags". Exception: {0}'.format(e))
