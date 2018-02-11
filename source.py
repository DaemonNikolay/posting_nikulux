def upload_vk(vk_api,
              url_img,
              url_caption,
              text
              ):
    import requests
    import json
    import wget
    import os
    import constant

    group_id = constant.group_id  # реальная группа

    upload_url = vk_api.photos.getWallUploadServer(group_id = group_id)
    upload_url = upload_url['upload_url']

    url = url_img
    filename = wget.download(url)
    os.rename(filename, u'' + os.getcwd() + '/' + "1.jpg")

    rs = requests.post(upload_url, files = {'photo': open('1.jpg', 'rb')})
    os.remove('1.jpg')
    rs = json.loads(rs.text)

    savePhoto = vk_api.photos.saveWallPhoto(gid = group_id,
                                            hash = rs['hash'],
                                            photo = rs['photo'],
                                            server = rs['server'],
                                            caption = url_caption)

    var = savePhoto[0]['id'] + "," + url_caption

    vk_api.wall.post(owner_id = -group_id, message = text, attachments = var)


def upload_img_vk(url_img,
                  vk_api
                  ):
    import requests
    import json
    import wget
    import os
    import constant

    group_id = constant.group_id  # реальная группа
    text = '#it_umor_nikulux',

    upload_url = vk_api.photos.getWallUploadServer(group_id = group_id)
    upload_url = upload_url['upload_url']

    url = url_img
    filename = wget.download(url)
    os.rename(filename, u'' + os.getcwd() + '/' + "1.jpg")

    rs = requests.post(upload_url, files = {'photo': open('1.jpg', 'rb')})
    os.remove('1.jpg')
    rs = json.loads(rs.text)

    savePhoto = vk_api.photos.saveWallPhoto(gid = group_id,
                                            hash = rs['hash'],
                                            photo = rs['photo'],
                                            server = rs['server']
                                            )

    var = savePhoto[0]['id']

    vk_api.wall.post(owner_id = -group_id, message = text, attachments = var)


def upload_gif_vk(vk_api,
                  url_img,
                  url_caption,
                  text
                  ):
    import requests
    import json
    import wget
    import os
    import constant

    group_id = constant.group_id

    upload_url = vk_api.docs.getWallUploadServer(group_id = group_id)
    upload_url = upload_url['upload_url']

    url = url_img
    filename = wget.download(url)
    os.rename(filename, u'' + os.getcwd() + '/' + "2.gif")

    rs = requests.post(upload_url, files = {'file': open('2.gif', 'rb')})
    os.remove('2.gif')
    rs = json.loads(rs.text)

    saveGif = vk_api.docs.save(file = rs['file'])

    var = saveGif[0]['url']

    vk_api.wall.post(owner_id = -group_id, message = text, attachments = var)


def upload_video_vk(vk_api,
                    link,
                    text
                    ):
    import constant

    group_id = constant.group_id

    vk_api.wall.post(owner_id = -group_id, message = text, attachments = link)


def upload_telegram(token = '443016858:AAEfK2ZuxgvxrI2ctbozfFLtSoY8Oj1KB6Q',
                    caption_img = 'http://nikulux.ru',
                    url_img = '',
                    url_caption = '',
                    text = ''
                    ):
    import requests
    import constant

    token = token
    chat_id_canal = constant.chat_id_canal

    res = requests.Session()
    res.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}'.format(token,
                                                                                      chat_id_canal,
                                                                                      text))
    if (url_img != ''):
        res.get('https://api.telegram.org/bot{0}/sendPhoto?chat_id={1}&photo={2}&caption={3}'.format(token,
                                                                                                     chat_id_canal,
                                                                                                     url_img,
                                                                                                     url_caption))

    res.close()


def upload_img_telegram(token = '443016858:AAEfK2ZuxgvxrI2ctbozfFLtSoY8Oj1KB6Q',
                        url_img = '',
                        url_caption = '#it_umor_nikulux',
                        ):
    import requests
    import constant

    token = token
    chat_id_canal = constant.chat_id_canal

    res = requests.Session()

    if (url_img != ''):
        res.get('https://api.telegram.org/bot{0}/sendPhoto?chat_id={1}&photo={2}&caption={3}'.format(token,
                                                                                                     chat_id_canal,
                                                                                                     url_img,
                                                                                                     url_caption))

    res.close()


def upload_video_telegram(url_video,
                          text_tel_video
                          ):
    import requests
    import constant

    token = constant.token
    chat_id_canal = constant.chat_id_canal

    res = requests.Session()

    for element in url_video:
        element = text_tel_video + " (" + element + ")"
        res.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}'.format(token,
                                                                                          chat_id_canal,
                                                                                          element
                                                                                          ))

    res.close()


def update1(sql):
    import pymysql
    import constant

    conn = pymysql.connect(host = constant.host,
                           user = constant.user,
                           passwd = constant.passwd,
                           db = constant.db,
                           charset = constant.charset,
                           init_command = constant.init_command
                           )
    cursor = conn.cursor()

    cursor.execute(sql)
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()

    conn.close()


def select1(sql):
    import pymysql
    import constant

    conn = pymysql.connect(host = constant.host,
                           user = constant.user,
                           passwd = constant.passwd,
                           db = constant.db,
                           charset = constant.charset,
                           init_command = constant.init_command
                           )
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    conn.close()

    return row


import vk
import time, datetime
import random


def update(id):
    sql = """UPDATE data_post SET send=TRUE WHERE id = %s LIMIT 1""" % id
    update1(sql = sql)


def update_img(id):
    sql = """UPDATE data_post_img SET send=TRUE WHERE id = %s LIMIT 1""" % id
    update1(sql = sql)


def update_video(id):
    sql = """UPDATE data_post_video SET send=TRUE WHERE id = %s LIMIT 1""" % id
    update1(sql = sql)


def select():
    option = random.randint(0, 2)
    if (option == 0):
        sql_select = "SELECT * FROM data_post WHERE send = FALSE LIMIT 1"
    elif (option == 1):
        sql_select = "SELECT * FROM data_post_video WHERE send = FALSE LIMIT 1"
    elif (option == 2):
        sql_select = "SELECT * FROM data_post_img WHERE send = FALSE LIMIT 1"

    return select1(sql = sql_select)


def timer_sleep():
    import constant
    date_posting = datetime.datetime.today() + datetime.timedelta(hours = 3)
    link = constant.address + "Следующая публикация будет " + str(date_posting.strftime("%Y-%m-%d %H:%M:%S"))
    requests.Session().get(link)
    requests.Session().close()
    time.sleep(10800)


import constant

id_application = constant.id_application
login = constant.login
password = constant.password

session = vk.AuthSession(app_id = id_application, user_login = login, user_password = password, scope = 'wall, messages, photos, docs, video')
vk_api = vk.API(session = session, v = '5.35', lang = 'ru')

import datetime

while (1):
    import requests

    address = constant.address

    try:
        if (datetime.datetime.now().hour >= 0 and datetime.datetime.now().hour < 8):
            time.sleep(1200)
            continue

        res = select()
        if (len(res) == 0):
            continue

        if (len(res[0]) == 5):
            id = res[0][0]
            url_img = res[0][1]
            url_caption = res[0][2]
            text = res[0][3]

            upload_vk(url_img = url_img, url_caption = url_caption, text = text, vk_api = vk_api)
            upload_telegram(url_img = url_img, url_caption = url_caption, text = text)

            requests.Session().get(
                address + "Пост выложен\n" + str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
            requests.Session().close()

            update(id = id)

        elif (len(res[0]) == 14):
            print("-----------------------------")
            id_video = res[0][0]
            text_video = res[0][1]
            text_telegram_video = res[0][2]
            video0 = str(res[0][3]).split("/")
            video1 = str(res[0][4]).split("/")
            video2 = str(res[0][5]).split("/")
            video3 = str(res[0][6]).split("/")
            video4 = str(res[0][7]).split("/")
            video5 = str(res[0][8]).split("/")
            video6 = str(res[0][9]).split("/")
            video7 = str(res[0][10]).split("/")
            video8 = str(res[0][11]).split("/")
            video9 = str(res[0][12]).split("/")

            # label = str(video0[3] + "," + video1[3] + "," + video2[3] + "," + video3[3] + "," + video4[3])
            list_urls = []
            for i in range(3, 13):
                if (len(res[0][i]) > 1):
                    list_urls.append(res[0][i])

            result = ""
            list_video_to_vk = [video0, video1, video2, video3, video4, video5, video6, video7, video8, video9]
            for i in range(0, 10):
                if (len(list_video_to_vk[i]) > 1):
                    result += str(list_video_to_vk[i][3]) + " ,"

            result = result[0:len(result) - 1]

            print(result)

            upload_video_vk(vk_api = vk_api, text = text_video, link = result)
            upload_video_telegram(url_video = list_urls, text_tel_video = text_telegram_video)

            requests.Session().get(
                address + "Видео выложено\n" + str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
            requests.Session().close()

            update_video(id = id_video)

        elif (len(res[0]) == 3):
            id_img = res[0][0]
            url_img_post = res[0][1]

            upload_img_vk(url_img = url_img_post, vk_api = vk_api)
            upload_img_telegram(url_img = url_img_post)

            requests.Session().get(
                address + "Изображение выложено\n" + str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
            requests.Session().close()

            update_img(id = id_img)

        print(" Успех " + datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
        timer_sleep()

    except KeyError as e:
        address_error = address + str(e) + " не решено\n" + str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
        requests.Session().get(address_error)
        requests.Session().close()

        session = vk.AuthSession(id_application, login, password, scope = 'wall, messages, photos, docs, video')
        vk_api = vk.API(session)

        address_error = address + str(e) + " решено\n" + str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
        requests.Session().get(address_error)
        requests.Session().close()

    except Exception as e:
        print(e)
        address_error = address + str(e) + " КЕРДЫК!!! \n" + str(
            datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
        requests.Session().get(address_error)
        requests.Session().close()
        time.sleep(1800)
