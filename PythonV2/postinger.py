import vk_api
import pymysql
from local_data import db


# <GENERAL>

def auth():
    login, password = db.PrivateDataVk.login, db.PrivateDataVk.password
    vk_session = vk_api.VkApi(login=login,
                              password=password,
                              scope=db.PrivateDataVk.scope)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        return 'Auth crash: ' + str(error_msg)

    return vk_session.get_api()


def creating_logs(message):
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql = """INSERT INTO logs_publications 
                     SET logs_publications.text={0} 
                     """.format(single_image_id)
            cursor.execute(sql)

        connection.commit()
        return cursor.fetchone()

    except Exception as e:
        print(e)

    finally:
        connection.close()


# </GENERAL>

# <HUMOR>

def select_humor():
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql = """SELECT single_image.attachments, single_image.id, tags.tag 
                     FROM tags 
                        LEFT JOIN single_image 
                        ON single_image.tag = tags.id 
                     WHERE single_image.used='0' 
                     LIMIT 1"""
            cursor.execute(sql)

            return cursor.fetchone()

    except Exception as e:
        print('Exception in "SELECT humor": {0}'.format(e))

    finally:
        connection.close()


def update_used_for_table_single_image(single_image_id):
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql = """UPDATE single_image 
                     SET single_image.used='1' 
                     WHERE single_image.id={0}""".format(single_image_id)
            cursor.execute(sql)

        connection.commit()
        return cursor.fetchone()

    except Exception as e:
        print(e)

    finally:
        connection.close()


def publication_humor(vk):
    humor = select_humor()

    if humor is None:
        print('All images are used!')
        return

    attachment = '{0},{1}'.format(humor[0], db.Nikulux.base_url)
    message = humor[2]

    try:
        vk.wall.post(owner_id=-db.Group.owner_id,
                     from_group=db.Group.from_group,
                     message=message,
                     attachments=attachment)

        update_used_for_table_single_image(single_image_id=humor[1])

        print('Publication humor is completed!')

    except Exception as e:
        print('Publication humor - Exception: {0}'.format(e))


# </HUMOR>


# <POSTS>

def select_post():
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql = """SELECT posts.id, posts.content, posts.attachments, posts.url, tags.tag 
                     FROM posts 
                      LEFT JOIN tags 
                      ON posts.tag=tags.id 
                     WHERE posts.used='0' LIMIT 1"""

            cursor.execute(sql)

            return cursor.fetchone()

    except Exception as e:
        print('Exception in "SELECT post": {0}'.format(e))

    finally:
        connection.close()


def update_used_for_table_posts(posts_id):
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql = """UPDATE posts 
                     SET posts.used='1' 
                     WHERE posts.id={0}""".format(posts_id)
            cursor.execute(sql)

        connection.commit()
        return cursor.fetchone()

    except Exception as e:
        print(e)

    finally:
        connection.close()


def publication_post(vk):
    post = select_post()

    if post is None:
        print('All posts are used!')
        return

    attachment = '{0},{1}'.format(post[2], post[3])
    message = '{0}\n\n{1}'.format(post[1], post[4])

    try:
        vk.wall.post(owner_id=-db.Group.owner_id,
                     from_group=db.Group.from_group,
                     message=message,
                     attachments=attachment)

        update_used_for_table_posts(posts_id=post[0])

        print('Publication post is completed!')

    except Exception as e:
        print('Publication post - Exception: {0}'.format(e))


# </POSTS>


# <VIDEO>

def select_video():
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql = """SELECT video.id, video.message, video.attachments, tags.tag 
                     FROM tags 
                        LEFT JOIN video 
                        ON video.tag = tags.id 
                     WHERE video.used='0' 
                     LIMIT 1"""
            cursor.execute(sql)

            return cursor.fetchone()

    except Exception as e:
        print('Exception in "SELECT video": {0}'.format(e))

    finally:
        connection.close()


def update_used_for_table_video(video_id):
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql = """UPDATE video 
                     SET video.used='1' 
                     WHERE video.id={0}""".format(video_id)
            cursor.execute(sql)

        connection.commit()

        return cursor.fetchone()

    except Exception as e:
        print('UPDATE TABLE video - Exception: {0}'.format(e))

    finally:
        connection.close()


def publication_video(vk):
    video = select_video()

    if video is None:
        print('All video are used!')
        return

    video_id = video[0]
    message = '{0}\n\n{1}'.format(video[1], video[3])
    attachments = video[2]

    try:
        vk.wall.post(owner_id=-db.Group.owner_id,
                     from_group=db.Group.from_group,
                     message=message,
                     attachments=attachments)

        update_used_for_table_video(video_id=video_id)

        print('Publication video is completed!')

    except Exception as e:
        print('Publication video - Exception: {0}'.format(e))


# </VIDEO>

def main():
    vk = auth()

    if (str(vk).startswith('Auth crash')):
        print(vk)
        return

    publication_humor(vk)
    publication_post(vk)
    publication_video(vk)


if __name__ == '__main__':
    main()
