import vk_api
import requests
import json
import os
import pymysql
from local_data import db


def auth():
    login, password = db.PrivateDataVk.login, db.PrivateDataVk.password
    vk_session = vk_api.VkApi(login, password, scope=db.PrivateDataVk.scope)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        return 'Auth crash: ' + str(error_msg)

    # return vk_session.get_api()
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
    vk = auth()
    if (str(vk).startswith('Auth crash')):
        print(vk)
        return

    connection = pymysql.connect(host=db.Database.host,
                                 user=db.Database.username,
                                 db=db.Database.name_db,
                                 password=db.Database.password,
                                 charset=db.Database.charset)

    path_to_images = '../images/single_photo'
    upload = vk_api.VkUpload(vk)

    for name_image in os.listdir(path_to_images):
        try:
            # address_server = vk.photos.getWallUploadServer(group_id=db.GroupTest.group_id)
            # upload_photo = json.loads(requests.post(address_server['upload_url'], files={
            #     'photo': open('{0}/{1}'.format(path_to_images, name_image), 'rb')
            # }).text)
            #
            # response = vk.photos.saveWallPhoto(group_id=db.GroupTest.group_id,
            #                                    photo=upload_photo['photo'],
            #                                    server=upload_photo['server'],
            #                                    hash=upload_photo['hash'])
            #
            # print(response)
            #
            # attachment = 'photo{0}_{1}'.format(response[0]['owner_id'], response[0]['id'])


            photo = upload.photo('{0}/{1}'.format(path_to_images, name_image),
                                 album_id=db.GroupTest.album_id,
                                 group_id=db.GroupTest.group_id
                                 )

            attachment = 'photo{0}_{1}'.format(
                (photo[0]['owner_id'] * (-1)), photo[0]['id']
            )

            insert_attachments_to_db(connection, attachment, name_image)

        except Exception as e:
            print('File: {0} - Exception: {1}'.format(name_image, e))

    connection.close()


if __name__ == '__main__':
    main()
