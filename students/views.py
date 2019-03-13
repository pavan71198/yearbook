from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.views import auth_logout
from .models import Testimonial, PollAnswer, PollQuestion, ProfileAnswers, ProfileQuestion, Profile

# Create your views here.


def home(request):
    if request.method == 'GET':
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        if logged_in:
            user = User.objects.filter(username=request.user.username).first()
            user_profile = Profile.objects.filter(user=user).first()
            testimonials = Testimonial.objects.filter(given_to=user_profile)
            poll_questions = PollQuestion.objects.all()
            polls = {}
            for question in poll_questions:
                answers = PollAnswer.objects.filter(question=question)
                polls[question] = []
                for answer in answers:
                    polls[question].append((answer.answer, answer.voted_by))
            context = {
                'testimonials': testimonials,
                'polls': polls,
                'user': user,
                'user_profile': user_profile,
                'logged_in': logged_in
            }
            return render(request, 'home.html', context)
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        if logged_in:
            user = User.objects.filter(username=request.user.username).first()
            user_profile = Profile.objects.filter(user=user).first()
            testimonials = Testimonial.objects.filter(given_to=user_profile)
            poll_questions = PollQuestion.objects.all()
            polls = {}
            for question in poll_questions:
                answers = PollAnswer.objects.filter(question=question)
                polls[question] = []
                for answer in answers:
                    polls[question].append((answer.answer, answer.voted_by))
            context = {
                'testimonials': testimonials,
                'polls': polls,
                'user': user,
                'user_profile': user_profile,
                'logged_in': logged_in
            }
            return render(request, 'home.html', context)
        else:
            return HttpResponseRedirect(reverse('login'))


def profile(request, username):
    if request.method == 'GET':
        if request.user and not request.user.is_anonymous:
            user = User.objects.filter(username=request.user.username).first()
            user_profile = Profile.objects.filter(user=user).first()
            profile_user = User.objects.filter(username=username).first()
            profile = Profile.objects.filter(user=profile_user).first()
            testimonials = Testimonial.objects.filter(given_to=profile)
            profile_answers = ProfileAnswers.objects.filter(profile=profile)
            context = {
                'logged_in': True,
                'user': user,
                'user_profile': user_profile,
                'profile_user': profile_user,
                'testimonials': testimonials,
                'profile': profile,
                'answers': profile_answers
            }
            return render(request, 'profile.html', context)
        else:
            profile_user = User.objects.filter(username=username).first()
            testimonials = Testimonial.objects.filter(given_to=profile_user)
            profile = Profile.objects.filter(user=profile_user).first()
            profile_answers = ProfileAnswers.objects.filter(profile=profile)
            context = {
                'logged_in': False,
                'profile_user': profile_user,
                'testimonials': testimonials,
                'profile': profile,
                'answers': profile_answers
            }
            return render(request, 'profile.html', context)
    else:
        if request.user and not request.user.is_anonymous:
            return home(request)
        else:
            return home(request)

def login(request):
    if request.method == 'GET':
        if request.user and not request.user.is_anonymous:
            user = User.objects.filter(username=request.user.username).first()
            context = {
                  'logged_in': True,
                  'user': user
            }
            return render(request, 'login.html', context)
        else:
            context = {
                'logged_in': False
            }
            return render(request, 'login.html', context)
    else:
        if request.user and not request.user.is_anonymous:
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('login'))

# def edit_profile(request):
#     if request.method == 'GET':
#         if request.user and not request.user.is_anonymous:
#
#
@login_required()
def add_testimonial(request, username):
    return HttpResponse("Success")


