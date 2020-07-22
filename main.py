import requests
import os
import random
from dotenv import load_dotenv


def download_image_from_xkcd():
    number_of_choice = random.randint(1, 2334)
    url = f'http://xkcd.com/{number_of_choice}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response_from_xkcd = response.json()
    image_response = response.json()['img']
    file_response = requests.get(image_response)
    filename_response = response.json()['title']
    with open(filename_response + '.png', 'wb') as file:
        file.write(file_response.content)
    return response_from_xkcd


def upload_file_to_vk(client_key_vk, group_id_vk, response_from_xkcd):
    filename = response_from_xkcd['title']
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
    vk_response = requests.post(url_for_save, params=parameters)
    vk_response.raise_for_status()
    save_response = vk_response.json()
    return save_response


def publish_file_on_wall_vk(
        client_key_vk, owner_id_vk, user_id_vk,
        file_save_on_server_vk,
        response_from_xkcd
        ):
    filename = response_from_xkcd['title']
    comment = response_from_xkcd['alt']
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
    os.remove(f'{filename}.png')


def main():
    load_dotenv()
    client_key_vk = os.getenv('access_key')
    group_id_vk = os.getenv('access_group_id_vk')
    owner_id_vk = os.getenv('access_owner_id_vk')
    user_id_vk = os.getenv('access_user_id_vk')
    response_from_xkcd = download_image_from_xkcd()
    file_on_server_vk = upload_file_to_vk(
        client_key_vk,
        group_id_vk, response_from_xkcd
        )
    file_save_on_server_vk = save_file_to_vk(
        client_key_vk, group_id_vk, user_id_vk,
        file_on_server_vk
        )
    publish_file_on_wall_vk(
        client_key_vk, owner_id_vk, user_id_vk,
        file_save_on_server_vk, response_from_xkcd
        )


if __name__ == '__main__':
    main()
