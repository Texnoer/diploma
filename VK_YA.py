import requests
from pprint import pprint

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

you_id = int(input('Введите id: '))
token_ya = input('Вставте токен с Полигона Яндекс.Диска: ')
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
        return photos.json()['response']['items']

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

vk_foto = VkUser(token, '5.126')
foto_likes = vk_foto.sizes_max()

HEADERS = {
    "Authorization": f"OAuth {token_ya}"
}
class YaUploader:
    def __init__(self, token_ya):
        self.token_ya = token_ya

    def upload(self, file_path: str):
        """Метод загруджает файл file_path на яндекс диск"""
        dict_photo =[]
        for pair in foto_likes:
            url = pair['url']
            likes = pair['likes']
            size = pair['type']
            dict_photo.append({"file_name": likes, "size": size})
            response = requests.post(
            "https://cloud-api.yandex.net/v1/disk/resources/upload",
            params={
                "path": f'/VK_Photo/{likes}',
                "url": url
            },
            headers=HEADERS
        )
        pprint(dict_photo)
if __name__ == '__main__':
    uploader = YaUploader("token_ya")
    result = uploader.upload('url')

