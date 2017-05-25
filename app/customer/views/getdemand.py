#coding=utf-8
from api.document.doc_tools import *
from api.view.base import *
from app.live.models import *
from django.conf import settings
from api.convert.convert_user import *
# from PIL import Image
import time
import tempfile
import json
from QcloudApi.qcloudapi import *
from app.customer.models.user import *
import logging

ACTION = {
    0:u'DescribeRecordPlayInfo', #获取视频信息，通过VID
    1:u'DescribeVodInfo', #获取视频的详细信息，竟然也可以通过VID进行获取，很无语
}



class QCloudDemand(object):
    module = 'vod'
    #TODO:点播的秘钥
    SECRET_ID = 'AKIDcABhnDSMPYwYTlL6zFx9aellfRIP5YlK'
    SECRET_KEY = '5kBoCTiivmyjR1uIkhC5tLP5Ym2xGEiY'
    REGION = 'bj'

    config = {
        'Region': REGION,
        'secretId': SECRET_ID,
        'secretKey': SECRET_KEY,
        'method': 'post'
    }

    params = {
        'Action' : ACTION[0],
        'Region' : REGION,
        'SecretId' : SECRET_ID,
    }

    @classmethod
    def set_user_to_list(self,uid,dflag=DemandList.DEMANDLISTFLAG):
        try:
            is_new,reg = DemandList.gen(uid,DemandList.DEMANDLISTFLAG_MARKED)
            return is_new,reg
        except Exception,e:
            raise Exception("设置白名单失败" + e.message)
                

    @classmethod
    def check_user_exist(self,uid):
        if not DemandList.check_is_ok(uid):
            return False
        return True

    @classmethod 
    def save_video_info(self,uid,vid,fileid,filename,playurl,duration,imageurl,status,createtime=None,size=None):
        try:
            code = DemandVideoInfo.gen(uid,vid,fileid,filename,playurl,duration,imageurl,status)
            return code
        except Exception,e:
            raise Exception("数据存储失败")
        

    @classmethod
    def videoinfo_parser_save(self,uid,data):
        if not data:
            raise Exception("数据为空，重新获取")

        fileSet = {}
        files = data['fileSet']
        filesData = []

        for i in range(len(files)):
            for item in files[i].items():
                if item[0] == 'playSet':
                    fileSet['url'] = item[1][0]['url'] 
                    continue
                fileSet[item[0]] = item[1]
            filesData.append(fileSet)
        
        for i in range(len(filesData)):
            try:
                result = self.save_video_info(uid,filesData[i]['vid'],filesData[i]['fileId'],filesData[i]['fileName'],filesData[i]['url'],filesData[i]['duration'],filesData[i]['image_url'],filesData[i]['status'])
                return result
            except Exception,e:
                raise Exception("数据存储:"+e.message)

    @classmethod
    def get_vidoe_info(self,uid,vid):
        try:
            if not self.check_user_exist(uid):
                raise Exception("非白名单用户，不能录制视频")
            service = QcloudApi(self.module, self.config)
            #print service.generateUrl(action, params)
            self.params['vid'] = vid
            result =  service.call(ACTION[0], self.params)
            
            data = json.loads(result)

            if not data['code']:
                return data
            raise Exception(result)
            
            #service.setRequestMethod('get')
            #print service.call('DescribeClass', {})
        except Exception, e:
            raise Exception("获取信息失败:"+ e.message)


#TODO:效率问题，这里不直接执行，在CMS后台进行执行
#result = QCloudDemand.get_vidoe_info(uid,vid)
#TODO: 解析返回值并写入到数据库
#retCode = QCloudDemand.videoinfo_parser_save(uid,result)

"""
# 这个是腾讯云这边的返回值格式，上面已经针对这个进行处理，你这边可以在调优
{
    u'message': u'', 
    u'code': 0, 
    u'fileSet': 
    [
        {
            u'status': u'2', 
            u'playSet': 
            [
                {u'url': u'http://200020814.vod.myqcloud.com/200020814_b61e158efb114dc68aecc1797687c2ff.f0.mp4', u'definition': 0, u'vwidth': 240, u'vheight': 320, u'vbitrate': 413000}, 
                {u'url': u'http://200020814.vod.myqcloud.com/200020814_b61e158efb114dc68aecc1797687c2ff.f20.mp4', u'definition': 20, u'vwidth': 640, u'vheight': 852, u'vbitrate': 357368}
            ], 
            u'vid': u'200020814_b61e158efb114dc68aecc1797687c2ff', 
            u'fileName': u'\u5c0f\u72cd\u5b50', 
            u'image_url': u'http://p.qpic.cn/videoyun/0/200020814_b61e158efb114dc68aecc1797687c2ff_1/640', 
            u'duration': u'5', 
            u'fileId': u'14651978969260251238'
        }
    ]
}
"""
"""
#
# 下面是API接口，主要是给你参考，API接口的格式，没什么难的，慢慢熟悉后API这边就很快可以上手了
#
@handler_define
class CheckDemandUser(BaseHandler):
    @api_define("Check demand user", r'/live/demand/checkuser', [
        Param('user_id',True,str,"","120",u'用户ID')
    ], description=u"检查用户是否在白名单",protocal="https")
    @login_required
    def get(self):
        try:
            uid = self.arg('user_id')
            data = QCloudDemand.check_user_exist(uid)
        except Exception, e:
            logging.error("check user error:%s" % str(e))
            return self.write({"status": "fail", "error": "%s:%s" % (e,e.message)})
        
        self.write({'status':'success', 'data': data})

@handler_define
class RecordFinished(BaseHandler):
    @api_define("record finished",r'/live/demand/recfinished',[
        Param('user_id',True,str,"","120",u'用户ID'),
        Param('vid',True,str,"","200020814_b61e158efb114dc68aecc1797687c2ff",u'视频ID'),
    ],description=u"用户录制完毕后调用接口",protocal="https")
    @login_required
    def get(self):
        try:
            uid = self.arg('user_id')
            vid = self.arg('vid')
            #TODO:效率问题，这里不直接执行，在CMS后台进行执行
            #result = QCloudDemand.get_vidoe_info(uid,vid)
            #TODO: 解析返回值并写入到数据库
            #retCode = QCloudDemand.videoinfo_parser_save(uid,result)
            result = DemandVideoInfo.save_vid(uid,vid)
        except Exception, e:
            logging.error("demand video error:%s" % str(e))
            return self.write({"status": "fail", "error": "%s" % (e.message)})
        self.write({'status':'success','data':result})
"""

