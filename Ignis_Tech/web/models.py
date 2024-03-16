from django.db import models

# define the database of our web applications

# this defines the users database
class Signin(models.Model):
    user_name = models.CharField(max_length=100, default=None)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email

# this defines the events database
class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=200)
    event_image = models.ImageField(upload_to='images/')
    is_liked = models.BooleanField(default=False)
    user_id = models.CharField(max_length=200)



