from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse, Http404

from socialnetwork.forms import LoginForm, RegisterForm, ProfileForm
from socialnetwork.models import Post, Profile, Comment
import json


def login_action(request):
    context = {}

    if request.method == "GET":
        # initialize a new form object (unbound form)
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)
    
    form = LoginForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect('home')

def register_action(request):
    context = {}
    if request.method == "GET":
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)
    
    form = RegisterForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'socialnetwork/register.html', context)
    
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    Profile.objects.create(user=new_user)
    login(request, new_user)

    return redirect('home')

@login_required
def search_action(request):
    # set context with list of posts
    context = {"posts": Post.objects.all().order_by('-creation_time')}
    return render(request, 'socialnetwork/stream.html', context)

def logout_action(request):
    logout(request)
    return redirect('login')

@login_required
def profile_edit(request):
    old_profile = request.user.profile

    # if GET request, return form
    if request.method == 'GET':
        context = {"form": ProfileForm(initial={'bio': request.user.profile.bio})}
        return render(request, 'socialnetwork/profile.html', context)
    
    # if form is not valid
    new_form = ProfileForm(request.POST, request.FILES)
    if not new_form.is_valid():
        context = { "form": new_form }
        return render(request, 'socialnetwork/profile.html', context)
    
    # delete the old profile picture
    old_profile.picture.delete()

    # store the picture and content type to db
    pic = new_form.cleaned_data['picture']
    pic_type = pic.content_type

    old_profile.picture = pic
    old_profile.content_type = pic_type
    old_profile.bio = new_form.cleaned_data['bio']
    old_profile.save()
    
    context = {"form": new_form}
    return render(request, 'socialnetwork/profile.html', context)

@login_required
def get_photo(request, id):
    profile = get_object_or_404(Profile, user=id)

    if not profile.picture:
        raise Http404
    return HttpResponse(profile.picture, content_type=profile.content_type)

@login_required
def get_post_image(request, image_id):
    post_image = get_object_or_404(PostImage, id=image_id)

    if not post_image.image:
        raise Http404
    return HttpResponse(post_image.image, content_type=post_image.content_type)


@login_required
# context field: text, error 
# model used: Post
def global_stream_action(request):
    # set context with list of posts
    context = {"posts": Post.objects.all().order_by('-creation_time')}

    if request.method == "GET":
        return render(request, 'socialnetwork/stream.html', context)
    
    if "text" not in request.POST or not request.POST["text"]:
        context["error"] = "You must enter some text to add"
        return render(request, "socialnetwork/stream.html", context)
    
    new_post = Post(text=request.POST["text"], user=request.user, creation_time=timezone.now())
    new_post.save()

    context = {"posts": Post.objects.all().order_by('-creation_time')}
    return render(request, "socialnetwork/stream.html", context)


@login_required
def follower_stream_action(request):
    context = { "posts": Post.objects.filter(user__in=request.user.profile.following.all()).order_by('-creation_time') }
    return render(request, 'socialnetwork/follower-stream.html', context)

@login_required
def follow_action(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()

    return render(request, 'socialnetwork/other-profile.html', { 'profile':user_to_follow.profile })

@login_required
def unfollow_action(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    
    return render(request, 'socialnetwork/other-profile.html', { 'profile':user_to_unfollow.profile })

@login_required
def other_profile_action(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'socialnetwork/other-profile.html', { 'profile':user.profile })


def get_global(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to view the global stream.", status=401)
    
    response_data = {}
    response_data['posts'] = []
    response_data['comments'] = []
    
    for post_item in Post.objects.all().order_by('creation_time'):
        my_item = {
            'id': post_item.id,
            'text': post_item.text,
            'user_id': post_item.user.id,
            'first_name': post_item.user.first_name,
            'last_name': post_item.user.last_name,
            'creation_time': post_item.creation_time.isoformat()
        }
        response_data['posts'].append(my_item)
    
    for comment_item in Comment.objects.all():
        my_item = {
            'id': comment_item.id,
            'text': comment_item.text,
            'user_id': comment_item.creator.id,
            'first_name': comment_item.creator.first_name,
            'last_name': comment_item.creator.last_name,
            'post_id': comment_item.post.id,
            'creation_time': comment_item.creation_time.isoformat()
        }
        response_data['comments'].append(my_item)
    
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

def get_follower(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to view the follower stream.", status=401)
    
    response_data = {}
    response_data['posts'] = []
    response_data['comments'] = []
    
    # Get posts from users that the current user is following
    following_posts = Post.objects.filter(user__in=request.user.profile.following.all()).order_by('creation_time')
    
    for post_item in following_posts:
        my_item = {
            'id': post_item.id,
            'text': post_item.text,
            'user_id': post_item.user.id,
            'first_name': post_item.user.first_name,
            'last_name': post_item.user.last_name,
            'creation_time': post_item.creation_time.isoformat()
        }
        response_data['posts'].append(my_item)
    
    for comment_item in Comment.objects.filter(post__in=following_posts):
        my_item = {
            'id': comment_item.id,
            'text': comment_item.text,
            'user_id': comment_item.creator.id,
            'first_name': comment_item.creator.first_name,
            'last_name': comment_item.creator.last_name,
            'post_id': comment_item.post.id,
            'creation_time': comment_item.creation_time.isoformat()
        }
        response_data['comments'].append(my_item)
    
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

def add_comment(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to add a comment.", status=401)
    
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter an comment to add.", status=400)
    
    if not 'post_id' in request.POST or not request.POST['post_id']:
        return _my_json_error_response("You must specify a post to add a comment to.", status=400)
    
    # check if post_id is a number
    if not request.POST['post_id'].isdigit():
        return _my_json_error_response("Invalid post ID.", status=400)

    csrf_token = request.POST['csrfmiddlewaretoken']
    if not csrf_token:
        return _my_json_error_response("CSRF verification failed.", status=403)
    
    # check if post exists
    if not Post.objects.filter(id=request.POST['post_id']).exists():
        return _my_json_error_response("The specified post does not exist.", status=400)
    
    post = Post.objects.get(id=request.POST['post_id'])
    
    new_comment = Comment(text=request.POST['comment_text'], creator=request.user, post=post, creation_time=timezone.now())
    new_comment.save()
    
    response_data = {}
    response_data['posts'] = []
    response_data['comments'] = [{
        'id': new_comment.id,
        'text': new_comment.text,
        'user_id': new_comment.creator.id,
        'first_name': new_comment.creator.first_name,
        'last_name': new_comment.creator.last_name,
        'post_id': new_comment.post.id,
        'creation_time': new_comment.creation_time.isoformat()
    }]

    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)
