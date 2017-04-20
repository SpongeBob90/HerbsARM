from django.db import models

# Create your models here.
class File(models.Model):
    filename = models.CharField(max_length = 30)
    file = models.FileField(upload_to = './app01/static/upload/')

    def __unicode__(self):
        return self.filename

class Transaction(models.Model):
    t_id = models.CharField(max_length = 30)
    herb = models.CharField(max_length = 30)
    weight = models.CharField(max_length = 30)
	
    def __unicode__(self):
        return self.filename