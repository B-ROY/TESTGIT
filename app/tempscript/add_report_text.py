# coding=utf-8

from app.customer.models.report import *


def add_report_text():

    type_texts = []
    type_texts.append([
        "昵称存在违规内容",
        "签名存在不良信息",
        "相册过于暴露"
    ])

    type_texts.append([
        "有意拉往其他平台",
        "恶意欺骗礼物",
        "言语存在无端谩骂"
    ])
    type_texts.append([
        "聊天内容涉及色情、辱骂他人",
        "恶意欺骗礼物",
        "性别与资料不符"
    ])
    type_texts.append([
        "聊天内容涉及色情、辱骂他人",
        "恶意欺骗礼物",
        "性别与资料不符"
    ])

    for i, datas in enumerate(type_texts):
        print datas
        for j, data in enumerate(datas):
            label = i*100+j
            ReportText.create_report_text(label, data, i)


