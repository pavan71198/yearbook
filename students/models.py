from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    btech = '01'
    mtech = '42'
    phd = '61'
    msc = '21'
    msr = '43'
    ma = '22'
    bdes = '02'
    mdes = '42'

    program_dict = {
        btech: 'BTech',
        mtech: 'MTech',
        phd: 'PhD',
        msc: 'MSc',
        msr: 'MS-R',
        ma: 'MA',
        bdes: 'BDes',
        mdes: 'MDes'
    }

    program_values = (
        (btech, 'BTech'),
        (mtech, 'MTech'),
        (phd, 'PhD'),
        (msc, 'MSc'),
        (msr, 'MS-R'),
        (ma, 'MA'),
        (bdes, 'BDes'),
        (mdes, 'MDes')
    )

    cse = '01'
    ece = '02'
    me = '03'
    ce = '04'
    dd = '05'
    bsbe = '06'
    cl = '07'
    cst = '22'
    eee = '10'
    ma = '23'
    ph = '21'
    rt = '54'
    ch = '22'
    hss = '41'
    enc = '51'
    env = '52'
    nt = '53'
    lst = '55'

    department_dict = {
        cse: 'CSE',
        ece: 'ECE',
        me: 'ME',
        ce: 'CE',
        dd: 'DD',
        bsbe: 'BSBE',
        cl: 'CL',
        cst: 'CST',
        eee: 'EEE',
        ma: 'MA',
        ph: 'PH',
        rt: 'RT',
        ch: 'CH',
        hss: 'HSS',
        enc: 'ENC',
        env: 'ENV',
        nt: 'NT',
        lst: 'LST'
    }

    department_values = (
        (cse, 'CSE'),
        (ece, 'ECE'),
        (me, 'ME'),
        (ce, 'CE'),
        (dd, 'DD'),
        (bsbe, 'BSBE'),
        (cl, 'CL'),
        (cst, 'CST'),
        (eee, 'EEE'),
        (ma, 'MA'),
        (ph, 'PH'),
        (rt, 'RT'),
        (ch, 'CH'),
        (hss, 'HSS'),
        (enc, 'ENC'),
        (env, 'ENV'),
        (nt, 'NT'),
        (lst, 'LST'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    rollno = models.IntegerField()
    program = models.CharField(max_length=2, choices=program_values)
    department = models.CharField(max_length=3, choices=department_values)
    bio = models.TextField(max_length=1000)

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name


class Testimonial(models.Model):
    given_by = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='given_by')
    content = models.TextField(max_length = 1000)
    given_to = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='given_to')

    def __str__(self):
        return self.given_by.full_name+" -> "+self.given_to.full_name

class PollQuestion (models.Model):
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question

class PollAnswer (models.Model):
    answer = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='voted_to')
    question = models.ForeignKey(PollQuestion, null=True, on_delete=models.SET_NULL)
    voted_by = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='voted_by')

    def __str__(self):
        return self.question.question+" "+self.voted_by.full_name+" -> "+self.answer.full_name


class ProfileQuestion (models.Model):
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question

class ProfileAnswers (models.Model):
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(ProfileQuestion, null=True, on_delete=models.SET_NULL)
    answer = models.TextField(max_length = 1000)

    def __str__(self):
        return self.question.question+" "+self.profile.user.first_name+" "+self.profile.user.last_name