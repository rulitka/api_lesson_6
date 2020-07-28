import requests
import os
import logging
import random
from dotenv import load_dotenv


def get_response_from_site(url):
    response = requests.get(url)
    response.raise_for_status()
    response_from_site = response.json()
    return response_from_site


def find_last_comics():
    url = 'http://xkcd.com/info.0.json'
    response_from_site = get_response_from_site(url)
    last_comics_xkcd = response_from_site['num']
    return last_comics_xkcd


def find_random_comics():
    last_comics_xkcd = find_last_comics()
    random_number = random.randint(1, last_comics_xkcd)
    return random_number


def get_image_from_xkcd():
    number_of_choice = find_random_comics()
    url = f'http://xkcd.com/{number_of_choice}/info.0.json'
    response_from_xkcd = get_response_from_site(url)
    return response_from_xkcd


def download_image_from_xkcd(image_response, filename):
    file_url = requests.get(image_response)
    with open(filename + '.png', 'wb') as file:
        file.write(file_url.content)


def upload_file_to_vk(client_key_vk, group_id_vk, filename):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    access_vk = {
        'access_token': client_key_vk, 'v': '5.120',
        'access rights': 'photos', 'group_id': group_id_vk
        }
    server_response = requests.get(url, params=access_vk)
    server_response.raise_for_status()
    url_response = server_response.json()['response']['upload_url']
    with open(f'{filename}.png', 'rb') as file:
        url_for_upload = url_response
        files = {'photo': file}
        upload_response = requests.post(url_for_upload, files=files)
        upload_response.raise_for_status()
    return upload_response


def save_file_to_vk(client_key_vk, group_id_vk, user_id_vk, file_on_server_vk):
    photo_response = file_on_server_vk.json()['photo']
    server_response = file_on_server_vk.json()['server']
    hash_response = file_on_server_vk.json()['hash']
    url_for_save = 'https://api.vk.com/method/photos.saveWallPhoto'
    parameters = {
        'access_token': client_key_vk, 'access rights': 'photos',
        'user_id': user_id_vk, 'group_id': group_id_vk,
        'photo': photo_response, 'server': server_response,
        'hash': hash_response, 'v': '5.120'
        }
    try:
        vk_response = requests.post(url_for_save, params=parameters)
        vk_response.raise_for_status()
        save_response = vk_response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.exception(f'HTTP error occurred: {http_err}')
    except Exception as err:
        logging.exception(f'Other error occurred: {err}')
    return save_response


def publish_file_on_wall_vk(
        client_key_vk, owner_id_vk, user_id_vk,
        file_save_on_server_vk,
        comment
        ):
    url_for_publish = 'https://api.vk.com/method/wall.post'
    owner_id = file_save_on_server_vk['response'][0]['owner_id']
    media_id = file_save_on_server_vk['response'][0]['id']
    access_vk = {
        'access_token': client_key_vk,
        'access rights': 'wall', 'v': '5.120',
        'owner_id': owner_id_vk, 'friends_only': 0,
        'from_group': 1, 'message': comment,
        'attachments': f"photo{owner_id}_{media_id}"
    }
    response = requests.post(url_for_publish, params=access_vk)
    response.raise_for_status()


def remove_file_from_folder(
        filename
        ):
    os.remove(f'{filename}.png')


def main():
    load_dotenv()
    client_key_vk = os.getenv('ACCESS_TOKEN_VK')
    group_id_vk = os.getenv('ACCESS_GROUP_ID_VK')
    owner_id_vk = os.getenv('ACCESS_OWNER_ID_VK')
    user_id_vk = os.getenv('ACCESS_USER_ID_VK')
    response_from_xkcd = get_image_from_xkcd()
    filename = response_from_xkcd['title']
    comment = response_from_xkcd['alt']
    image_response = response_from_xkcd['img']
    download_image_from_xkcd(image_response, filename)
    file_on_server_vk = upload_file_to_vk(
        client_key_vk,
        group_id_vk, filename
        )
    file_save_on_server_vk = save_file_to_vk(
        client_key_vk, group_id_vk, user_id_vk,
        file_on_server_vk
        )
    publish_file_on_wall_vk(
        client_key_vk, owner_id_vk, user_id_vk,
        file_save_on_server_vk, comment
        )
    remove_file_from_folder(
        filename
        )


if __name__ == '__main__':
    main()
