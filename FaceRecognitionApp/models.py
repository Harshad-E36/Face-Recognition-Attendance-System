from django.db import models

# Create your models here.
class people(models.Model):
  encoding = models.TextField()
  name = models.CharField(max_length=25)
  
  def __str__(self,):
    return self.name

class detection(models.Model):
  name = models.CharField(max_length=25)
  date = models.DateField(auto_now_add=True)
  time = models.TimeField(auto_now_add=True)

  