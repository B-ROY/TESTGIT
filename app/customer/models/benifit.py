#coding=utf-8

from mongoengine import *
import datetime
from base.settings import CHATPAMONGO
from app.customer.models.user import User, UserInviteCode
import logging

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class TicketAccount(Document):

    """
        record the user'e benifit
    """
    user = GenericReferenceField("User", verbose_name=u'用户')
    total_ticket = FloatField(verbose_name=u"总收益")
    gift_ticket = FloatField(verbose_name=u"礼物收益")
    call_ticket = FloatField(verbose_name=u"通话收益")
    video_ticket = FloatField(verbose_name=u"私房视频收益")
    friend_charge_ticket = FloatField(verbose_name=u"好友充值收益")
    friend_benifit_ticket = FloatField(verbose_name=u"好友收益收益")
    money_requesting = FloatField(verbose_name=u"申请中的提现")
    money = FloatField(verbose_name=u"可提现金额")
    money_withdrawed = FloatField(verbose_name=u"已提现额")
    bonus_ticket = FloatField(verbose_name=u"由bonus_diamond获得的额外收益")
    last_ticket = FloatField(verbose_name=u"最后一次变更之前的收益")
    update_time = DateTimeField(verbose_name=u"最后更新时间")


    WITHDRAW_RATIO = 0.6
    INVITE_TICKET_RATIO = 0.1

    INVITE_CHARGE_RATIO = 0.1
    INVITE_CHARGE_WITHDRAW_RATIO =0.6

    @classmethod
    def add_inviter_charge_ticket(cls, user_id, charge):
        invite_record = UserInviteCode.objects.filter(user_id=user_id).first()
        if invite_record:
            invite_user = User.objects.get(id=invite_record.invite_id)

            TicketAccount.objects(user=invite_user).update(
                set__update_time=datetime.datetime.now(),
                inc__total_ticket=charge * cls.INVITE_CHARGE_RATIO,
                inc__friend_charge_ticket=charge * cls.INVITE_CHARGE_RATIO,
                inc__money=charge * cls.INVITE_CHARGE_RATIO * cls.INVITE_CHARGE_WITHDRAW_RATIO
            )

    def add_ticket(self, desc, trade_type, ticket):
        from app.customer.models.account import TradeTicketRecord
        try:
            to_user_bill = TradeTicketRecord(
                user=self.user,
                before_balance=self.user.ticket,
                after_balance=self.user.ticket + ticket,
                desc=desc,
                ticket=ticket,
                created_time=datetime.datetime.now(),
                trade_type=trade_type,
            )
            to_user_bill.save()

            self.update(
                set__update_time=datetime.datetime.now(),
                inc__gift_ticket=ticket if trade_type == TradeTicketRecord.TradeTypeGift else 0,
                inc__call_ticket=ticket if trade_type == TradeTicketRecord.TradeTypeAudio else 0,
                inc__video_ticket=ticket if trade_type == TradeTicketRecord.TradeTypePrivateVideo else 0,
                inc__total_ticket=ticket,
                inc__money=ticket * self.WITHDRAW_RATIO
            )

            invite_record = UserInviteCode.objects.filter(user_id=self.user.id).first()

            if invite_record:
                invite_user = User.objects.get(id=invite_record.invite_id)
                withdraw_bonus_rario = WithdrawBonusRatio.objects.filter(user_type=invite_user.user_type).order_by(
                    "create_time").first()
                if withdraw_bonus_rario:
                    ratio = withdraw_bonus_rario.ratio
                else:
                    ratio = 0.6
                TicketAccount.objects(user=invite_user).update(
                    set__update_time=datetime.datetime.now(),
                    inc__total_ticket=ticket * self.INVITE_TICKET_RATIO,
                    inc__money=ticket * self.INVITE_TICKET_RATIO * ratio,
                    inc__friend_benifit_ticket=ticket * self.INVITE_TICKET_RATIO
                )

        except Exception, e:
            logging.error("add ticket error " + str(e))




class WithdrawBonusRatio(Document):
    """
       用户类型不同 分成比例不同
  tornado/docs/index.rst  """
    user_type = IntField(verbose_name=u"用户类型")
    ratio = FloatField(verbose_name=u"提成比例")
    create_time = DateTimeField(verbose_name=u'规则创建时间')
