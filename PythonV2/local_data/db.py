class Database:
    host = 'localhost'
    username = 'root'
    password = ''  # rfgbnfy
    name_db = 'postinger-python'
    charset = 'utf8mb4'


class Group:
    album_id_img = 253996367  # 254584117
    album_id_video = 1  # 21
    group_id = 155660424  # 145125017
    owner_id = group_id
    from_group = 1


class PrivateDataVk:
    login = '89529333095'
    password = 'pbvjdfybt4'
    scope = 'wall, messages, photos, video'
    user_id = 445418216


class Nikulux:
    base_url = 'http://nikulux.ru'


class TypePublication:
    posts = 'posts'
    humor = 'humor'
    video = 'video'
    auth = 'auth'
    select = 'select'
    update = 'update'
    publication = 'publication'


class Publications:
    timer_to_seconds = 7200


class General:
    path_to_images_posts = '../images/posts'
    path_to_posts = '../local_data/posts.json'
