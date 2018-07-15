import vk_api
import os
import json
import pymysql
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


def insert_post(description, attachments, url, tag):
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql = """INSERT INTO posts (content, attachments, url, tag) 
                            VALUES ('{0}','{1}','{2}','{3}')""".format(description, attachments, url, tag)
            cursor.execute(sql)
            connection.commit()

        return cursor.fetchone()

    except Exception as e:
        print('Error INSERT: Exception: {0}'.format(e))

    finally:
        connection.close()


def main():
    vk = auth()
    if (str(vk).startswith('Auth crash')):
        print(vk)
        return

    path = '../local_data/posts.json'

    if not os.path.isfile(path):
        print('File "{0}" not found!'.format(path))
        return

    file_posts = open(path, 'r', encoding='utf8')
    content = json.loads(file_posts.read())
    file_posts.close()

    upload = vk_api.VkUpload(vk)
    vk_use_api = vk.get_api()

    path_to_images_posts = '../images/posts'
    for element in content['posts']:
        description = '{0}\n\n{1}'.format(element['title'],
                                          element['description'])

        try:
            upload.photo('{0}/{1}'.format(path_to_images_posts, element['attachment']),
                         album_id=db.Group.album_id_img,
                         group_id=db.Group.group_id)

            address_server = vk_use_api.photos.getWallUploadServer(group_id=db.Group.group_id)
            upload_photo = json.loads(requests.post(address_server['upload_url'], files={
                'photo': open('{0}/{1}'.format(path_to_images_posts, element['attachment']), 'rb')
            }).text)

            response = vk_use_api.photos.saveWallPhoto(group_id=db.Group.group_id,
                                                       photo=upload_photo['photo'],
                                                       server=upload_photo['server'],
                                                       hash=upload_photo['hash'])

            attachment = 'photo{0}_{1}'.format(response[0]['owner_id'], response[0]['id'])

            url = element['url']
            tag = element['tag_id']

            insert_post(description=description, attachments=attachment, url=url, tag=tag)

            print('Article "{0}" - successfully!'.format(element['title']))

        except Exception as e:
            print('Article "{0}": Exception{1}'.format(element['title'], e))


if __name__ == '__main__':
    main()
