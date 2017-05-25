# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # child audio
    url(r'^child_audio_list$', 'app.audio.views.audio.child_audio_list', name='child_audio_list'),
    url(r'^child_audio_create$', 'app.audio.views.audio.child_audio_create', name='child_audio_create'),
    url(r'^child_audio_edit$', 'app.audio.views.audio.child_audio_edit', name='child_audio_edit'),
    url(r'^close_child_audio$', 'app.audio.views.audio.close_child_audio', name='close_child_audio'),
    # audio price
    url(r'^audio_price_list$', 'app.audio.views.audio.audio_price_list', name='audio_price_list'),
    url(r'^audio_price_edit$', 'app.audio.views.audio.audio_price_edit', name='audio_price_edit'),
    url(r'^price_add$', 'app.audio.views.audio.audio_price_add', name='audio_price_add'),
    url(r'^price_add_handler$', 'app.audio.views.audio.priceHanler', name='add_price_handler'),

    #video price
    url(r'^video_price_list$', 'app.audio.views.audio.video_price_handler', name='video_price_handler'),
    url(r'^video_price_edit$', 'app.audio.views.audio.edit_price_handler', name='edit_price_handler'),
    url(r'^video_price_add$', 'app.audio.views.audio.add_price_handler', name='add_price_handler'),
    url(r'^add_price_handler$', 'app.audio.views.audio.add_handler', name='add_handler'),

    #pushRecord
    url(r'^push_msg_record', 'app.audio.views.pushRecord.PushRecord', name='push_msg_record'),
    url(r'^push_msg', 'app.audio.views.pushRecord.Push', name='push_msg')
    
)