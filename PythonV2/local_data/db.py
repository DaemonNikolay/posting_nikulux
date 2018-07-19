class Database:
    host = 'localhost'
    username = 'root'
    password = ''
    name_db = 'postinger-python'
    charset = 'utf8mb4'


class Group:
    album_id_img = 253996367
    album_id_video = 1
    group_id = 155660424
    owner_id = group_id
    from_group = 1


class PrivateDataVk:
    login = '89618754106'
    password = 'ubgcfy22331'
    scope = 'wall, messages, photos, video'


class Nikulux:
    base_url = 'http://nikulux.ru'


class TypePublication:
    posts = 'posts'
    humor = 'humor'
    video = 'video'
    auth = 'auth'
    select = 'select'
    update = 'update'


class Publications:
    timer_to_seconds = 7200

class General:
    path_to_images_posts = '../images/posts'
    path_to_posts = '../local_data/posts.json'