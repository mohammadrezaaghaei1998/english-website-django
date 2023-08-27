from django.db import models
from django.contrib.auth.models import User



class Package(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    hour = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='package_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    video_file = models.FileField(upload_to='videos/',default=None,null=True)    
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title



class Purchase(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    videos = models.ManyToManyField(Video)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
    



class UserPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE,default=None)
    unlocked = models.BooleanField(default=False)



class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=17, blank=True)
    

    def __str__(self):
        return self.user.username 
    




class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject