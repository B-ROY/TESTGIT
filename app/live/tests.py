import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tests.utils import skipIfCustomUser
from django.contrib.flatpages.models import FlatPage
from django.test import TestCase
from django.test.utils import override_settings

class HeyDoAppTest(unittest.TestCase):

    def createUser(self):
        is_new, user = User.create_user(
            openid="1234567890",
            source=1,
            nick="username",
            gender=1,
            ip=self.request.remote_ip,
            province="",
            city="",
            country="",
            headimgurl="",
        )

        #success,message = QCloudIM.account_import(user)
        return is_new, user        

if __name__ == '__main__':
    unittest.main()
