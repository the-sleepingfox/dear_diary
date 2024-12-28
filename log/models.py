from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.

class Entry(models.Model):
    id= models.UUIDField(primary_key=True, default= uuid.uuid4, editable= False)
    heading= models.CharField(max_length= 100)
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    content= models.TextField()
    owner= models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.heading