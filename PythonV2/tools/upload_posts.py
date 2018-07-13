import os
import json
from local_data import db


def main():
    path = '../local_data/posts.json'

    with open(path, 'r') as file_posts:
        content = json.loads(file_posts.read())

    print(content['posts'][0]['title'])


if __name__ == '__main__':
    main()
