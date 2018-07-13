import vk_api
import pymysql
from local_data import db


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


def select_humor():
    try:
        connection = pymysql.connect(host=db.Database.host,
                                     user=db.Database.username,
                                     db=db.Database.name_db,
                                     password=db.Database.password,
                                     charset=db.Database.charset)

        with connection.cursor() as cursor:
            sql = """SELECT single_image.attachments, single_image.caption_photo, tags.tag 
                     FROM tags 
                        LEFT JOIN single_image 
                        ON single_image.tag = tags.id 
                     WHERE single_image.used='0' 
                     LIMIT 1"""
            cursor.execute(sql)

            return cursor.fetchone()

    except Exception as e:
        print(e)

    finally:
        connection.close()


def main():
    vk = auth()

    if (str(vk).startswith('Auth crash')):
        print(vk)
        return

    humor = select_humor()
    attachment = '{0},{1}'.format(humor[0], db.Nikulux.base_url)
    message = humor[2]

    publication_humor = vk.wall.post(owner_id=-db.GroupTest.owner_id,
                                     from_group=db.GroupTest.from_group,
                                     message=message,
                                     attachments=attachment)

    print(publication_humor)


if __name__ == '__main__':
    main()
