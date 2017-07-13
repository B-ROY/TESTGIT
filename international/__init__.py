# -*- coding: utf-8 -*-

import gettext


languages = 'turkey'
gettext.install('inter', '/mydata/python/live_video/international/locale', unicode=False)
gettext.translation('inter', '/mydata/python/live_video/international/locale', languages=['turkey']).install(True)