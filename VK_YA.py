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

    def get_fotos(self):
        # Параметры VK
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
    def get_likes(self):
        #Показывает кол-во лайков в фото
        list_likes =[]
        for photo in self.get_fotos():
            likes = photo['likes']['count']
            list_likes.append(likes)
        return list_likes

    def get_largest(self, size_dict):
        # Функция ищет наибольший размер картинки
        if size_dict['width'] >= size_dict['height']:
            return size_dict['width']
        else:
            return size_dict['height']

    def sizes_max(self):
        # Цикл поиска фото наибольшего размера
        list_photo = []
        for photo in self.get_fotos():
            sizes = photo['sizes']
            max_size = max(sizes, key=self.get_largest)['url']
            list_photo.append(max_size)
        return list_photo

vk_foto = VkUser(token, '5.126')

# pprint(vk_foto.get_fotos())
# pprint(vk_foto.get_fotos())#['response']['items'])
pprint(vk_foto.sizes_max())
pprint(vk_foto.get_likes()) #Лайки
if __name__ == '__main__':
        VkUser(token, '5.126')


