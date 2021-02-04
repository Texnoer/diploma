import requests
import json
from pprint import pprint
from tqdm import tqdm
file_comp = '\Folder'
with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def get_fotos(self):
        """Параметры VK"""
        foto_url = self.url + 'photos.get'
        foto_params = {
            'owner_id': you_id,
            'album_id': 'profile',
            'count': '5',
            'photo_sizes': True,
            'extended': True
            }
        photos = requests.get(foto_url, params={**self.params, **foto_params})
        return photos.json().get('response', {}).get('items', [])

    def get_largest(self, size_dict):
        """Функция ищет наибольший размер картинки"""
        if size_dict['width'] >= size_dict['height']:
            return size_dict['width']
        else:
            return size_dict['height']

    def sizes_max(self):
        """Цикл поиска фото наибольшего размера"""
        self.list_photo = []
        for photo in self.get_fotos():
            sizes = photo['sizes']
            max_size = max(sizes, key=self.get_largest)['url']
            type_photo = max(sizes, key=self.get_largest)['type']
            self.list_photo.append({'url': max_size, 'likes': photo['likes']['count'], 'type': type_photo})
        return self.list_photo
class YaUploader:
    def __init__(self, token_ya, file_comp):
        self.token_ya = token_ya
        self.file_comp = file_comp
        self.foto_likes = vk_foto.sizes_max()
        self.HEADERS = {"Authorization": f"OAuth {token_ya}"}

    def upload(self):
        """Метод загруджает файл file_path на яндекс диск"""
        dict_photo =[]
        for pair in tqdm(self.foto_likes):
            url = pair['url']
            likes = pair['likes']
            size = pair['type']
            ext = url.split('.')[-1].split('?')[0]
            filename = f"{likes}.{ext}"

            dict_photo.append({"file_name": filename, "size": size})
            response = requests.post(
            "https://cloud-api.yandex.net/v1/disk/resources/upload",
            params={
                "path": f'/VK_Photo/{filename}',
                "url": url
            },
            headers=self.HEADERS
            )

        response = requests.get(
            "https://cloud-api.yandex.net/v1/disk/resources/upload",
            params={
                "path": self.file_comp
            },
            headers=self.HEADERS
        )

        with open(f'{self.file_comp}/dict.json', 'w') as f:
            json.dump(dict_photo, f, indent=2)

        response = requests.get(
            "https://cloud-api.yandex.net/v1/disk/resources/upload",
            params={
                "path": "/VK_Photo/dict.json"
            },
            headers=self.HEADERS
        )
        href: object = response.json()["href"]

        with open(f"{self.file_comp}/dict.json", 'rb') as f:
            upload_response = requests.put(href, files={"file": f})
            response.raise_for_status()

if __name__ == '__main__':
    you_id = int(input('Введите id: '))
    token_ya = input('Вставте токен с Полигона Яндекс.Диска: ')
    vk_foto = VkUser(token, '5.126')
    uploader = YaUploader(token_ya, file_comp)
    result = uploader.upload()

