
from django.shortcuts import render, Http404, get_object_or_404, redirect, HttpResponse, reverse
from django.shortcuts import render_to_response  
from urllib.parse import quote 
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from blogArabic.forms import MyRegistrationForm
from django.contrib.auth.forms import PasswordChangeForm
from blogArabic.forms import createForm, createAuthor, CommentForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from blogArabic.models import author, articles, Category, contactModel, comment_put
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .token import activation_token
from django.contrib.auth.forms import PasswordChangeForm
from django.template import loader
from django.db.models import Q
from django.template.defaultfilters import slugify
#htiscounter

def base(request):
  div = articles.objects.all()
  context = {
     'div': div
  }
  return render(request, 'base.html', context)

def error_404_view(request, exception):
    return render(request,'blogArabic/404_error.html')



def search(request): 
           all_articles = articles.objects.all().order_by('-id')
             # to search in loggedin page
           search = request.GET.get('q')
           if search:
              messages.success(request, 'تم البحث', extra_tags='search')
              all_articles = all_articles.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)  | 
                Q(article_author__username__icontains=search) 

              )
              #add paginator
           paginator = Paginator(all_articles, 15)  # Show 25 contacts per page

           page = request.GET.get('page')
           total_articles = paginator.get_page(page)
  

           return render(request, 'home/search.html', {'all_articles': total_articles, 
            'full_name': request.user.username})

# Create your views here.
#faq page
def faq(request):
       
        return render(request, 'home/faq.html', {'full_name': request.user.username})

#reset password page
def reset_pass(request):

        return render(request, 'home/reste_pass.html')

#category page
def show_category(request):
        
        query = Category.objects.all()
       
        
        return render(request, 'home/category.html', {"topic": query, 'full_name': request.user.username})

# open home page
def index(request):
         
           all_articles = articles.objects.all().order_by('-id')
           
           solo = articles.objects.order_by('-id')[:1]
           todo = articles.objects.order_by('-id')[:1]
           tolo = articles.objects.filter().order_by('-read')[:1]

           solo1 = articles.objects.filter(category = 9).order_by('-id')[:2] # health category
           first = articles.objects.filter(category = 9).order_by('category')[:6] #health
          

           solo2 = articles.objects.filter(category = 8).order_by('-id')[:2]#sport category
           second = articles.objects.filter(category = 8).order_by('category')[:6] #sport

           solo3 = articles.objects.filter(category = 1).order_by('-id')[:2]#programation
           third = articles.objects.filter(category = 1).order_by('category')[:6]#porramation

           solo4 = articles.objects.filter(category = 10).order_by('-id')[:2] #application
           five = articles.objects.filter(category = 10).order_by('category')[:6] #app

           featured = articles.objects.filter(featured=True).order_by('-featured')[:4]



            # end search 
           
           #show five articles plus read
           article_read = articles.objects.filter().order_by('-read')[:9]
           #show spicial articles
           
           # show first article
          
             # show fourth articles
           fourth = articles.objects.order_by('-id')[:4]

            

           context = {

          
                   'full_name': request.user.username,
                   'testme': 'Hello world!',
                   'first_article':first,
                   'fourth_article':fourth,
                   'all_articles': all_articles,
                   'read': article_read,
                   'solo': solo,
                   'solo1': solo1,
                   'featured': featured,
                   'solo2': solo2,
                   'solo3': solo3,
                   'solo4': solo4,
                   
                   'second': second,
                   'third': third,
                   'five': five,
                   'todo':todo,
                   'tolo': tolo,
                  


           }
         

           return render(request, 'home/index.html', context) 



# about page
def about(request):
        
       
       query = contactModel.objects.order_by('-id')[:4]
       return render(request, 'home/about.html', {'full_name': request.user.username, 'query': query})
#contact page
def contact(request):
        
        
       
        return render(request, 'home/contact.html', {'full_name': request.user.username})
#open login page
def login(request):

    c = {}
    c.update(csrf (request))
    return render_to_response('home/login.html', c)

# function to see if the username and password user there is in database        
def auth_views(request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        

        user  = auth.authenticate(username = username, password = password)

        if user is not None:
                auth.login(request, user)
                # when user have pic profile rederect loggedin page 
                user = get_object_or_404(User, id=request.user.id)
                author_profile = author.objects.filter(name=user.id)
                if author_profile:
                       authorUser = get_object_or_404(author, name=request.user.id)

                       messages.success(request, 'مرحبا بك ', extra_tags='welcome')
                       
                       return HttpResponseRedirect('/')

                # else rederect to chose pic profile
                else:
                           
                           return HttpResponseRedirect('/avatar')
               
                
              
                
        else: 
                
                messages.success(request, 'إسم المستخدم أو كلمة السر غير صحيحة', extra_tags='passwordWrong')
                return HttpResponseRedirect('/')
                




#chose avatar 
def avatar(request):
        return render(request, 'home/avatar.html')

#logout or Desconnect
def logout(request):

    auth.logout(request)
   
    
    return HttpResponseRedirect('/')



# create register function
def register(request):
        
    form = MyRegistrationForm(request.POST or None)
    if form.is_valid():

        instance = form.save(commit=False)
        instance.is_active = False
        instance.save()
        site=get_current_site(request)
        mail_subject="Confirmation message for me"
        message=render_to_string('home/confirm_email.html',{
            'user':instance,
            'domain':site.domain,
            'uid':instance.id,
            'token':activation_token.make_token(instance)
        })
        to_email=form.cleaned_data.get('email')
        to_list=[to_email]
        from_email=settings.EMAIL_HOST_USER
        send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
     
        return HttpResponse("<h1>Thanks for your registration. A confirmation link was sent to your email</h1>")
     
    return render(request, 'home/register.html', {"form": form})


# redrect from register form to avatar html file

def send_pass_link(request):
      email = request.POST.get('email', '')
      user = auth.authenticate(email = email)
      if user is not None:
         site = get_current_site(request)
         mail_subject = "Reset Password"
         message = render_to_string('home/reset_password.html', {
             
            'user':instance,
            'domain':site.domain,
            'uid':user.id,
            'token':activation_token.make_token(user)
         })
         to_email=form.cleaned_data.get('email')
         to_list=[to_email]
         from_email=settings.EMAIL_HOST_USER
         send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
         return HttpResponse("<h1>Thanks we well send you link to reset your password !</h1>")
      return render(request, 'home/reste_pass.html')


# to pass to page to create one article     
def create_article(request):
    
       
        
    if request.user.is_authenticated:

        user = get_object_or_404(User, id=request.user.id)
        
        author_profile = author.objects.filter(name=user.id)

        # check if user has pic profile
        if author_profile:
          #if user has pic profile 
          form = createForm(request.POST or None, request.FILES or None)
          if form.is_valid():
           instance = form.save(commit = False)
           instance.save()
          return render(request, 'home/post.html', {"form": form, 'full_name': request.user.username})
        # if user has not pic profile
        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                ins = form.save(commit = False)
                ins.name = user
                ins.save()
                
                return HttpResponseRedirect('/')
            return render(request, 'home/avatar.html', {"form": form})
    else:
      HttpResponseRedirect('/login')

     
        
    

def publish(request): 
       
        if request.user.is_authenticated:
          user = get_object_or_404(User, id=request.user.id)
          
          author_profile = author.objects.filter(name=user.id)
        
          authorUser = get_object_or_404(author, name=request.user.id)
          
    
          form = createForm (request.POST or None, request.FILES or None)
          

          if form.is_valid():
            
            instance = form.save(commit=False)
           
        # pass instance author
            instance.avatar = authorUser
        # pass instance user login
            instance.article_author = request.user
          

            instance.save()

        #pass from data base to template
            messages.success(request, 'تم نشر المقال', extra_tags='Done')
            redirect_to = reverse('blogArabic:show_article', kwargs={'id': instance.id, 'slug': instance.slug})
            return redirect(redirect_to)
          return render(request, 'home/index.html', {'form': form, 'user': authorUser, 'full_name': request.user.username})
         
        
        else:
          return HttpResponseRedirect('/login')

# show the true link publish(details)
def show_article(request, id, slug):

    
   
    
            # show second article
    post = get_object_or_404(articles, id=id, slug = slug)
    share_title = quote(post.title)
    
    add = comment_put.objects.all().filter(user_put = id).order_by('-id')
    art = articles.objects.get(pk = id, slug = slug)
    first = articles.objects.order_by('-id')[:1]
    three = articles.objects.order_by('-id')[:5]
    th = articles.objects.filter().order_by('-read')[:2]

    is_liked = False
   
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    
    context = {
         'art': art,
         'add': add,
         'share_title': share_title,
         'full_name': request.user.username,
         'post': post,
         'first': first,
         'th':th,
         'three': three,
         'is_liked': is_liked,
         'total_likes': post.total_likes(),
       

          }
    art.read += 1
    art.save(update_fields=('read',))
   
  
    return render(request, 'home/article.html', context)

# show user profile
def show_profile(request, id):
   
    
      
    post = get_object_or_404(author, id=id)
    
    art = articles.objects.filter(avatar=post.id).order_by('-id')
    
   
    context = {
       
         
         'art': art,
         'user': post,
         'full_name': request.user.username,
         
       
          }
   
  
    return render(request, 'home/profile_visited.html', context)


def getProfile(request):
    if request.user.is_authenticated:

        user = get_object_or_404(User, id=request.user.id)
        author_profile = author.objects.filter(name=user.id)

       
        if author_profile:
            authorUser = get_object_or_404(author, name=request.user.id)
            post = articles.objects.filter(avatar=authorUser.id).order_by('-id')

            paginator = Paginator(post, 10)

            page = request.GET.get('page')
            try:
              queryset = paginator.page(page)

            
            except PageNotAnInteger:
                queryset = paginator.page(1) 
            except EmptyPage:
                queryset = paginator.page(paginator.num_pages) 

           


           
         
            return render(request, 'home/profile.html', {"user": authorUser, 'post':  queryset, 'full_name': request.user.username,})

        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                ins = form.save(commit = False)
                ins.name = user
                ins.save()
                
                return HttpResponseRedirect('/')
            return render(request, 'home/avatar.html', {"form": form})

    else:
        return HttpResponseRedirect('/login')







#show solo category articles
def getTopic(request, id, slug):
   
    cat = get_object_or_404(Category, pk=id, slug = slug)
    post = articles.objects.filter(category=cat.id).order_by('-id')
    first_post = articles.objects.filter(category=cat.id).order_by('-id')[:1]
    six_articles = articles.objects.order_by('id')[:6]
    paginator = Paginator(post, 10)  # Show 25 contacts per page

    page = request.GET.get('page')
    total_article = paginator.get_page(page)

    context = {
       "post": total_article,
       'first_post': first_post,
       "cat": cat,
       'six_articles': six_articles,
       'full_name': request.user.username
    }

   
    return render(request, "home/topic.html", context)

def activate(request, uid, token):
    try:
        user = get_object_or_404(User, pk = uid)
    except:
        raise Http404('No user faound')
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('<h1> Account is activated now you can <a href ="/login">login</a></h1>')
    else:
        return HttpResponse('<h3> Invalid activation Link </h3>')   


# to delete user articles
def getDelete(request, pid):
    if request.user.is_authenticated:
        post= articles.objects.get(id = pid)
        post.delete()
        messages.warning(request, 'تم حذف المنشور بنجاح', extra_tags='delete')
        return HttpResponseRedirect('/')

    else:
         return HttpResponseRedirect('/login')

def getUpdate(request, pid):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        post = get_object_or_404(articles, id=pid)
        form = createForm(request.POST or None, request.FILES or None, instance=post)
        # delete the first article
        post.delete()
        # save the update article
        if form.is_valid():

            instance = form.save(commit=False)
            instance.article_author = request.user
            instance.avatar = u
            instance.save()

           
            return HttpResponseRedirect('/profile')
        return render(request, 'home/post.html', {"form": form})
    else:
        return render_to_response('home/login.html')


def contact_comment(request):
     
          username1 = request.POST['username1']
          email = request.POST['email']
          text_body = request.POST['text_body']



          put = contactModel(username1 = username1, email = email, text_body = text_body)
          put.save()
          # must be define this url in urls py file
          messages.success(request,'شكرا تم الإرسال', extra_tags='contactCM' )
          return HttpResponseRedirect('/')


# change password from profile
def change_password(request):
    if request.user.is_authenticated:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit = True)
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'تم تغيير كلمة السر', extra_tags='changed')
            return HttpResponseRedirect('/')
        else:
            messages.success(request, 'تأكد من كلمة السر المدخلقة ...شكرا.', extra_tags='error')
            return HttpResponseRedirect('/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'home/profile.html', {"form": form })  


#terme service page
def terms_service(request):
    return render(request, 'home/termsOfservice.html')


#privacy page
def privacy(request):
    return render(request, 'home/Privacy.html')


def like_post(request):
    post = get_object_or_404(articles, id=request.POST.get('post_id'))
   #post = get_object_or_404(articles, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
    }
    
  
    

    redirect_to = reverse('blogArabic:show_article', kwargs={'id': post.id, 'slug': post.slug})
    return redirect(redirect_to, context)



# save comment user login in database comment_put

def save_comment(request, id):
   
    post = articles.objects.get(id = id)
    user = get_object_or_404(User, id=request.user.id)
    author_profile = author.objects.filter(name=user.id)
    authorUser = get_object_or_404(author, name=request.user.id)
   
    
    if request.method == 'POST':
        f = CommentForm(request.POST)
        if f.is_valid():
            c = f.save(commit = False)
            c.avatar_commenter = authorUser
            c.user_put = post
            c.user_comment = request.user
            c.save()

    add = comment_put.objects.all().order_by('-id')[:1]
    context = {
      'post': post,
      
      
      'add':add,
    
    }
    messages.success(request, 'تم نشر التعليق', extra_tags='commentuser')
    
    redirect_to = reverse('blogArabic:show_article', kwargs={'id': post.id, 'slug': post.slug})
    return redirect(redirect_to, context)






   
