import requests
from pprint import pprint

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

you_id = int(input('Введите id: '))
# token_ya = input('Вставте токен с Полигона Яндекс.Диска: ')
class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

        self.owner_id = you_id
    def get_fotos(self, user_id=None):
        if user_id is None:
            user_id = self.owner_id
        foto_url = self.url + 'photos.get'
        foto_params = {
            'album_id': 'profile',
            'count': '2',
            'photo_sizes': True,
            }

        photos = requests.get(foto_url, params={**self.params, **foto_params})

        return photos.json()

    def get_largest(size_dict):
        # Функция ищет наибольший размер картинки
        if size_dict['width'] >= size_dict['height']:
            return size_dict['width']
        else:
            return size_dict['height']


    def sizes_max(self):
        # Цикл поиска фото наибольшего размера
        for photo in self.get_fotos():
            sizes = photo['sizes']
            max_size = max(sizes, key=self.get_largest())#['url']
            print(max_size)


vk_foto = VkUser(token, '5.126')

# pprint(vk_foto.get_fotos())
pprint(vk_foto.get_fotos())#['response']['items'])
print(vk_foto.sizes_max())
# ['response']['items'][0]['sizes'][-1]

if __name__ == '__main__':
        VkUser(token, '5.126')

