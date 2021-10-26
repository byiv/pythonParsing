import scrapy
from scrapy.http import HtmlResponse
import re
import json
from pprint import pprint
from urllib.parse import urlencode
from copy import deepcopy
from instaparser.items import InstaparserItem
from instaparser.login import pwd


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'byiv_85'
    inst_pwd = pwd
    users_for_parse = ['buneeva.design',
                       'byzov_is']
    api_url = 'https://i.instagram.com/api/v1/friendships'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={
                'username': self.inst_login,
                'enc_password': self.inst_pwd
            },
            headers={'X-CSRFToken': csrf}

        )

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for user_for_parse in self.users_for_parse:
                yield response.follow(
                    f'/{user_for_parse}',
                    callback=self.user_parse,
                    cb_kwargs={'username': user_for_parse}
                )

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        params = {'count': 12, 'max_id': 0}
        friends = ['following', 'followers']
        for friend in friends:
            if friend == 'followers':
                params['search_surface'] = 'follow_list_page'
            user_friends_url = f'{self.api_url}/{user_id}/{friend}/?{urlencode(params)}'
            print()
            yield response.follow(user_friends_url,
                                  callback=self.user_parse_friend,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'params': deepcopy(params),
                                             'friend': friend
                                             }
                                  )

    def user_parse_friend(self, response: HtmlResponse, username, user_id, params, friend):
        j_data = response.json()
        next_max_id = j_data.get('next_max_id')
        if next_max_id:
            params['max_id'] = next_max_id
            user_friends_url = f'{self.api_url}/{user_id}/{friend}/?{urlencode(params)}'
            print()
            yield response.follow(user_friends_url,
                                  callback=self.user_parse_friend,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'params': deepcopy(params),
                                             'friend': friend
                                             }
                                  )
        users = j_data.get('users')
        print()
        for user in users:
            item = InstaparserItem(main_id=user_id,
                                   main_username=username,
                                   user_id=user.get('pk'),
                                   user_name=user.get('username'),
                                   user_photo=user.get('profile_pic_url'),
                                   type_friend=friend
                                   )
            yield item

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
