#coding=utf-8

import facebook
from app.customer.common_util.image import UploadImage


class FacebookAPI(object):

    @classmethod
    def get_user_info(cls, access_token):
        import time
        start_time = int(time.time())
        access_token = access_token
        print access_token
        #access_token = "EAAYpViK68lYBAJ1lI6eP3Y1d2LS04APhPD6beE9vwRpB8IZCRIM5Kv325sI3DAY24VqlIlcDdHT71qyLhToL9KaPhAzFbaHZCsQgLQAYA5s6aHACqwln5mlQ7QyqFmommlFdpWvMMQVP2LK0j7xB3piiUyrpQElzEn7bHNLF52I5eEcprkaW7i7nyISoUZD"
        graph = facebook.GraphAPI(access_token=access_token, version='2.7')
        user_info = graph.get_object('me',fileds="name,gender")
        print user_info
        gender = 2 if "gender" in user_info and user_info["gender"] == "female" else 1
        picture = graph.get_object('me/picture', type="large", is_silhouette="false")

        if "data" in picture:
            data = UploadImage.push_binary_to_qclude(picture["data"])
            print data
            url =  data.get("data", {}).get('download_url', '')
        else:
            url =  "https://hdlive-10048692.image.myqcloud.com/head_1497412888" if gender == 1 \
                else "https://hdlive-10048692.image.myqcloud.com/head_1497413140"
        print picture
        print len(picture)

        end_time = int(time.time())
        print "total cost time is " + str(end_time - start_time)

        result = {
            "nickname": user_info["name"],
            "headimgurl" : url,
            "sex": gender,
        }
        return result