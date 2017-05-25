# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    #level
    url(r'^level/list$', 'app.customer.views.level.level_list', name='level_list'),
    url(r'^level/edit$', 'app.customer.views.level.level_new', name='level_edit'),
    url(r'^gift/list$', 'app.customer.views.gift.gift_list', name='gift_list'),
    url(r'^gift/edit$', 'app.customer.views.gift.gift_edit', name='gift_edit'),
    url(r'^gift/delete', 'app.customer.views.gift.gift_delete', name='gift_delete'),
    url(r'^gift/position$', 'app.customer.views.gift.gift_position', name='gift_position'),
    url(r'^adv/list$', 'app.customer.views.adv.adv_list', name='adv_list'),
    url(r'^adv/edit$', 'app.customer.views.adv.adv_edit', name='adv_edit'),
    url(r'^adv/position$', 'app.customer.views.adv.adv_position', name='adv_position'),
    url(r'^adv/delete', 'app.customer.views.adv.adv_delete', name='adv_delete'),
    url(r'^adv/upload$', 'app.customer.views.adv.adv_upload', name='adv_upload'),
    url(r'^upload/image$', 'app.customer.views.gift.upload_img', name='upload_img'),
    url(r'^account$', 'app.customer.views.account.account', name='account'),
    url(r'^account/add_balance$', 'app.customer.views.account.add_balance', name='add_balance'),
    url(r'^account/replace_pay', 'app.customer.views.account.replace_pay', name='replace_pay'),
    url(r'^account/account_experience', 'app.customer.views.account.account_experience', name='account_experience'),
    url(r'^account/operate_experience', 'app.customer.views.account.operate_experience', name='operate_experience'),
    url(r'^account/apple_verify$', 'app.customer.views.account.apple_verify', name='apple_verify'),
    url(r'^more/trade/orders$', 'app.customer.views.account.more_trade_orders', name='more_trade_orders'),
    url(r'^trade/order/detail$', 'app.customer.views.account.trade_order_detail', name='trade_order_detail'),

    url(r'^trade/account/record$', 'app.customer.views.account.trade_account_records', name='trade_account_records'),
    url(r'^trade/rule$', 'app.customer.views.account.trade_rule', name='trade_rule'),
    url(r'^trade/rule/edit$', 'app.customer.views.account.trade_rule_edit', name='trade_rule_edit'),
    url(r'^trade/rule/delete$', 'app.customer.views.account.trade_rule_delete', name='trade_rule_delete'),

    url(r'^withdraw/orders', 'app.customer.views.account.with_draw_orders', name='with_draw_orders'),
    url(r'^withdraw/order/detail', 'app.customer.views.account.withdraw_order_detail', name='withdraw_order_detail'),
    url(r'^withdraw/order/confirm_form', 'app.customer.views.account.withdraw_pass_confirm_form', name='withdraw_pass_confirm_form'),
    url(r'^withdraw/order/dismiss_form', 'app.customer.views.account.withdraw_dismiss_form', name='withdraw_dismiss_form'),
    url(r'^allow/withdraw', 'app.customer.views.account.allow_withdraw_order', name='allow_withdraw_order'),
    url(r'^dissmiss/withdraw', 'app.customer.views.account.dissmiss_withdraw_order', name='dissmiss_withdraw_order'),

    url(r'^switch/list$', 'app.customer.views.switch.switch_list', name='switch_list'),
    url(r'^switch/edit$', 'app.customer.views.switch.switch_edit', name='switch_edit'),
    url(r'^switch/delete', 'app.customer.views.switch.switch_delete', name='switch_delete'),
    url(r'^switch/platform_json', 'app.customer.views.switch.platform_json', name='platform_json'),

    url(r'^version/list$', 'app.customer.views.version_info.version_list', name='version_list'),
    url(r'^version/edit$', 'app.customer.views.version_info.version_edit', name='version_edit'),
    url(r'^version/delete', 'app.customer.views.version_info.version_delete', name='version_delete'),

    #experience
    url(r'^experience/list$', 'app.customer.views.experience.experience_list', name='experience_list'),
    url(r'^experience/type/edit$', 'app.customer.views.experience.experience_type_new', name='experience_type_edit'),

    #report
    url(r'^report/list$', 'app.customer.views.report.report_list', name='report_list'),
    url(r'^report/edit$', 'app.customer.views.report.report_edit', name='report_edit'),
    url(r'^report/ignore$', 'app.customer.views.report.report_ignore', name='report_ignore'),
    url(r'^report/off$', 'app.customer.views.report.report_off', name='report_off'),

    #user
    url(r'^user/list$', 'app.customer.views.user.user_list', name='user_list'),
    url(r'^user/show/(\d+)$', 'app.customer.views.user.show', name='user_show'),
    url(r'^user/block$', 'app.customer.views.user.block', name='user_block'),
    url(r'^user/check/identity/exist$', 'app.customer.views.user.check_identity', name='user_check_identity_exist'),
    url(r'^user/update/identity$', 'app.customer.views.user.update_identity', name='update_identity'),
    url(r'^user/update/nickname', 'app.customer.views.user.update_nickname', name='update_nickname'),
    url(r'^user/update/desc', 'app.customer.views.user.update_desc', name='update_desc'),
    url(r'^user/parttime/list$', 'app.customer.views.user.parttime_list', name='parttime_list'), # parttime manage
    url(r'^user/parttime/edit$', 'app.customer.views.user.parttime_edit', name='parttime_edit'),
    url(r'^user/parttime/set_parttime$', 'app.customer.views.user.set_parttime', name='set_parttime'),
    url(r'^user/parttime/show$', 'app.customer.views.user.parttime_show', name='parttime_show'),
    url(r'^user/parttime/excel$', 'app.customer.views.excel.output', name='output'),
    url(r'^user/superadmin/list$', 'app.customer.views.user.superadmin_list', name='superadmin_list'), # superadmin manage
    url(r'^user/superadmin/edit$', 'app.customer.views.user.superadmin_edit', name='superadmin_edit'),
    url(r'^user/superadmin/set_superadmin$', 'app.customer.views.user.set_superadmin', name='set_superadmin'),
    url(r'^user/channel_list$', 'app.customer.views.user.channel_list', name='channel_list'),
    url(r'^user/channel_edit$', 'app.customer.views.user.channel_edit', name='channel_edit'),
    url(r'^user/channel_delete$', 'app.customer.views.user.channel_delete', name='channel_delete'),
    url(r'^hotanchor', 'app.customer.views.Anchor.AnchorHandler', name='hotanchor'),
    url(r'^userShow', 'app.customer.views.Anchor.AnchorShow', name='user_show_handler'),
    url(r'^AnchorChange', 'app.customer.views.Anchor.change', name='AnchorChange'),
    url(r'^add_hot_anchor', 'app.customer.views.Anchor.add_anchor', name='add_hot_anchor'),
    url(r'^AnchorDelete', 'app.customer.views.Anchor.delete_anchor', name='AnchorDelete'),



    #child_user
    url(r'^child_user/list$', 'app.customer.views.child_user.child_user_list', name='child_user_list'),
    url(r'^child_user/edit$', 'app.customer.views.child_user.child_user_edit', name='child_user_edit'),
    url(r'^child_user/create$', 'app.customer.views.child_user.child_user_create', name='child_user_create'),
    url(r'^child_user/account$', 'app.customer.views.child_user.child_user_account', name='child_user_account'),
    url(r'^child_user/add$', 'app.customer.views.child_user.child_user_add', name='child_user_add'),
    url(r'^child_user/upload$', 'app.customer.views.child_user.child_user_upload', name='child_user_upload'),
    url(r'^child_user/picture$', 'app.customer.views.child_user.child_user_picture', name='child_user_picture'),
    url(r'^child_user/picture_delete$', 'app.customer.views.child_user.child_picture_delete', name='child_picture_delete'),
    url(r'^child_user/pictureinfo$', 'app.customer.views.child_user.child_pictureinfo', name='child_pictureinfo'),
    url(r'^child_user/pictureadd$', 'app.customer.views.child_user.child_pictureadd', name='child_pictureadd'),
    url(r'^child_user/picturecreate$', 'app.customer.views.child_user.child_picturecreate', name='child_picturecreate'),
    url(r'^child_user/comment_delete$', 'app.customer.views.child_user.child_comment_delete', name='child_comment_delete'),
    url(r'^child_user/comment_create$', 'app.customer.views.child_user.child_comment_create', name='child_comment_create'),

    #lucknum
    url(r'^lucknum/list$', 'app.customer.views.lucknum.lucknum_list', name='lucknum_list'), 
    url(r'^lucknum/edit$', 'app.customer.views.lucknum.lucknum_new', name='lucknum_edit'),

    #demand
    url(r'^demand/list$', 'app.customer.views.demand.demand_list', name='demand_list'), 
    url(r'^demand/edit$', 'app.customer.views.demand.demand_new', name='demand_edit'),
    url(r'^demand/delete$', 'app.customer.views.demand.demand_delete', name='demand_delete'), 
    url(r'^demand/videodelete$', 'app.customer.views.demand.demandvideo_delete', name='demandvideo_delete'),      
    url(r'^demand/videolist$', 'app.customer.views.demand.demandvideo_list', name='demandvideo_list'),  

    #startup_image
    url(r'^startup_image/list$', 'app.customer.views.startup_image.startup_image_list', name='startup_image_list'),
    url(r'^startup_image/edit$', 'app.customer.views.startup_image.startup_image_edit', name='startup_image_edit'),
    url(r'^startup_image/delete', 'app.customer.views.startup_image.startup_image_delete', name='startup_image_delete'),

    #whitelist
    url(r'^whitelist/list$', 'app.customer.views.whitelist.whitelist_list', name='whitelist_list'),
    url(r'^whitelist/edit$', 'app.customer.views.whitelist.edit_whitelist', name='edit_whitelist'),
    url(r'^whitelist/delete', 'app.customer.views.whitelist.delete_whitelist', name='delete_whitelist'),

    #block_user
    url(r'^block_user/list$', 'app.customer.views.block_user.block_user_list', name='block_user_list'),
    url(r'^block_user/edit$', 'app.customer.views.block_user.block_user_new', name='block_user_edit'),
    url(r'^block_user/update$', 'app.customer.views.block_user.block_user_update', name='block_user_update'),

    #roomusergift
    url(r'^room_user_gift$', 'app.customer.views.user.room_user_gift', name='room_user_gift'),

    #RealNameVerify
    url(r'^RealName$', 'app.customer.views.RealName.RealNameHandler', name='RealName'),

    url(r'^StatueHandler$', 'app.customer.views.RealName.Statue_edit', name='StatueHandler'),

    #Withdraw
    url(r'^WithdrawHandler$', 'app.customer.views.Withdraw.WithdrawHandler', name='WithdrawHandler'),

    url(r'^choose', 'app.customer.views.Withdraw.chooseHandler', name='chooseHandler'),

    url(r'^refuseHandler', 'app.customer.views.Withdraw.refuseHandler', name='refuseHandler'),

    #video_manager_handler_verify
    url(r'^videoManagerHandler', 'app.customer.views.user.videoManager', name='videoManagerHandler'),
    url(r'^StatusVideoHandler', 'app.customer.views.user.Status_video_manager', name='StatusVideoHandler'),






    
    #
    # #bussiness
    # url(r'^bussiness/list$', 'app.customer.views.business.statistics', name='business_statistics'),
    # #statistics
    # url(r'^statistics/user$', 'app.customer.views.statistics_view.user', name='user_statistics'),
    # url(r'^statistics/trade_in$', 'app.customer.views.statistics_view.trade_in', name='trade_in_statistics'),
    # url(r'^statistics/trade_in_detail$', 'app.customer.views.statistics_view.trade_in_detail', name='trade_in_detail_statistics'),
    # url(r'^statistics/wd_out$', 'app.customer.views.statistics_view.withdraw_out', name='withdraw_out_statistics'),
    # url(r'^statistics/wd_out_detail$', 'app.customer.views.statistics_view.withdraw_out_detail', name='withdraw_out_detail_statistics'),
)

