from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import NewPostForm,NewCommentForm,NewPostImage
from .models import Post,comments,Like,PostImages,Rating
from users.models import Profile
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json
from django.forms import modelformset_factory

from django import template
User = get_user_model()

register =  template.Library()

@register.filter()
def range(min =5):
	return range(min)
# Create your views here.
def index(request):
	post = Post.objects.all().order_by('-date_posted')
	ranpost = Post.objects.order_by('?')
	b={}
	toprate=[]
	for p in post:
		a = 0
		rate = Rating.objects.filter(post = p)
		for r in rate:
			a += r.rating
		print(a,r.post)
		if a != 0:
			b[a] = r.post
	c=sorted(b.items(),reverse=True)
	for val in c:
		toprate.append(val[1])
	context={'post':post[0:6],'allpost':post,'ranpost':ranpost,'toprate':toprate[0:6]}
	return render(request,'feed/index.html',context)


@login_required
def create_post(request):
	user = request.user
	if request.method == 'POST':
		p_form = NewPostForm(request.POST)
		i_form = NewPostImage(request.POST, request.FILES)
		files = request.FILES.getlist('images')
		if p_form.is_valid() and i_form.is_valid():
			p_obj = p_form.save(commit=False)
			p_obj.user_name = user
			p_obj.save()
			for f in files[0:4]:
				if f:
					photo = PostImages(Imgtitle=p_obj, pimages=f)
					photo.save()
			messages.success(request,"Yeeew, check it out on the home page!")
			return redirect("users:dashboard")
	else:
		p_form = NewPostForm()
		i_form = NewPostImage()
	return render(request, 'feed/create_post.html',{'postForm': p_form, 'imageform': i_form})



@login_required
def editpost(request,id):
	print(id)
	details = Post.objects.get(id= id)
	photos = PostImages.objects.filter(Imgtitle= details)
	if request.method != 'POST':
		p_form = NewPostForm(instance = details)
		i_form = NewPostImage()
	else:
		p_form = NewPostForm(instance= details,data=request.POST)
		i_form = NewPostImage(request.POST or None,request.FILES or None)
		files = request.FILES.getlist('images')
		if p_form.is_valid() and i_form.is_valid():
			p_form.save()
			if len(photos) < 4:
				a = 4-len(photos)
				for f in files[0:a]:
					photo = PostImages(Imgtitle = details,pimages=f)
					photo.save()
				return redirect('feed:postdetails',id =id)
			return redirect('feed:postdetails',id =id)
	context = {'postform':p_form,'imageform':i_form,'det':details,'img':photos}
	return render(request,'feed/editpost.html',context)

def postdetails(request,id):
	post = Post.objects.get(id=id)
	photo = PostImages.objects.filter(Imgtitle=post)
	if request.user.is_authenticated:
		is_liked = Like.objects.filter(user = request.user ,post = post)
	else:
		is_liked = None
	comment = comments.objects.filter(post=post, reply= None).order_by('-id')
	rate = Rating.objects.filter(post = post)
	a=0
	for r in rate:
		a += r.rating
	b = (a/len(rate))/10
	
	print(b)

	if request.method == 'POST':
		form = NewCommentForm(request.POST)
		if form.is_valid():
			reply_id = request.POST.get('reply_id')
			print(reply_id)
			reply_com = None
			if reply_id:
				reply_com = comments.objects.get(id = reply_id)
			data = form.save(commit = False)
			data.username = request.user
			data.reply = reply_com
			data.post = post
			data.save()
			return redirect('feed:postdetails', id = post.id)
	else:
		form = NewCommentForm()
	context = {'post':post,'photo':photo,'form':form,'is_liked':is_liked,'comment':comment,'ratevalue':b} 
	return render(request,'feed/postdetails.html',context)

@login_required
def deletepost(request,id):
	post = Post.objects.get(id = id)
	post.delete()
	return redirect('users:dashboard')

def categories(request,value):
	if value == "electrical":
		post = Post.objects.filter(tags = value).order_by("-date_posted")
	elif value == "house":
		post = Post.objects.filter(tags = value).order_by("-date_posted")
	elif value == "office":
		post = Post.objects.filter(tags = value).order_by("-date_posted")
	elif value == "fashion":
		post = Post.objects.filter(tags = value).order_by("-date_posted")
	elif value == "games":
		post = Post.objects.filter(tags = value).order_by("-date_posted")
	elif value == "comming":
		post = Post.objects.filter(tags = value).order_by("-date_posted")
	elif value == "innovation":
		post = Post.objects.filter(adminchoose = value).order_by("-date_posted")
	else:
		post = Post.objects.all().order_by('-date_posted')

	context = {"allpost":post}
	return render(request,'feed/products.html',context)

@login_required
def changeimage(request,imgid,postid,value):
	print(imgid,postid)
	photo = PostImages.objects.get(id = imgid)
	if value == 'change':
		file = request.FILES['images']
		print(photo.pimages)
		print(file)
		photo.pimages = file
		photo.save()
	else:
		photo.delete()
		
	return redirect('feed:editpost',id = postid )


@login_required
def del_comment(request,id,postid):
	comment = comments.objects.get(id = id)
	if comment.username == request.user:
		comment.delete()
	return redirect('feed:postdetails',id = postid)

@login_required
def like(request):
	post_id = request.GET.get("likeId", "")
	user = request.user
	post = Post.objects.get(pk=post_id)
	liked= False
	like = Like.objects.filter(user=user, post=post)
	if like:
		like.delete()
	else:
		liked = True
		Like.objects.create(user=user, post=post)
	resp = {
        'liked':liked
    }
	response = json.dumps(resp)
	return HttpResponse(response, content_type = "application/json")
@login_required
def deletelike(request,id):
	like = Like.objects.get(id = id)
	if like.user == request.user:
		like.delete()
	return redirect('feed:wishlist')

@login_required
def wishlist(request):
	p = request.user.profile
	like = Like.objects.filter(user=request.user)
	context ={'like':like }
	return render(request,'feed/wishlist.html',context)

@login_required
def ratingstar(request):
	post_id = request.GET.get("rateid",)
	value = request.GET.get("ratevalue",)
	user = request.user
	post = Post.objects.get(id = post_id)
	print(post_id,value)
	rate = Rating.objects.filter(user = user,post= post)
	if rate:
		for r in rate:
			r.rating = value
			r.save()
	else:
		Rating.objects.create(user = user , post= post)
	resp = {
        'rated':True
    }
	response = json.dumps(resp)
	return HttpResponse(response, content_type = "application/json")
