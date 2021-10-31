from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone
from social_core.exceptions import AuthException, AuthForbidden
from users.models import UserExternProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', '/method/users.get', None, urlencode(
        OrderedDict(fields=';'.join(('bdate', 'sex', 'about', 'photo_50', 'personal')),
                    access_token=response['access_token'], v='5.131')), None
                          ))
    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    data = resp.json()['response'][0]
    try:
        if data['sex']:
            user.userexternprofile.gender = UserExternProfile.MALE if data['sex'] == 2 else \
                UserExternProfile.FEMALE
    except KeyError:
        pass
    try:
        if data['about']:
            user.userexternprofile.about = data['about']
    except KeyError:
        pass

    try:
        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    except KeyError:
        pass

    try:
        if data['photo_50']:
            user.userexternprofile.photo = data['photo_50']
    except KeyError:
        pass

    try:
        if data['personal']['langs']:
              user.userexternprofile.lang = data['personal']['langs']
    except KeyError:
        pass
    user.save()

