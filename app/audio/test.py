# coding=utf-8
import base64
import hashlib
import urllib2
import urllib
"""
from django.test import TestCase

# Create your tests here.


<?php
	/*
		*demo仅供参考
	*/
	$url 					= '';		//支付网关
	$para['order_no'] 		= 	'商户号_自定义订单号';							//订单号
	$para['goods_name'] 	= 	'';												//商品名
	$para['remark'] 		= 	'test';											//商品备注
	$para['order_amt'] 		= 	'';												//订单金额
	$para['return_url'] 	= 	'';												//同步地址
	$para['notify_url'] 	= 	'';												//异步地址
	$para['custom'] 		=  	'';												//透传地址
	$para['payment_type'] 	=   '';												//支付类型
	$code			 		= 	'商户号';										//商户号
	$key 					= 	'商户key';										//key
	//拼装验签
	$custom_str 			= 'order_no='.$para['order_no'].'&order_amt='.$para['order_amt'].'&key='.$key;
	$base_custom_str 		= base64_encode($custom_str);
	$para['sign'] 			= md5($base_custom_str);
"""


param = {}
url  = "http://api.gongdapeng.cn/wft_pc_another/index.php"
param["order_no"] = "548_23"
param["goods_name"] = "测试商品889"
param["remark"] = "test"
param["order_amt"] = 2
param["return_url"] = "www.baidu.com"
param["notify_url"] = ""
param["custom"] = ""
param["payment_type"] = 3

sign_orig = "order_no=" + param["order_no"] + "&order_amt=" + str(param["order_amt"]) + "&key=175f2ca6897f223f0b1ab3c8d1e36114"
sign_base64 = base64.b64encode(sign_orig)
smd5 = hashlib.md5()
smd5.update(sign_base64)
sign = smd5.hexdigest()
param["sign"] = sign

print url+"?"+urllib.urlencode(param)
req = urllib2.Request(url + "?" + urllib.urlencode(param))
data = urllib2.urlopen(req).read()
print data




