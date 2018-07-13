import vk_api
import pymysql
from local_data import db


# GENERAL

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


# -----------------------------

# HUMOR

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

            return cursor.fetchone()

    except Exception as e:
        print(e)

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
        return cursor.fetchone()

    except Exception as e:
        print(e)

    finally:
        connection.close()


def publication_humor(vk):
    humor = select_humor()

    if humor is None:
        print('All images are used!')
        return

    attachment = '{0},{1}'.format(humor[0], db.Nikulux.base_url)
    message = humor[2]

    try:
        vk.wall.post(owner_id=-db.GroupTest.owner_id,
                     from_group=db.GroupTest.from_group,
                     message=message,
                     attachments=attachment)

        update_used_for_table_single_image(single_image_id=humor[1])

    except Exception as e:
        print(e)


# -----------------------------


# POSTS


# -----------------------------


def main():
    vk = auth()

    if (str(vk).startswith('Auth crash')):
        print(vk)
        return

    publication_humor(vk)


if __name__ == '__main__':
    main()
