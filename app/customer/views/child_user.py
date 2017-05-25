# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from app.customer.models.user import *
from app.customer.models.account import *
from app.customer.models.level import *
from app.customer.common_util.image import UploadImage
from redis_model.queue import GetUserId

from app.picture.models.picture import *
from app.picture.models.comment import *
from PIL import Image, ImageFilter
import multiprocessing

import datetime
import time


class Pages:
    def __init__(self, objects, count):
        self.pages = Paginator(objects, count)

    def pages_to_show(self, page):
        # pages_wanted stores the pages we want to see, e.g.
        #  - first and second page always
        #  - two pages before selected page
        #  - the selected page
        #  - two pages after selected page
        #  - last two pages always
        #
        # Turning the pages into a set removes duplicates for edge
        # cases where the "context pages" (before and after the
        # selected) overlap with the "always show" pages.
        pages_wanted = set([1, 2,
                            page - 2, page - 1,
                            page,
                            page + 1, page + 2,
                            self.pages.num_pages - 1, self.pages.num_pages])

        # The intersection with the page_range trims off the invalid
        # pages outside the total number of pages we actually have.
        # Note that includes invalid negative and >page_range "context
        # pages" which we added above.
        pages_to_show = set(self.pages.page_range).intersection(pages_wanted)
        pages_to_show = sorted(pages_to_show)

        # skip_pages will keep a list of page numbers from
        # pages_to_show that should have a skip-marker inserted
        # after them.  For flexibility this is done by looking for
        # anywhere in the list that doesn't increment by 1 over the
        # last entry.
        skip_pages = [x[1] for x in zip(pages_to_show[:-1],
                                        pages_to_show[1:])
                      if (x[1] - x[0] != 1)]

        # Each page in skip_pages should be follwed by a skip-marker
        # sentinel (e.g. -1).
        for i in skip_pages:
            pages_to_show.insert(pages_to_show.index(i), -1)

        return pages_to_show

@login_required
def child_user_list(request):
    key = request.GET.get('search_kw', '')
    order_key = request.GET.get('order_kw','')
    users = User.objects.all().filter(user_type=2).order_by('-id')

    if key:
    	try:
            skey = int(key)
            users = users.filter(id=skey)
            if not users:
                users = User.objects.filter(identity=skey)
        except Exception, e:
            users = users.filter(nickname__contains=key)

    if order_key:
        keyNum = int(order_key)
        # users = users.order_by('-' + OrderKey.to_s(order_key))
        users = User.objects.filter(gender=keyNum)

    else:
        users = users.order_by('-created_at')

#    for user in users:
#    	user.account = Account.objects.get(user=user)

    pages = Pages(users, 20)
    page = request.GET.get('page')


    try:
        show_users = pages.pages.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_users = pages.pages.page(1)
        page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_users = pages.pages.page(pages.num_pages)

    for user in show_users:
        user.account = Account.objects.get(user=user)

    return render(request, 'child_user/child_user_list.html',
        {'users': show_users, 'pages_to_show': pages.pages_to_show(int(page)), 'search_kw': key,'order_kw': order_key, })


@login_required
def child_user_edit(request):
    if request.method == "GET":
        user_id = request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        user.birth_date = user.birth_date.date()

    else:
        user_id = request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        
        qd = request.POST 
        nickname = qd.get('edit_nickname')
        birth_date = qd.get('edit_birth_date')
        gender = int(qd.get('edit_gender', '0'))
        area = qd.get('edit_area', '')
        blood_type = qd.get('edit_blood_type', '')
        emotional = qd.get('edit_emotional', '')
        occupation = qd.get('edit_occupation', '')
        desc = qd.get('edit_desc', '')

        user.nickname = nickname
        user.birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
        user.constellation = User.zodiac(birth_date)
        user.gender = gender
        user.area = area
        user.blood_type = blood_type
        user.emotional = emotional
        user.occupation = occupation
        user.desc = desc
        user.save()

    return render(request, 'child_user/child_user_edit.html',
        {'user': user, })

@login_required
def child_user_upload(request):
    if request.method == "POST":
        image = request.FILES.get('edit_image')
        if not image:
            return HttpResponse(u'请添加照片')
        user_id = request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        idata = image.read()
        data = UploadImage.push_binary_to_qclude(idata)
        url = data.get("data",{}).get('download_url','')
        user.image = User.convert_http_to_https(url)
        user.save()

        return HttpResponse(u'上传成功')
    else:
        return HttpResponse(u'上传失败')

@login_required
def child_user_account(request):
    #if request.method == "GET":
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)
    account = Account.objects.get(user=user)
    
    orders = TradeBalanceOrder.objects.filter(user=user).order_by('-buy_time')[0:10]
    records = TradeDiamondRecord.objects.filter(user=user).order_by('-created_time')[0:10]
    #else:

    return render(request, 'child_user/child_user_account.html',
        {'user': user, 'account': account, 'orders': orders, 'records': records, })

@login_required
def child_user_add(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        gold = int(request.POST.get('edit_user_gold', 0))
        exp = int(request.POST.get('edit_user_exp', 0))
        if gold == 0 and exp == 0:
            return HttpResponse(u'请输入金币或经验')

        if exp != 0:
            _level = Level.objects.get(pk=1)
            user.level = _level
            user.level_desc = str(_level.grade)
            user.last_experience = str(_level.experience)
            user.experience = 0
            user.add_experience(exp)

        if gold != 0:
            order = TradeBalanceOrder(
                user=User.objects.get(id=user_id),
                rule=TradeBalanceRule.objects.get(money=1),
                diamon=gold,
                money=1,
                desc=u'小号加金币订单',
                buy_time=datetime.datetime.now(),
                filled_time=datetime.datetime.now(),
                trade_type=0,
                fill_in_type=6,
                platform=4,
                status=1,
                order_id=None,
                out_order_id=None,
            )
            order.save()
        
            account = Account.objects.get(user=User.objects.get(id=user_id))
            before_balance = account.diamond
            after_balance = before_balance+gold
            record = TradeDiamondRecord(
                user=User.objects.get(id=user_id),
                before_balance=before_balance,
                after_balance=after_balance,
                diamon=gold,
                desc=u'小号充值',
                created_time=datetime.datetime.now(),
                trade_type=0,
            )
            record.save()
        
            account.last_diamond = account.diamond
            diamond = account.last_diamond + gold
            account.diamond = diamond
            account.update_time = datetime.datetime.now()
            account.save()

        return HttpResponse(u'更改成功')
    
    else:
        return render(request, "child_user/child_user_add.html",
            {'user': user, })

@login_required
def child_user_create(request):
    if request.method == "POST":
        image = request.FILES.get('edit_image')

        qd = request.POST
        nickname = qd.get('edit_nickname')
        birth_date = qd.get('edit_birth_date')
        gender = int(qd.get('edit_gender', '0'))
        area = qd.get('edit_area', '')
        blood_type = qd.get('edit_blood_type', '')
        emotional = qd.get('edit_emotional', '')
        occupation = qd.get('edit_occupation', '')
        desc = qd.get('edit_desc', '')
        
        t = datetime.datetime.now().timetuple()  
        timeStamp = str(int(time.mktime(t)))
        openid = "wala_childuser1234" + timeStamp

        if not image:
            image = 'https://hdlive-10048692.image.myqcloud.com/5c8ff8bdc5a3645edcd8d4f9313f29e7'
        else:
            idata = image.read()
            data =  UploadImage.push_binary_to_qclude(idata)
            image = data.get("data", {}).get('download_url', '')

        user = User(
            id=User.objects.all().count()+1,
            openid=openid,
            source=0,
            nickname=nickname,
            gender=gender,
            area=area,
            platform=0,
            province="",
            country="",
            city="",
            experience=0,
            ticket=0,
            total_ticket=0,
            locked_ticket=0,
            cost=0,
            contribute_experience=0,
            contribute_ticket=0,
            desc=desc,
            is_block=0,
            image = User.convert_http_to_https(image),
            user_type=0,
            is_bot=2,
            constellation=User.zodiac(birth_date),
            occupation=occupation,
            blood_type=blood_type,
            birth_date=datetime.datetime.strptime(birth_date, '%Y-%m-%d'),
            emotional=emotional,
            created_at=datetime.datetime.now()
        )

        _level = Level.objects.get(pk=1)
        user.level = _level
        user.level_desc = str(_level.grade)
        user.last_experience = str(_level.experience)
        
        user_identity = LuckIDInfo.objects.filter(id_assign=0, id_type=0).order_by('id').first()
        user_identity.id_assign = 1
        user_identity.save()
        user.identity = int(user_identity.user_id)
        #user.identity = 3000000 + int(timeStamp) % 10000
        #ruid = GetUserId("HeyDo_NorNumBlock")
        #user.identity = ruid.get_user_id()
        user.save()

        account = Account(user=user)
        account.save()

        #if not image:
        #    is_new, user = User.create_user(openid=openid,source=0,nick=nickname,platform=2)
        #else:
        #    idata = image.read()
        #    data = UploadImage.push_binary_to_qclude(idata)
        #    image = data.get("data",{}).get('download_url','')
        #    is_new, user = User.create_user(openid=openid,source=0,nick=nickname,platform=2,headimgurl=image)

        #user.birth_date = birth_date
        #user.gender = gender
        #user.area = area
        #user.blood_type = blood_type
        #user.emotional = emotional
        #user.occupation = occupation
        #user.desc = desc
        #user.user_type = 2
        #user.save()

        return HttpResponse(u'创建成功')

    else:
        return render(request, 'child_user/child_user_create.html')

@login_required
def child_user_picture(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)
    account = Account.objects.get(user=user)
    pictures = PictureInfo.objects.filter(user_id=user_id).order_by('status', '-created_at')

    pages = Pages(pictures, 20)
    page = request.GET.get('page')

    try:
        show_pictures = pages.pages.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_pictures = pages.pages.page(1)
        page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_pictures = pages.pages.page(pages.num_pages)

    for picture in show_pictures:
        picture.purchase_count = len(picture.purchase_list)
        picture.comment_count = len(picture.comment)

    return render(request, 'child_user/child_user_picture.html',
        {'user': user, 'account': account, 'pictures': show_pictures, 'pages_to_show': pages.pages_to_show(int(page)), 
        'extra': "&user_id=%s" % user_id, })

@login_required
def child_picture_delete(request):
    picture_id = request.GET.get('id')
    user_id = request.GET.get('user_id')
    PictureInfo.delete_picture(picture_id, user_id)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def child_pictureinfo(request):
    picture_id = request.GET.get('id')
    picture = PictureInfo.objects.get(id=picture_id)
    user = User.objects.get(id=picture.user_id)

    purchase_list = []
    like_list = []
    comment_list = []
    for purchase_user in picture.purchase_list:
        purchase_member = User.objects.get(id=purchase_user)
        purchase_list.append(purchase_member)

    for like_user in picture.like_user:
        like_member = User.objects.get(id=like_user)
        like_list.append(like_member)

    comments = picture.comment
    comments.reverse()
    for comment_id in comments:
        comment_member = CommentInfo.objects.get(id=comment_id)
        comment_member.user = User.objects.get(id=comment_member.user_id)
        comment_list.append(comment_member)

    return render(request, 'child_user/child_pictureinfo.html', 
        {'picture': picture, 'user': user, 'purchase_list': purchase_list, 'like_list': like_list, 'comment_list': comment_list, })

@login_required
def child_pictureadd(request):
    user_id = request.GET.get('user_id')
    price_list = PicturePriceList.objects.all()

    return render(request, 'child_user/child_pictureadd.html', 
        {'price_list': price_list, 'user_id': user_id, })


@login_required
def child_picturecreate(request):
    user_id = request.GET.get('user_id')
    price_list = PicturePriceList.objects.all()
    picture = request.FILES.get('edit_picture')
    qd = request.POST
    price = int(qd.get('edit_price', '0'))
    desc = qd.get('edit_desc', '')
    
    if desc == "":
        return HttpResponse(u'请添加描述!')

    if not picture:
        return HttpResponse(u'请添加图片!')
    else:
        if price == 0:
            idata = picture.read()
            data =  UploadImage.push_binary_to_qclude(idata, price)
            picture_url = data.get("data", {}).get('download_url', '')
            new_url = picture_url
        else:
            name = '/Users/JT/Desktop/1.jpg'
            new_name = '/Users/JT/Desktop/2.jpg'
            new_url = 'https://hdlive-10048692.image.myqcloud.com/5c8ff8bdc5a3645edcd8d4f9313f29e7'

            idata = picture.read()
            pic = open(name, 'wb')
            pic.write(idata)
            data =  UploadImage.push_binary_to_qclude(idata, price)
            picture_url = data.get("data", {}).get('download_url', '')
            pic.close()

            #image = Image.open(name)
            #image = image.filter(MyGaussianBlur(radius=40))
            #image.save(new_name)

            #new_pic = open(new_name, 'rb')
            #data = UploadImage.push_binary_to_qclude(new_pic)
            #new_url = data.get("data", {}).get('download_url', '')
            #new_pic.close()
    
    lock_list = [0]
    for pic_price in price_list:
        lock_list.append(pic_price.picture_price)
    lock_type = lock_list.index(price)

    created_at = datetime.datetime.now()

    try:
        picture = PictureInfo(
            user_id=user_id,
            created_at=created_at,
            picture_url=User.convert_http_to_https(new_url),
            picture_real_url=User.convert_http_to_https(picture_url),
            comment=None,
            desc=desc,
            picture_type="",
            price=price,
            is_private=1,
            lock_type=lock_type,
            lock_count=0,
            purchase_list=None,
            location="",
            mention=None,
            like_user=None,
            like_count=0,
            view_count=0,
            status=0,
        )
        picture.save()

        if price != 0:
            lock = multiprocessing.Lock()
            p = multiprocessing.Process(target=PictureInfo.generate_blurred_picture, args=(lock, picture_url, lock_type, picture.id))
            p.start()

        return HttpResponse(u'添加图片成功!')

    except Exception,e:
        logging.error("create picture error:{0}".format(e))
        return HttpResponse(u'添加图片失败!')
    


@login_required
def child_comment_delete(request):
    comment_id = request.GET.get('comment_id')
    user_id = request.GET.get('user_id')

    status = PictureInfo.delete_comment(comment_id, user_id)
    
    if status:
        return HttpResponse(u'删除成功')
    else:
        return HttpResponse(u'删除失败')

@login_required
def child_comment_create(request):
    picture_id = request.GET.get('picture_id')
    qd = request.POST
    identity = qd.get('edit_user_identity')
    comment = qd.get('edit_user_comment')

    try:
        user = User.objects.get(identity=int(identity))
        created_at = datetime.datetime.now()
        status = PictureInfo.create_comment(picture_id=picture_id, user_id=user.id, created_at=created_at, comment=comment)
        if status:
            return HttpResponse(u'创建评论成功')
        else:
            return HttpResponse(u'创建评论失败')

    except User.DoesNotExist:
        return HttpResponse(u'用户不存在')
















