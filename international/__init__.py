# -*- coding: utf-8 -*-

import gettext
from base.settings import Manifest

languages = Manifest.languages
gettext.install('inter', '/Users/biweibiren/ALLIN_API_OFFICIAL/live_video/international/locale', unicode=False)
gettext.translation('inter', '/Users/biweibiren/ALLIN_API_OFFICIAL/live_video/international/locale', languages=[languages]).install(True)