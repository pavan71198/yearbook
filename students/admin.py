from django.contrib import admin
from students.models import Profile,Testimonal, ProfileQuestion, ProfileAnswers, PollQuestion, PollAnswer
# Register your models here.

admin.site.register(Profile)
admin.site.register(Testimonal)
admin.site.register(ProfileQuestion)
admin.site.register(ProfileAnswers)
admin.site.register(PollQuestion)
admin.site.register(PollAnswer)