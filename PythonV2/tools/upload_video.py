import vk_api
import pymysql
import os
import json
import requests
from local_data import db


def auth():
    login, password = db.PrivateDataVk.login, db.PrivateDataVk.password
    vk_session = vk_api.VkApi(login, password, scope=db.PrivateDataVk.scope)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        return 'Auth crash: ' + str(error_msg)

    return vk_session


def insert_video(message, attachments, tag):
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql = """INSERT INTO video (message, attachments, tag) 
                            VALUES ('{0}','{1}','{2}')""".format(message, attachments, tag)
            cursor.execute(sql)
            connection.commit()

        print('Video  "{0}" - successfully!'.format(message))

        return cursor.fetchone()

    except Exception as e:
        print('Error INSERT video: Exception: {0}'.format(e))

    finally:
        connection.close()


def main():
    vk = auth()
    if (str(vk).startswith('Auth crash')):
        print(vk)
        return

    path = '../local_data/video.json'

    if not os.path.isfile(path):
        print('File "{0}" not found!'.format(path))
        return

    file_posts = open(path, 'r', encoding='utf8')
    content = json.loads(file_posts.read())
    file_posts.close()

    vk_use_api = vk.get_api()

    is_continue = False

    for element in content['video']:
        attachments = ''
        tag = element['tag_id']

        for video_link in element['links']:
            try:
                response = vk_use_api.video.save(description=tag,
                                                 link=video_link,
                                                 group_id=db.Group.group_id,
                                                 album_id=db.Group.album_id_video)

                try:
                    query = requests.get(url=response['upload_url'])
                    attachments += '{0}{1}_{2},'.format('video', response['owner_id'], response['video_id'])

                except Exception as e:
                    print('Query - Exception: {0}'.format(e))
                finally:
                    query.close()

                is_continue = True

            except Exception as e:
                print('Video save - Exception: {0}'.format(e))

        if is_continue:
            message = element['message']
            attachments = attachments[0:len(attachments) - 1]

            insert_video(message=message,
                         attachments=attachments,
                         tag=tag)


if __name__ == '__main__':
    main()
