from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Testimonial, PollAnswer, PollQuestion, ProfileAnswers, ProfileQuestion, Profile

# Create your views here.

def votes_sort_key(item):
    return len(item[1])

def home(request):
    if request.method == 'GET':
        if request.user and not request.user.is_anonymous:
            logged_in = True
        else:
            logged_in = False
        if logged_in:
            user = User.objects.filter(username=request.user.username).first()
            user_profile = Profile.objects.filter(user=user).first()
            testimonials = Testimonial.objects.filter(given_to=user_profile).order_by('-id')
            poll_questions = PollQuestion.objects.all()
            polls = {}
            for question in poll_questions:
                answers = PollAnswer.objects.filter(question=question)
                answers_count = answers.count()
                poll_dict = {}
                for answer in answers:
                    if answer.answer in poll_dict.keys():
                        poll_dict[answer.answer].append(answer.voted_by)
                    else:
                        poll_dict[answer.answer] = [answer.voted_by]
                polls[(question, answers_count)] = sorted(poll_dict.items(), key=votes_sort_key, reverse=True)
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
        return error404(request)


def profile(request, username):
    if request.method == 'GET':
        if request.user and not request.user.is_anonymous:
            user = User.objects.filter(username=request.user.username).first()
            user_profile = Profile.objects.filter(user=user).first()
            profile_user = User.objects.filter(username=username).first()
            if profile_user==user:
                myprofile = True
            else:
                myprofile = False
            if profile_user:
                profile = Profile.objects.filter(user=profile_user).first()
                testimonials = Testimonial.objects.filter(given_to=profile).order_by('-id')
                profile_questions =ProfileQuestion.objects.all()
                profile_answers = ProfileAnswers.objects.filter(profile=profile)
                mytestimonial = testimonials.filter(given_by=user_profile).first()
                answers={}
                for question in profile_questions:
                    answers[question] = profile_answers.filter(question=question).first()
                context = {
                    'logged_in': True,
                    'myprofile': myprofile,
                    'user': user,
                    'testimonials': testimonials,
                    'mytestimonial': mytestimonial,
                    'profile': profile,
                    'answers': answers
                }
                return render(request, 'profile.html', context)
            else:
                return error404(request)
        else:
            profile_user = User.objects.filter(username=username).first()
            if profile_user:
                profile = Profile.objects.filter(user=profile_user).first()
                testimonials = Testimonial.objects.filter(given_to=profile).order_by('-id')
                profile_questions = ProfileQuestion.objects.all()
                profile_answers = ProfileAnswers.objects.filter(profile=profile)
                answers = {}
                for question in profile_questions:
                    answers[question] = profile_answers.filter(question=question).first()
                context = {
                    'logged_in': False,
                    'testimonials': testimonials,
                    'profile': profile,
                    'answers': answers
                }
                return render(request, 'profile.html', context)
            else:
                return error404(request)
    else:
        return error404(request)

def search(request):
    if request.method == 'GET':
        if request.user and not request.user.is_anonymous:
            user = User.objects.filter(username=request.user.username).first()
            key = request.GET.get("key","")
            if key and key!="":
                profiles = Profile.objects.filter(user__first_name__contains=key)
            else:
                return HttpResponseRedirect(reverse('home'))
            context = {
                'logged_in': True,
                'user': user,
                'profiles': profiles
            }
            return render(request, 'search.html', context)
        else:
            key = request.GET.get("key", "")
            if key and key != "":
                profiles = Profile.objects.filter(user__first_name__contains=key)
            else:
                return HttpResponseRedirect(reverse('home'))
            context = {
                'logged_in': False,
                'profiles': profiles
            }
            return render(request, 'search.html', context)
    else:
        return error404(request)

def login(request):
    if request.method == 'GET':
        if request.user and not request.user.is_anonymous:
            user = User.objects.filter(username=request.user.username).first()
            context = {
                'logged_in': True,
                'user': user,
            }
            return render(request, 'login.html', context)
        else:
            next = request.GET.get('next',"/")
            context = {
                'logged_in': False,
                'next': next
            }
            return render(request, 'login.html', context)
    else:
        return error404(request)

# def edit_profile(request):
#     if request.method == 'GET':
#         if request.user and not request.user.is_anonymous:
#
#
@login_required
def add_testimonial(request, username):
    if request.method == 'GET':
        return error404(request)
    else:
        given_by = User.objects.filter(username=request.user.username).first()
        given_by = Profile.objects.filter(user=given_by).first()
        given_to = User.objects.filter(username=username).first()
        if given_to:
            if given_to == given_by:
                return JsonResponse({'status': 0, 'error': "You can't write a testimonial for yourself"})
            given_to = Profile.objects.filter(user=given_to).first()
            content = request.POST.get("content","")
            if len(content)<200 and content!="":
                old_testimonial = Testimonial.objects.filter(given_to=given_to, given_by=given_by).first()
                if old_testimonial:
                    old_testimonial.content = content
                    old_testimonial.save()
                    return JsonResponse({'status': 1, 'message':"edited"})
                else:
                    Testimonial.objects.create(given_to=given_to, given_by=given_by, content=content)
                    return JsonResponse({'status':1, 'message':"added"})
            else:
                return JsonResponse({'status':0, 'error':"Testimonial content size out of bounds"})
        else:
            return JsonResponse({'status':0, 'error':"User doesn't exist"})

@login_required
def delete_testimonial(request):
    if request.method == 'GET':
        return error404(request)
    else:
        user = User.objects.filter(username=request.user.username).first()
        testimonial_id = int(request.POST.get("testimonial_id",-1))
        if testimonial_id and testimonial_id!=-1:
            testimonial = Testimonial.objects.filter(id=testimonial_id).first()
            if testimonial:
                if user==testimonial.given_to.user or user==testimonial.given_by.user:
                    testimonial.delete()
                    return JsonResponse({'status': 1, 'message': "Testimonial deleted successfully"})
                else:
                    return JsonResponse({'status': 0, 'error': "You are not authorised to delete this"})
            else:
                return JsonResponse({'status': 0, 'error': "Testimonial doesn't exist"})
        else:
            return JsonResponse({'status': 0, 'error': "Testimonial doesn't exist"})

@login_required
def change_answer(request,username):
    if request.method == 'GET':
        return error404(request)
    else:
        user = User.objects.filter(username=request.user.username).first()
        profile_user = User.objects.filter(username=username).first()
        if user==profile_user:
            question_id = int(request.POST.get("question_id", -1))
            profile = Profile.objects.filter(user=user).first()
            if question_id and question_id != -1:
                new_answer = request.POST.get("answer", -1)
                if len(new_answer) < 200 and new_answer != -1:
                    question = ProfileQuestion.objects.filter(id=question_id).first()
                    if question:
                        answer = ProfileAnswers.objects.filter(question=question, profile=profile).first()
                        if answer:
                            answer.answer = new_answer
                            answer.save()
                            return JsonResponse({'status': 1, 'message':"edited"})
                        else:
                            ProfileAnswers.objects.create(question=question, profile=profile, answer=new_answer)
                            return JsonResponse({'status': 1, 'message': "added"})
                    else:
                        return JsonResponse({'status': 0, 'error': "Question doesn't exist"})
                else:
                    return JsonResponse({'status': 0, 'error': "Answer size out of bounds"})
            else:
                return JsonResponse({'status': 0, 'error': "Question doesn't exist"})
        else:
            return JsonResponse({'status': 0, 'error': "You are not authorised to change this"})

@login_required
def add_vote(request):
    if request.method == 'GET':
        user = User.objects.filter(username=request.user.username).first()

    else:
        return error404(request)


def error404(request):
    if request.user and not request.user.is_anonymous:
        user = User.objects.filter(username=request.user.username).first()
        context = {
            'logged_in': True,
            'user': user
        }
        return render(request, '404.html', context)
    else:
        return render(request, '404.html')

