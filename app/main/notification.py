"""
Alerts Notification
labmet
"""

import os
import json
import requests


class NotificationNotAuth(Exception):
    pass


class Notification:

    def __init__(self, apikey, profile='labmet'):
        # TODO: Change this
        self.apikey = apikey
        self.profile = profile
        self.headers = {}
        self.headers['Content-Type'] = 'application/json'
        self.headers['Authorization'] = 'Bearer ' + self.apikey
        self.tokens = []
        self.base_url = 'https://api.ionic.io'

        if apikey is not None:
            self.get_tokens()

    def test_auth(self):
        """testing if auth correct"""
        url = self.base_url + "/auth/test"
        response = requests.get(url, headers=self.headers).json()

        try:
            assert response['meta']['status'] == 200
        except:
            raise NotificationNotAuth('incorrect token')

        return True

    def get_tokens(self):
        """return mobile token"""
        url = self.base_url + '/push/tokens'

        if len(self.tokens) == 0:
            response = requests.get(url, headers=self.headers).json()
            assert response['meta']['status'] == 200
            if len(response['data']) > 0:
                self.tokens = [d['token'].encode(
                    'iso-8859-15') for d in response['data']]
        return self.tokens

    def send_push_all(self, msg):
        # TODO: Async func
        if not self.apikey:
            return 
        url = self.base_url + '/push/notifications'
        if len(self.tokens) > 0:

            data = {
                "tokens": self.tokens,
                "profile": self.profile,
                "notification": {
                    "message": msg
                }
            }
            response = requests.post(url, json=data,
                                     headers=self.headers).json()
            assert response['meta']['status'] == 201
            return True
        else:
            print("No tokens")


def main():
    notification = Notification(os.environ.get('NOTIFICATIONKEY'))
    notification.get_tokens()
    notification.send_push_all('Alert is very dry')

if __name__ == '__main__':
    main()
