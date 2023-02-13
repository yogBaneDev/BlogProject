from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import *
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

@login_required(login_url='login')
def home(request):
    messages.info(request,'Logged in Successfully')
    blog_form=BlogForm(request.POST or None,request.FILES or None)
    if request.method=="POST":
        if blog_form.is_valid():
            blog=blog_form.save(commit=False)
            blog.user=request.user
            blog.save()
        else:
            messages.info(request,blog_form.errors)
        blog_form=BlogForm()
        Blog_Data=Blogpost.objects.all().values
        return render(request, 'home.html',context={"datas":Blog_Data,"form":blog_form})
    Blog_Data=Blogpost.objects.all().values
    return render(request, 'home.html',context={"datas":Blog_Data,"form":blog_form})

@login_required(login_url='login')
def blog(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        print(search)
        Blog_Data = Blogpost.objects.filter(user=request.user).filter(Q(Title__icontains=search)|Q(Description__icontains=search)|Q(Blog_txt__icontains=search)).values()
        
        return render(request, 'blog.html',context={"datas":Blog_Data})
    Blog_Data= Blogpost.objects.filter(user=request.user)
    return render(request, 'blog.html',context={"datas":Blog_Data})
@login_required(login_url='login')
def all_blog(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        print(search)
        Blog_Data = Blogpost.objects.filter(Q(Title__icontains=search)|Q(Description__icontains=search)|Q(Blog_txt__icontains=search)).values()
        
        return render(request, 'blog.html',context={"datas":Blog_Data})
    Blog_Data= Blogpost.objects.all()
    return render(request, 'blog.html',context={"datas":Blog_Data})
@login_required(login_url='login')    
def detail_blog(request,pk):
    
    Blog_Data=Blogpost.objects.filter(id=pk)
    
    return render(request,'detail_blog.html',context={"datas":Blog_Data})

def edit_blog(request,pk):
    blog_main=Blogpost.objects.get(id=pk)
    blog_form=BlogForm(request.POST or None, request.FILES or None, instance=blog_main)
    if request.method=="POST":
        if blog_form.is_valid():
            blog_edit=blog_form.save(commit=False)
            blog_edit.user=request.user
            blog_edit.save()
        else:
            messages.info(request,blog_form.errors)
        
        return redirect(blog)

    Blog_Data=Blogpost.objects.filter(user=request.user)
    return render(request, 'edit.html',context={"datas":Blog_Data,"form":blog_form})

def blog_delete(request,kp):
    blog_main=Blogpost.objects.get(id=kp)
    blog_main.delete()
    return redirect(blog)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.info(request,'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form =UserRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})

#https://plainenglish.io/blog/user-registration-and-login-authentication-in-django-2f3450479409