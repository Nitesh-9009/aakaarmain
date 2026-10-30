from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Import models from other apps
from sympo.cityplan_app.models import cityplan_reg
from sympo.threemtt.models import threemtt
from sympo.poster_app.models import poster_class

## import data tables from database
from .models import Submission, iitb, non_iitb

# Create your views here.
def poster(request):
    return render(request, "poster.html")

def city_front(request):
    return render(request, "city_front.html")

def mtt(request):
    return render(request, "thesis_180.html")

def home(request):
    return render(request, "home_new.html")

def main_view1(request):
    # The ICES landing page. `sympo_main.html` carries the current design;
    # `sympo_page.html` is the superseded layout, kept for reference.
    return render(request, "sympo_main.html")

def new(request):
    return render(request, "new.html")

def academic_home(request):
    return render(request,"academic.html")

def submission(request):
    return render(request, "submission.html")

def main_view(request):
    user = request.user
    is_filled_mtt = False
    is_filled_cityplan = False
    is_filled_poster = False
    
    if user.is_authenticated:
        email = user.email
        # Use .exists() for efficient database checks instead of len()
        is_filled_cityplan = cityplan_reg.objects.filter(email1=email).exists()
        is_filled_mtt = threemtt.objects.filter(email=email).exists()
        is_filled_poster = poster_class.objects.filter(email=email).exists()

    return render(request, "sympo_main.html", {
        'is_filled_cityplan': is_filled_cityplan,
        'submit_form': False,  # Was 'submit_form' in original, kept it
        'is_filled_mtt': is_filled_mtt,
        'is_filled_poster': is_filled_poster
    })

@login_required  # Ensures user is logged in, preventing errors
def submitted(request):
    if request.method == "POST":
        email = request.user.email

        # This dictionary holds all the form data
        submission_defaults = {
            'author': request.POST.get('author', ''),
            'colgName': request.POST.get('colgName', ''),
            'degree': request.POST.get('degree', ''),
            'mobileNo': request.POST.get('mobileNo', ''),
            'co1': request.POST.get('co1', ''),
            'mail1': request.POST.get('mail1', ''),
            'co2': request.POST.get('co2', ''),
            'mail2': request.POST.get('mail2', ''),
            'co3': request.POST.get('co3', ''),
            'mail3': request.POST.get('mail3', ''),
            'field': request.POST.get('field', ''),
            'title': request.POST.get('title', ''),
            'others': request.POST.get('others', ''),
            'abstract': request.FILES.get('abstract'),
            'authentication': request.FILES.get('authentication'),
            'referral': request.POST.get('referral', 'NA'),
        }

        # Use update_or_create:
        # This one command finds a submission with the user's email.
        # If it finds one, it UPDATES it with the new data.
        # If it doesn't find one, it CREATES a new one.
        # This is much safer and faster than your original code.
        Submission.objects.update_or_create(
            email=email,
            defaults=submission_defaults
        )

    return redirect('home')

def iitb_view(request):
    if request.method == "POST":
        ldap = request.POST.get('ldap', '')

        # Use get_or_create to safely handle new registrations
        # This avoids errors and duplicate entries
        obj, created = iitb.objects.get_or_create(
            ldap=ldap,
            defaults={
                'name': request.POST.get('name', ''),
                'contact': request.POST.get('contact', ''),
                'roll': request.POST.get('roll_no', ''),
                'department': request.POST.get('department', '')
            }
        )

        if not created:
            # If 'created' is False, the LDAP already existed.
            # Render the page again with an error message.
            return render(request, 'academic.html', {
                'error': 'This LDAP ID is already registered.'
            })
        
        # If we are here, the user was created successfully
        return render(request, 'academic.html', {'filled_acad': True})

    # If not POST, just render the page
    return render(request, 'academic.html')

def noniitb_view(request):
    if request.method == "POST":
        email = request.POST.get('email', '')

        # Use get_or_create to safely handle new registrations
        obj, created = non_iitb.objects.get_or_create(
            email=email,
            defaults={
                'name': request.POST.get('name', ''),
                'contact': request.POST.get('contact', ''),
                'college': request.POST.get('college', ''),
                'transaction_id': request.POST.get('transaction_id', ''),
                'payment_screenshot': request.FILES.get('payment_screenshot')
            }
        )

        if not created:
            # If 'created' is False, the email already existed.
            return render(request, 'academic.html', {
                'error': 'This email is already registered.'
            })

        # If we are here, the user was created successfully
        return render(request, 'academic.html', {'filled_acad': True})

    # If not POST, just render the page
    return render(request, 'academic.html')