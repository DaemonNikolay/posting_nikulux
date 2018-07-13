import os
import json
from local_data import db


def main():
    path = '../local_data/posts.json'

    if not os.path.isfile(path):
        print('File "{0}" not found!'.format(path))
        return

    file_posts = open(path, 'r', encoding='utf8')
    content = json.loads(file_posts.read())
    file_posts.close()

    for element in content['posts']:
        print(element['title'])


if __name__ == '__main__':
    main()
