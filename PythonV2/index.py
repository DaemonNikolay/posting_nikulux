import vk_api
import requests
import json


def main():
    """ Пример загрузки фото """

    login, password = '89618754106', 'ubgcfy22331'
    vk_session = vk_api.VkApi(login, password, scope='wall, messages, photos, video')

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    """ В VkUpload реализованы методы загрузки файлов в ВК
    """

    # upload = vk_api.VkUpload(vk_session)
    #
    # photo = upload.photo(  # Подставьте свои данные
    #     'images/single_photo/1.jpg',
    #     album_id=247772750,
    #     group_id=155660424
    # )
    #
    # vk_photo_url = 'https://vk.com/photo{}_{}'.format(
    #     photo[0]['owner_id'], photo[0]['id']
    # )
    #
    # print(photo, '\nLink: ', vk_photo_url)

    vk = vk_session.get_api()

    address_server = vk.photos.getWallUploadServer(group_id=155660424)
    upload_photo = json.loads(requests.post(address_server['upload_url'], files={
        'photo': open('images/single_photo/1.jpg', 'rb')
    }).text)

    response = vk.photos.saveWallPhoto(group_id=155660424,
                                       photo=upload_photo['photo'],
                                       server=upload_photo['server'],
                                       hash=upload_photo['hash'],
                                       caption='Testing image')

    attachments = 'photo{0}_{1}'.format(response[0]['owner_id'], response[0]['id'])

    print(attachments)
    # attachments = 'photo' + str(response[0]['owner_id']) + '_' + ''

    vk.wall.post(owner_id=-155660424,
                 from_group=1,
                 message='Test 2',
                 attachments=attachments)


if __name__ == '__main__':
    main()
