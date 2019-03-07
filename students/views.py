from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Testimonial, PollAnswer, PollQuestion

# Create your views here.

def home(request):
    if request.method == 'GET':
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        if logged_in:
            user = User.objects.filter(username=request.user.username).first()
            testimonials = Testimonial.objects.filter(given_to=user)
            poll_questions = PollQuestion.objects.all()
            polls = {}
            for question in poll_questions:
                polls[question] = PollAnswer.objects.filter(question=question)
            context = {
                'testimonials' : testimonials,
                'polls' : polls,
                'user' : user,
                'logged_in' : logged_in
            }
            return render(request, 'home.html', context)
        else:
            context = {
                'logged_in' : logged_in
            }
            return render(request, 'home.html', context)
