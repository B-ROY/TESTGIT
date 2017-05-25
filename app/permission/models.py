#encoding=utf-8
from django.db import models
from django.contrib.auth.models import User,Group


class PagePermission(models.Model):

    code = models.CharField(u'页面权限码', max_length = 64,
                            db_index=True, unique=True, null=True)

    name = models.CharField(u"页面权限名称", max_length=64)
    action = models.CharField(u"Action Name", max_length=64)
    url_regex = models.CharField(u"Url Pattern", max_length=64)

    class Meta:
        verbose_name = u'页面权限'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u"%s" % unicode(self.name)


class UserPerms(models.Model):

    perm = models.ForeignKey(PagePermission)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = u'用户系统权限'
        verbose_name_plural = verbose_name

    @classmethod
    def change_perm(cls, uid, to_delete_perms, to_add_perms):
        #delelte perms
        cls.objects.filter(user_id=uid, perm_id__in=to_delete_perms).delete()
        #add perms
        for perm_id in to_add_perms:
            cls.objects.create(perm_id = perm_id,user_id = uid)


class GroupPerms(models.Model):

    perm = models.ForeignKey(PagePermission)
    group = models.ForeignKey(Group)

    class Meta:
        verbose_name = u'用户组系统权限'
        verbose_name_plural = verbose_name


class CooperateGame(models.Model):

    game_id = models.IntegerField(verbose_name=u'合作游戏id')
    game_name = models.CharField(max_length=32, verbose_name=u'游戏名')

    class Meta:
        verbose_name = u'合作游戏'
        verbose_name_plural = verbose_name


class UserCooperateGames(models.Model):

    game = models.ForeignKey(CooperateGame)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = u'用户对应的游戏'
        verbose_name_plural = verbose_name



