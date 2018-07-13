import vk_api
import os
import pymysql
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


def insert_attachments_to_db(connection, attachment, name_image):
    try:
        with connection.cursor() as cursor:
            sql = """INSERT INTO single_image (attachments, caption_photo) 
                     VALUES ('{0}','{1}')""".format(attachment, '#it_umor_nikulux')
            cursor.execute(sql)

        connection.commit()
        print('File: {0} - upload'.format(name_image))

    except Exception as e:
        print('File: {0} - Exception: {1}'.format(name_image, e))


def main():
    path_to_images = '../images/single_photo'
    names_images = os.listdir(path_to_images)

    if len(names_images) == 0:
        print('Directory is empty!')
        return

    vk = auth()
    if (str(vk).startswith('Auth crash')):
        print(vk)
        return

    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        upload = vk_api.VkUpload(vk)
        vk_use_api = vk.get_api()

        for name_image in names_images:
            try:
                upload.photo('{0}/{1}'.format(path_to_images, name_image),
                             album_id=db.GroupTest.album_id,
                             group_id=db.GroupTest.group_id)

                address_server = vk_use_api.photos.getWallUploadServer(group_id=db.GroupTest.group_id)
                upload_photo = json.loads(requests.post(address_server['upload_url'], files={
                    'photo': open('{0}/{1}'.format(path_to_images, name_image), 'rb')
                }).text)

                response = vk_use_api.photos.saveWallPhoto(group_id=db.GroupTest.group_id,
                                                           photo=upload_photo['photo'],
                                                           server=upload_photo['server'],
                                                           hash=upload_photo['hash'])

                attachment = 'photo{0}_{1}'.format(response[0]['owner_id'], response[0]['id'])
                insert_attachments_to_db(connection, attachment, name_image)

            except Exception as e:
                print('File: {0} - Exception: {1}'.format(name_image, e))

    except Exception as e:
        print(e)

    finally:
        connection.close()


if __name__ == '__main__':
    main()
