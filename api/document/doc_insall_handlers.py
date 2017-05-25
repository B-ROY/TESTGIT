#coding=utf-8

INSTALL_HANDLERS = [
    "api.handler.pay",
    "api.handler.search",
    "api.handler.userapi",
    "api.handler.account",
    "api.handler.start_init",
    "api.handler.version",
    "api.handler.admin",
    "api.handler.audioroom",
    "api.handler.picture",
    "api.handler.videoroom",
    "api.handler.gift",
    "api.handler.home",
    "api.handler.stat",
    "api.handler.service",
    "api.handler.withdraw",
    "api.handler.activity",#活动临时接口
    "api.handler.audit", #鉴黄举报相关接口
]

INSTALL_HANDLERS_NAME = {

    "api.handler.pay": "支付API",
    "api.handler.search": "搜索API",
    "api.handler.userapi": "用户信息 API",
    "api.handler.account": "用户账户API",
    "api.handler.start_init": "启动初始化API",
    "api.handler.version": "检查更新",
    "api.handler.admin": "检查管理员",
    "api.handler.audioroom": "语音房间 API",
    "api.handler.picture": "图片 API",
    "api.handler.videoroom": "视频房间 API",
    "api.handler.gift": "礼物",
    "api.handler.home": "首页",
    "api.handler.stat": "统计",
    "api.handler.service": "其它API",
    "api.handler.withdraw": "提现",
    "api.handler.activity": "活动临时接口",
    "api.handler.audit": "净化app接口"
}
