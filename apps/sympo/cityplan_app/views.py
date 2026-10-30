# Create your views here.
from django.shortcuts import render




from urllib import request
from django.http import HttpResponse
from django.shortcuts import render , redirect
from allauth.socialaccount.models import SocialAccount

## import data tables from database
from .models import cityplan_reg


# Create your views here.
def front_page(request):
    user = request.user
    is_filled_cityplan = False
    submit_form=False
    if user.is_authenticated:
        email = user.email
        is_filled_cityplan = len(cityplan_reg.objects.filter(email1=email))==1

    print(is_filled_cityplan)
    return render(request, "city_front.html",
    {
        'is_filled_cityplan':is_filled_cityplan,
        'submit_form':submit_form
    })



# def front_page(request):
#     return render(request, "city_front.html")



def register_cityplan(request):
    return render(request, "cityplan_form.html")



def registered_cityplan(request):
    if request.method == "POST":

        part1=request.POST.get('part1','')
        contact1=request.POST.get('contact1','')
        email1=request.POST.get('email1','')
        
        part2=request.POST.get('part2','')
        contact2=request.POST.get('contact2','')
        email2=request.POST.get('email2','')
        
        part3=request.POST.get('part3','')
        contact3=request.POST.get('contact3','')
        email3=request.POST.get('email3','')
        
        part4=request.POST.get('part4','')
        contact4=request.POST.get('contact4','')
        email4=request.POST.get('email4','')
        
        ref = request.POST.get('ref', '')

        data=cityplan_reg(participant1=part1,email1=email1,contact1=contact1,participant2=part2,email2=email2,contact2=contact2,participant3=part3,email3=email3,contact3=contact3,participant4=part4,email4=email4,contact4=contact4,ref=ref)
        data.save()
       	submit_form=True
        is_filled_cityplan=True

        

    return  redirect('cityplanning')
#     return  redirect('home')



