# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../push_util')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from base.settings import load_django_settings

load_django_settings('live_video.base', 'live_video.app')

#from statistics.models.ugc_and_brand import UgcAndBrand
#from statistics.models.revenue import Revenue
#from statistics.models.fillin_order import FillInOrder
#from statistics.models.fillin_pay_type import FillInPayType
#from statistics.models.premium_user import PremiumUser
from app.customer.models.readlog import *

# 每天0点执行统计
# 0 0 */1 * * python /mydata/python/live_video/background/statistics.py > /dev/null 2>&1 &
if __name__ == '__main__':
    # BusinessStatistics.write_record()
    # UgcAndBrand.write_record()
    # Revenue.write_record()
    # FillInOrder.write_record()
    # FillInPayType.write_record()
    # PremiumUser.write_record()
    GuidStatistics.write_record()
    AudioStatisticsTime.write_record()
    AudioStatisticsId.write_record()
    #PictureStatistics.write_record_db()
    AccountStatistics.write_record()

