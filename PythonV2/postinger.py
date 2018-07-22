import vk_api
import pymysql
import random
import time
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
        log = 'Auth crash: {0}'.format(error_msg)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.auth)

        return log

    log = 'Auth is completed'
    print(log)
    creating_logs(message=log,
                  type_publication=db.TypePublication.auth)

    return vk_session.get_api()


def creating_logs(message, type_publication):
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql = """INSERT INTO logs_publications 
                     SET logs_publications.text='{0}',
                         logs_publications.type_publication='{1}'
                     """.format(message, type_publication)
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

            content = cursor.fetchone()

            log = 'Complete: "SELECT humor" - single_image.id={0}'.format(content[1])
            print(log)
            creating_logs(message=log,
                          type_publication=db.TypePublication.select)

            return content

    except Exception as e:
        log = 'Exception: "SELECT humor" - {0}'.format(e)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.select)

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

        log = 'Complete: "UPDATE used TABLE single_image" - single_image.id={0}'.format(single_image_id)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.update)

        return cursor.fetchone()

    except Exception as e:
        log = 'Exception: "UPDATE used TABLE single_image" - single_image.id={0} - {1}'.format(single_image_id, e)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.update)

    finally:
        connection.close()


def publication_humor(vk):
    humor = select_humor()

    if humor is None:
        log = 'Error: all images are used'
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.humor)

        return

    attachment = '{0},{1}'.format(humor[0], db.Nikulux.base_url)
    message = humor[2]

    try:
        vk.wall.post(owner_id=-db.Group.owner_id,
                     from_group=db.Group.from_group,
                     message=message,
                     attachments=attachment)

        log = 'Complete: publication humor - single_image.id={0}'.format(humor[1])
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.humor)

        update_used_for_table_single_image(single_image_id=humor[1])

    except Exception as e:
        log = 'Exception: publication humor - single_image.id={0} - {1}'.format(humor[1], e)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.humor)


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

            content = cursor.fetchone()

            log = 'Complete: "SELECT post" - posts.id={0}'.format(content[0])
            print(log)
            creating_logs(message=log,
                          type_publication=db.TypePublication.select)

            return content

    except Exception as e:
        log = 'Exception: "SELECT post" - {0}'.format(e)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.select)

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

        log = 'Complete: "UPDATE used TABLE posts" - posts.id={0}'.format(posts_id)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.update)

        return cursor.fetchone()

    except Exception as e:
        log = 'Exception: "UPDATE used TABLE posts" - {0}'.format(e)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.update)

    finally:
        connection.close()


def publication_post(vk):
    post = select_post()

    if post is None:
        log = 'Error: all posts are used'
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.posts)

        return

    attachment = '{0},{1}'.format(post[2], post[3])
    message = '{0}\n\n{1}'.format(post[1], post[4])

    try:
        vk.wall.post(owner_id=-db.Group.owner_id,
                     from_group=db.Group.from_group,
                     message=message,
                     attachments=attachment)

        post_id = post[0]
        log = 'Complete: Publication post - posts.id={0}'.format(post_id)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.posts)

        update_used_for_table_posts(posts_id=post[0])

    except Exception as e:
        log = ' Exception: publication post - {0}'.format(e)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.posts)


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

            content = cursor.fetchone()

            log = 'Complete: "SELECT video" - video.id={0}'.format(content[0])
            print(log)
            creating_logs(message=log,
                          type_publication=db.TypePublication.select)

            return content

    except Exception as e:
        log = 'Exception: "SELECT video" - {0}'.format(e)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.select)

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

        content = cursor.fetchone()

        log = 'Complete: "UPDATE used TABLE video" - {0}'.format(video_id)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.update)

        return cursor.fetchone()

    except Exception as e:
        log = 'Exception: "UPDATE used TABLE video" - {0}'.format(e)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.update)

    finally:
        connection.close()


def publication_video(vk):
    video = select_video()

    if video is None:
        log = 'Error: all video are used'
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.video)

        return

    video_id = video[0]
    message = '{0}\n\n{1}'.format(video[1], video[3])
    attachments = video[2]

    try:
        vk.wall.post(owner_id=-db.Group.owner_id,
                     from_group=db.Group.from_group,
                     message=message,
                     attachments=attachments)

        log = 'Complete: publication video - video.id={0}'.format(video_id)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.video)

        update_used_for_table_video(video_id=video_id)

    except Exception as e:
        log = 'Exception: publication video - {0}'.format(e)
        print(log)
        creating_logs(message=log,
                      type_publication=db.TypePublication.video)


# </VIDEO>

def main():
    vk = auth()

    if (str(vk).startswith('Auth crash')):
        print(vk)
        return

    publication_humor(vk)
    publication_post(vk)
    publication_video(vk)

    # while True:
    #     option = random.randint(0, 2)
    #
    #     if option == 0:
    #         publication_humor(vk)
    #     elif option == 1:
    #         publication_post(vk)
    #     elif option == 2:
    #         publication_video(vk)
    #
    #     time.sleep(db.Publications.timer_to_seconds)


if __name__ == '__main__':
    main()
