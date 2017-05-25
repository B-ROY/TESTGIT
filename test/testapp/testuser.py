#coding=utf-8
from app.customer.models.user import *

class TestUserDeultImg:
    def test_get_all_default_img(self):
        pictures = UserDefaultImg.get_all_defaults_img()
        for picture in pictures:
            print picture.picture_url
            assert picture.picture_url in UserDefaultImg.Picture_info
            assert picture.gender in UserDefaultImg.User_gender