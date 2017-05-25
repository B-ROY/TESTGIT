#!/usr/bin/env python
# -*- coding:utf-8 -*-
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
from app.customer.models.platform import *
import datetime
import csv
from django.http import StreamingHttpResponse
import codecs

@login_required
def output(request):

	date = request.GET.get('search_date')
	if date:
		timeArray_min = time.strptime(date, "%Y-%m-%d")
		timeStamp_min = int(time.mktime(timeArray_min))
		timeStamp_max = timeStamp_min+86400

		user_room = LiveRoom.objects.filter(closed_at__gte=timeStamp_min).order_by('owner', '-created_at')
		user_room = user_room.filter(created_at__lt=timeStamp_max).order_by('owner', '-created_at')

		user_room = user_room.filter(owner__is_parttime=1)
		status = [u'正在直播', u'已关闭', u'被封号', u'涉黄被封']

		filename = date + u'兼职主播记录.csv'

		with open(filename, 'wb') as csvfile:
			csvfile.write(codecs.BOM_UTF8)
			spamwriter = csv.writer(csvfile, dialect='excel')
			spamwriter.writerow([date + u'兼职主播记录'])
			spamwriter.writerow([u'房间id', u'房间名', u'用户id', u'用户名', u'粒子数', u'状态', u'开始时间',u'结束时间', u'累计时长'])
			for room in user_room:
				if room.closed_at:
					if room.closed_at > timeStamp_max:
						created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(room.created_at))
						closed_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp_max))
						duration = time.strftime("%H:%M", time.localtime(timeStamp_max - room.created_at - 28800))
					elif room.created_at < timeStamp_min:
						created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp_min))
						closed_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(room.closed_at))
						duration = time.strftime("%H:%M", time.localtime(room.closed_at - timeStamp_min - 28800))
					else:
						created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(room.created_at))
						closed_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(room.closed_at))
						duration = time.strftime("%H:%M", time.localtime(room.closed_at - room.created_at - 28800))

#				created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(room.created_at))
#				if room.closed_at:
#					closed_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(room.closed_at))
#					duration = time.strftime("%H:%M", time.localtime(room.closed_at - room.created_at - 28800))

				else:
					closed_at = '-'
					duration = '-'
				spamwriter.writerow([room.id, room.name, room.owner.uuid, room.owner.nickname, room.owner.ticket, status[room.status-1], created_at, closed_at, duration])

	def file_iterator(file_name, chunk_size=512):
		with open(file_name) as f:
			while True:
				c = f.read(chunk_size)
				if c:
					yield c
				else:
					break

	the_file_name = filename
	response = StreamingHttpResponse(file_iterator(the_file_name))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(date + u'.csv')

	return response

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))