#!/usr/bin/env python
# coding=utf-8

from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest
from qcloud_cos import UploadSliceFileRequest
from qcloud_cos import UpdateFileRequest
from qcloud_cos import UpdateFolderRequest
from qcloud_cos import DelFileRequest
from qcloud_cos import MoveFileRequest
from qcloud_cos import DelFolderRequest
from qcloud_cos import CreateFolderRequest
from qcloud_cos import StatFileRequest
from qcloud_cos import StatFolderRequest
from qcloud_cos import ListFolderRequest
from qcloud_cos import Auth
from qcloud_cos import cos_client

"""
def cos_demo():
    # 设置用户属性, 包括appid, secret_id和secret_key
    # 这些属性可以在cos控制台获取(https://console.qcloud.com/cos)
    appid = 10048692                  # 替换为用户的appid
    secret_id = u'AKIDgknyBYkNKnpONeweTRwK9t6Nn0jn78yG'         # 替换为用户的secret_id
    secret_key = u'fBCXVJK1PpWPtYizb7vIGVMIJFm90GBa'         # 替换为用户的secret_key
    cos_client = CosClient(appid, secret_id, secret_key)

    # 设置要操作的bucket
    bucket = u'heydo'

    ############################################################################
    # 文件操作                                                                 #
    ############################################################################
    # 1. 上传文件(默认不覆盖)
    #    将本地的local_file_1.txt上传到bucket的根分区下,并命名为sample_file.txt
    #    默认不覆盖, 如果cos上文件存在,则会返回错误
    request = UploadFileRequest(bucket, u'/sample_file.txt', u'local_file_1.txt')
    upload_file_ret = cos_client.upload_file(request)
    print 'upload file ret:', repr(upload_file_ret)

    # 2. 上传文件(覆盖文件)
    #    将本地的local_file_2.txt上传到bucket的根分区下,覆盖已上传的sample_file.txt
    request = UploadFileRequest(bucket, u'/sample_file.txt', u'local_file_2.txt')
    request.set_insert_only(0)  # 设置允许覆盖
    upload_file_ret = cos_client.upload_file(request)
    print 'overwrite file ret:', repr(upload_file_ret)

    # 3. 获取文件属性
    request = StatFileRequest(bucket, u'/sample_file.txt')
    stat_file_ret = cos_client.stat_file(request)
    print 'stat file ret:', repr(stat_file_ret)

    # 4. 更新文件属性
    request = UpdateFileRequest(bucket, u'/sample_file.txt')

    request.set_biz_attr(u'这是个demo文件')           # 设置文件biz_attr属性
    request.set_authority(u'eWRPrivate')              # 设置文件的权限
    request.set_cache_control(u'cache_xxx')           # 设置Cache-Control
    request.set_content_type(u'application/text')     # 设置Content-Type
    request.set_content_disposition(u'ccccxxx.txt')   # 设置Content-Disposition
    request.set_content_language(u'english')          # 设置Content-Language
    request.set_x_cos_meta(u'x-cos-meta-xxx', u'xxx') # 设置自定义的x-cos-meta-属性
    request.set_x_cos_meta(u'x-cos-meta-yyy', u'yyy') # 设置自定义的x-cos-meta-属性

    update_file_ret = cos_client.update_file(request)
    print 'update file ret:', repr(update_file_ret)

    # 5. 更新后再次获取文件属性
    request = StatFileRequest(bucket, u'/sample_file.txt')
    stat_file_ret = cos_client.stat_file(request)
    print 'stat file ret:', repr(stat_file_ret)

    # 6. 移动文件, 将sample_file.txt移动位sample_file_move.txt
    request = MoveFileRequest(bucket, u'/sample_file.txt', u'/sample_file_move.txt')
    stat_file_ret = cos_client.move_file(request)
    print 'move file ret:', repr(stat_file_ret)

    # 7. 删除文件
    #request = DelFileRequest(bucket, u'/sample_file_move.txt')
    #del_ret = cos_client.del_file(request)
    #print 'del file ret:', repr(del_ret)

    ############################################################################
    # 目录操作                                                                 #
    ############################################################################
    # 1. 生成目录, 目录名为sample_folder
    #request = CreateFolderRequest(bucket, u'/sample_folder/')
    #create_folder_ret = cos_client.create_folder(request)
    #print 'create folder ret:', create_folder_ret

    # 2. 更新目录的biz_attr属性
    #request = UpdateFolderRequest(bucket, u'/sample_folder/', u'这是一个测试目录')
    #update_folder_ret = cos_client.update_folder(request)
    #print 'update folder ret:', repr(update_folder_ret)

    # 3. 获取目录属性
    #request = StatFolderRequest(bucket, u'/sample_folder/')
    #stat_folder_ret = cos_client.stat_folder(request)
    #print 'stat folder ret:', repr(stat_folder_ret)

    # 4. list目录, 获取目录下的成员
    #request = ListFolderRequest(bucket, u'/sample_folder/')
    #list_folder_ret = cos_client.list_folder(request)
    #print 'list folder ret:', repr(list_folder_ret)

    # 5. 删除目录
    #request = DelFolderRequest(bucket, u'/sample_folder/')
    #delete_folder_ret = cos_client.del_folder(request)
    #print 'delete folder ret:', repr(delete_folder_ret)
"""
class AudioRecord:
    appid = 10048692
    secret_id = u'AKIDgknyBYkNKnpONeweTRwK9t6Nn0jn78yG'
    secret_key = u'fBCXVJK1PpWPtYizb7vIGVMIJFm90GBa'
    def __init__(self,bucket,cos_path):
        self.cos_client = CosClient(AudioRecord.appid, AudioRecord.secret_id, AudioRecord.secret_key)
        self.auth = Auth(self.cos_client.get_cred())
        self.bucket = bucket
        self.cos_path = cos_path
        self.expired = 30

    def get_once_sign(self):
        return self.auth.sign_once(self.bucket, self.cos_path)

    def get_more_sign(self):
        return self.auth.sign_more(self.bucket, self.cos_path,self.expired)

    def get_down_sign(self):
        return self.auth.sign_download(self.bucket, self.cos_path,self.expired)

    def DirIsExist(self):
        return False

    def CreateIntroduceDir(self):
        #'/record/introduce/' + xxx 
        request = CreateFolderRequest(self.bucket, self.cos_path)
        create_folder_ret = self.cos_client.create_folder(request)
        result = json.loads(create_folder_ret)
        return result

    def DeleteFolderTest(self):
        request = DelFolderRequest(self.bucket, self.cos_path)
        delete_folder_ret = CosClient.del_folder(request)
        result = json.loads(delete_folder_ret)
        print 'delete folder ret:', repr(delete_folder_ret)
        return result

if __name__ == '__main__':
    ar = CosClient(appid=AudioRecord.appid, secret_id=AudioRecord.secret_id, secret_key=AudioRecord.secret_key)
    request = ListFolderRequest(u'porncheck', u'/1400011479/19700101/')
    list_folder_ret = ar.list_folder(request)
    print list_folder_ret
    #request = DelFolderRequest(u'porncheck', u'/1400011479/19700101/')
    #delete_folder_ret = ar.del_folder(request)
    #print 'delete folder ret:', repr(delete_folder_ret)
    #ar = AudioRecord('heydo','/record/introduce/102/')
    #ar = AudioRecord('porncheck', '/1400011479/19700101/')
    #print ar
    #print ar.get_once_sign()
    #print ar.DeleteFolderTest()
    #print ar.get_once_sign()
    #print ar.CreateIntroduceDir()
    #cos_demo()
