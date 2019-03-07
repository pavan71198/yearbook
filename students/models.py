from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    btech = 'bt'
    mtech = 'mt'
    phd = 'ph'
    msc = 'ms'
    bdes = 'bd'
    mdes = 'md'
    program_values = (
        (btech, 'BTech'),
        (mtech, 'MTech'),
        (phd, 'PhD'),
        (msc, 'MSc'),
        (bdes, 'BDes'),
        (mdes, 'MDes')
    )
    cse = 'cse'
    ee = 'ee'
    department_values = (
        (cse, 'Computer Science and Engineering'),
        (ee, 'Electrical Engineering')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rollno = models.IntegerField()
    program = models.CharField(max_length=2, choices=program_values)
    department = models.CharField(max_length=3, choices=department_values)
    bio = models.TextField(max_length=1000)
    webmail = models.EmailField(max_length=50, default="")
    profile_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name+" "+str(self.rollno)


class Testimonial(models.Model):
    given_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='given_by')
    content = models.TextField(max_length = 1000)
    given_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='given_to')

    def __str__(self):
        return self.given_by.first_name+" "+self.given_by.last_name+" -> "+self.given_to.first_name+" "+self.given_to.last_name

class PollQuestion (models.Model):
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question

class PollAnswer (models.Model):
    answer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='voted_to')
    question = models.ForeignKey(PollQuestion, null=True, on_delete=models.SET_NULL)
    voted_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='voted_by')

    def __str__(self):
        return self.question.question+" "+self.voted_by.first_name+" "+self.voted_by.last_name+" -> "+self.answer.first_name+" "+self.answer.last_name


class ProfileQuestion (models.Model):
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question

class ProfileAnswers (models.Model):
    profile = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(ProfileQuestion, null=True, on_delete=models.SET_NULL)
    answer = models.TextField(max_length = 1000)

    def __str__(self):
        return self.question.question+" "+self.profile.user.first_name+" "+self.profile.user.last_name
