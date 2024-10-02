from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect,render,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def signup_view(request):
    if request.user.is_authenticated and request.user.is_superuser==False:
        return redirect('home')
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

         
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')
 
 
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'signup.html')


        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken.')
            
            return render(request, 'signup.html')
           

        
        user = User.objects.create_user(username=username, email=email, password=password)

      
        return redirect('home')

    return render(request, 'signup.html')


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url='login')  
def home(request):
    user=request.user
    return render(request, 'home.html',{'user':user})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def login_view(request):
    if request.user.is_authenticated and request.user.is_superuser==False:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
 
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser==False:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')



@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def logout_view(request):
    logout(request)
    return redirect('login')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser==True:
        return redirect('admin_panel')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
           if user.is_superuser:
              login(request,user)
              return redirect('admin_panel')
            
    return render(request,'admin_login.html')


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url='admin_login')  
def admin_panel(request):
    user=User.objects.all()
    if request.method=='POST':
      name=request.POST.get('search')
      user = User.objects.filter(username__icontains=name)

    
    return render(request,'adminpanel.html',{'user':user})



@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url='admin_login')
def add_user(request):
       
    if request.method == 'POST': 
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')
        
       
        if password == confirm_password:
            count=0
            if User.objects.filter(username=username).exists():
                count+=1
                messages.error(request, 'Username already taken.')
            if User.objects.filter(email=email).exists():
                count+=1
                messages.error(request, 'Email already taken.')
            if count==0:
                 user = User.objects.create_user(username=username, email=email, password=password)
                 user.save()
                 messages.success(request, 'user created.')
                 return redirect('admin_panel')
    return render(request,'add.html')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def update(request, id):
   
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
      
        user.username = username
        user.email = email
        user.save() 
        
        return redirect('admin_panel')  
    
    return render(request, "update.html", {"u": user})

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def delete(request,id):
    u=User.objects.filter(id=id)
    u.delete()
    return redirect('admin_panel')

def test(request):
    return render(request,'test.html')
