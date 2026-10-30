

# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from .models import poster_class
first_time=False
# Create your views here.
#def poster_view(request):
#   return render(request,'poster.html')

def poster_view(request):
    user = request.user
    is_filled_poster=False
#    submit_form=False
    first_time=False
    if user.is_authenticated:
        email = user.email
        is_filled_poster = len(poster_class.objects.filter(email=email))==1
     

    
    return render(request, "poster.html",
    {
        'is_filled_poster':is_filled_poster,
       # 'submit_form':submit_form,
        'first_time':first_time
           })



def poster_submit(request):
    if request.method == "POST":
        user = request.user
        email=user.email
        name1=request.POST.get('name1','')
        mail1=request.POST.get('mail1','')
        mobile1=request.POST.get('mobile2','')
        college=request.POST.get('college','')
        name2=request.POST.get('name2','')
        mail2=request.POST.get('mail2','')
        mobile2=request.POST.get('mobile2','')
        name3=request.POST.get('name3','')
        mail3=request.POST.get('mail3','')
        mobile3=request.POST.get('mobile3','')
        field = request.POST.get('field', '')
        others = request.POST.get('others', '')
        experience = request.POST.get('experience', '')
        ref = request.POST.get('ref', '')        


        data=poster_class(email=email,name1=name1,mail1=mail1,mobile1=mobile1,college=college,name2=name2,mail2=mail2,mobile2=mobile2,name3=name3,mail3=mail3,mobile3=mobile3,field=field,others=others,experience=experience,ref=ref)
        data.save()


    user=request.user
    if user.is_authenticated:
        email = user.email
        is_filled_poster = True

    return render(request, "poster.html",
    {
        'is_filled_poster':is_filled_poster,
        'first_time':first_time
    })

   
       
        
        
