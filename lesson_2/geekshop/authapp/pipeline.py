from django.conf import settings
from datetime import datetime
from social_core.exceptions import AuthForbidden
import requests

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    # url_method = 'http://api.vk.com/method/'
    access_token = response.get('access_token')
    fields = ','.join(['bdate', 'sex', 'about'])

    api_url = f'{settings.SOCIAL_AUTH_VK_OAUTH2_URL_METHOD}users.get?fields={fields}&access_token={access_token}&v=5.131'

    response = requests.get(api_url)
    if response.status_code != 200:
        return

    data_json = response.json()['response'][0]

    if 'sex' in data_json:
        if data_json['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.GENDER
        elif data_json['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.OTHERS

    if 'bdate' in data_json:
        birthday = datetime.strptime(data_json['bdate'], '%d.%m.%Y')
        age = datetime.now().year - birthday.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        user.age = age

    if 'about' in data_json:
        user.shopuserprofile.about_me = data_json['about']