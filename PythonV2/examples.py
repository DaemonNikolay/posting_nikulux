import vk_api
import requests
import json
from local_data import db


def main():

    path = 'local_data/videos.json'
    file_video = open(path, 'r', encoding='utf8')
    content = json.loads(file_video.read())
    file_video.close()

    print(content['video'][1])
    
    
    
    # """ Пример загрузки фото """
    # 
    # login, password = '89618754106', 'ubgcfy22331'
    # vk_session = vk_api.VkApi(login, password, scope='wall, messages, photos, video')
    # 
    # try:
    #     vk_session.auth(token_only=True)
    # except vk_api.AuthError as error_msg:
    #     print(error_msg)
    #     return
    # 
    # vk = vk_session.get_api()
    # 
    # response = vk.video.save(description='This is text',
    #                          # отсутствие текста или символ пробела говорит о том, что нужно использовать текст по default из видео
    #                          link='https://www.youtube.com/watch?v=RK1K2bCg4J8',
    #                          group_id=db.GroupTest.group_id,
    #                          album_id=db.GroupTest.album_id_video)
    # 
    # attachment = '{0}{1}_{2}'.format('video', response['owner_id'], response['video_id'])
    # 
    # query = requests.get(url=response['upload_url'])
    # print(query.text)
    # query.close()
    # 
    # vk.wall.post(owner_id=-db.GroupTest.owner_id,
    #              from_group=db.GroupTest.from_group,
    #              message='Test video 1',
    #              attachments=attachment)
    # 
    # print(response)


if __name__ == '__main__':
    main()
