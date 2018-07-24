import vk_api
import pymysql
import random
import time
from datetime import datetime, timedelta
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
        log = 'Error: auth crash: {0}'.format(error_msg)
        print(log)
        logging_to_db(message=log,
                      type_publication=db.TypePublication.auth)

        return log

    vk = vk_session.get_api()

    log = 'Complete: auth is completed'
    print(log)

    logging_to_db(message=log,
                  type_publication=db.TypePublication.auth)
    logging_to_vk(vk=vk,
                  message=log)

    return vk


def is_auth(vk):
    if (str(vk).startswith('Auth crash')):
        log = f'Exception: auth crash - {vk}'
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.auth)

        return False
    return True


def logging_to_db(message, type_publication):
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


def logging_to_vk(vk, message):
    try:
        vk.messages.send(user_id=db.PrivateDataVk.user_id,
                         message=message,
                         group_id=db.Group.group_id)

    except Exception as e:
        log = f'Exception: logging to VK crash - {e}'
        print(log)
        logging_to_db(message=log,
                      type_publication=db.TypePublication.auth)


def next_time_publication():
    next_time_publication = datetime.now() + timedelta(seconds=db.Publications.timer_to_seconds)
    next_time_publication_format = next_time_publication.strftime('%Y.%m.%d %H:%M:%S')

    return f'Следующая публикация будет в: {next_time_publication_format}'


def count_materials_from_db(vk):
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql_table_posts = """SELECT COUNT(*) AS count_posts FROM posts WHERE posts.used='0'"""
            cursor.execute(sql_table_posts)
            count_posts = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            sql_table_single_image = """SELECT COUNT(*) AS count_humor FROM single_image WHERE single_image.used='0'"""
            cursor.execute(sql_table_single_image)
            count_humor = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            sql_table_video = """SELECT COUNT(*) AS count_video FROM video WHERE video.used='0'"""
            cursor.execute(sql_table_video)
            count_video = cursor.fetchone()[0]

            log = f'Complete: posts={count_posts}, humor={count_humor}, video={count_video}'
            print(log)

            logging_to_db(message=log,
                          type_publication=db.TypePublication.select)
            logging_to_vk(vk=vk,
                          message=log)

    except Exception as e:
        log = 'Exception: count materials failed - {0}'.format(e)
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.select)
        logging_to_vk(vk=vk,
                      message=log)

    finally:
        connection.close()


# </GENERAL>

# <HUMOR>

def select_humor(vk):
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

            logging_to_db(message=log,
                          type_publication=db.TypePublication.select)
            logging_to_vk(vk=vk,
                          message=log)

            return content

    except Exception as e:
        log = 'Exception: "SELECT humor" - {0}'.format(e)
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.select)
        logging_to_vk(vk=vk,
                      message=log)

    finally:
        connection.close()


def update_used_for_table_single_image(vk, single_image_id):
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

        logging_to_db(message=log,
                      type_publication=db.TypePublication.update)
        logging_to_vk(vk=vk,
                      message=log)

        return cursor.fetchone()

    except Exception as e:
        log = 'Exception: "UPDATE used TABLE single_image" - single_image.id={0} - {1}'.format(single_image_id, e)
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.update)
        logging_to_vk(vk=vk,
                      message=log)

    finally:
        connection.close()


def publication_humor(vk):
    humor = select_humor(vk=vk)

    if humor is None:
        log = 'Error: all images are used'
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.humor)
        logging_to_vk(vk=vk,
                      message=log)

        return log

    attachment = '{0},{1}'.format(humor[0], db.Nikulux.base_url)
    message = humor[2]

    try:
        vk.wall.post(owner_id=-db.Group.owner_id,
                     from_group=db.Group.from_group,
                     message=message,
                     attachments=attachment)

        log = 'Complete: publication humor - single_image.id={0}'.format(humor[1])
        print(log)
        logging_to_db(message=log,
                      type_publication=db.TypePublication.humor)
        logging_to_vk(vk=vk,
                      message=f'{log}\n{next_time_publication()}')

        update_used_for_table_single_image(vk=vk,
                                           single_image_id=humor[1])

        count_materials_from_db(vk)

    except Exception as e:
        log = 'Exception: publication humor - single_image.id={0} - {1}'.format(humor[1], e)
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.humor)
        logging_to_vk(vk=vk,
                      message=log)


# </HUMOR>


# <POSTS>

def select_post(vk):
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

            logging_to_db(message=log,
                          type_publication=db.TypePublication.select)
            logging_to_vk(vk=vk,
                          message=log)

            return content

    except Exception as e:
        log = 'Exception: "SELECT post" - {0}'.format(e)
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.select)
        logging_to_vk(vk=vk,
                      message=log)

    finally:
        connection.close()


def update_used_for_table_posts(vk, posts_id):
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

        logging_to_db(message=log,
                      type_publication=db.TypePublication.update)
        logging_to_vk(vk=vk,
                      message=log)

        return cursor.fetchone()

    except Exception as e:
        log = 'Exception: "UPDATE used TABLE posts" - {0}'.format(e)
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.update)
        logging_to_vk(vk=vk,
                      message=log)

    finally:
        connection.close()


def publication_post(vk):
    post = select_post(vk=vk)

    if post is None:
        log = 'Error: all posts are used'
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.posts)
        logging_to_vk(vk=vk,
                      message=log)

        return log

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

        logging_to_db(message=log,
                      type_publication=db.TypePublication.posts)
        logging_to_vk(vk=vk,
                      message=f'{log}\n{next_time_publication()}')

        update_used_for_table_posts(vk=vk, posts_id=post[0])

        count_materials_from_db(vk)

    except Exception as e:
        log = ' Exception: publication post - {0}'.format(e)
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.posts)
        logging_to_vk(vk=vk,
                      message=log)


# </POSTS>


# <VIDEO>

def select_video(vk):
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

            logging_to_db(message=log,
                          type_publication=db.TypePublication.select)
            logging_to_vk(vk=vk,
                          message=log)

            return content

    except Exception as e:
        log = 'Exception: "SELECT video" - {0}'.format(e)
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.select)
        logging_to_vk(vk=vk,
                      message=log)

    finally:
        connection.close()


def update_used_for_table_video(vk, video_id):
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

        log = 'Complete: "UPDATE used TABLE video" - {0}'.format(video_id)
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.update)
        logging_to_vk(vk=vk,
                      message=log)

        return cursor.fetchone()

    except Exception as e:
        log = 'Exception: "UPDATE used TABLE video" - {0}'.format(e)
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.update)
        logging_to_vk(vk=vk,
                      message=log)

    finally:
        connection.close()


def publication_video(vk):
    video = select_video(vk=vk)

    if video is None:
        log = 'Error: all video are used'
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.video)
        logging_to_vk(vk=vk,
                      message=log)

        return log

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

        logging_to_db(message=log,
                      type_publication=db.TypePublication.video)
        logging_to_vk(vk=vk,
                      message=f'{log}\n{next_time_publication()}')

        update_used_for_table_video(vk=vk, video_id=video_id)

        count_materials_from_db(vk)

    except Exception as e:
        log = 'Exception: publication video - video.id={0}'.format(e)
        print(log)

        logging_to_db(message=log,
                      type_publication=db.TypePublication.video)
        logging_to_vk(vk=vk,
                      message=log)


# </VIDEO>

def main():
    vk = auth()

    if not is_auth(vk=vk):
        return

    is_auth_failed = False
    is_publication = False

    while True:
        if is_auth_failed:
            vk = auth()

            if not is_auth(vk=vk):
                return

        try:
            option = random.randint(0, 2)

            if option == 0:
                if publication_humor(vk).find('Error') != -1:
                    is_publication = False
                else:
                    is_publication = True

            elif option == 1:
                if publication_post(vk).find('Error') != -1:
                    is_publication = False
                else:
                    is_publication = True

            elif option == 2:
                if publication_video(vk).find('Error') != -1:
                    is_publication = False
                else:
                    is_publication = True

            if is_publication:
                time.sleep(db.Publications.timer_to_seconds)

        except Exception as e:
            if str(e).lower().find('user authorization failed') != -1:
                is_auth_failed = True

            else:
                log = f'Exception: publication failed - {e}'
                print(log)

                logging_to_db(message=log,
                              type_publication=db.TypePublication.publication)
                logging_to_vk(vk=vk,
                              message=log)

                break


if __name__ == '__main__':
    main()
