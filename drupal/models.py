from django.db import models

class DrupalUser(models.Model):
    uid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=180, unique=True)
    pass_field = models.CharField(max_length=384, db_column='pass')
    mail = models.CharField(max_length=762, blank=True)
    theme = models.CharField(max_length=765)
    signature = models.CharField(max_length=765)
    signature_format = models.CharField(max_length=765, blank=True)
    created = models.IntegerField()
    access = models.IntegerField()
    login = models.IntegerField()
    status = models.IntegerField()
    timezone = models.CharField(max_length=96, blank=True)
    language = models.CharField(max_length=36)
    picture = models.IntegerField()
    init = models.CharField(max_length=762, blank=True)
    data = models.TextField(blank=True)
    class Meta:
        db_table = u'users'
