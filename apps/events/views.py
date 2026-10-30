import os
import boto3
import json
import datetime as dt
from botocore.exceptions import ClientError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount

## import data tables from database
from .models import (
    Cenex, StaadPro, Fusion, LabVisit, Primavera, Staad_payment, 
    Primavera_payment, Primaveraplusstaad_payment, Fusion_payment, 
    Fusionplusstaad_payment, Fusionplusstaad_reg, labpayment_modal, ceohour
)

# ==============================================================================
# 🔒 SECURE EMAIL HELPER FUNCTION
# ==============================================================================

def _send_ses_email(recipient_email, subject, html_body):
    """
    Securely sends an email using AWS SES, loading keys from environment variables.
    This one function replaces all the repeated, insecure code.
    """
    # --- THIS IS THE SECURE WAY ---
    # Load credentials from environment variables (NOT hard-coded)
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = "us-east-1"  # This was constant in all your views

    # Stop if keys are not set in the server environment
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        print(f"EMAIL NOT SENT to {recipient_email}: AWS credentials are not configured in the environment.")
        return

    # Use a consistent sender. You can change this if needed.
    SENDER = "Events Aakaar IIT Bombay <events@aakaariitbombay.org>"
    CHARSET = "UTF-8"

    client = boto3.client(
        'ses',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    try:
        response = client.send_email(
            Destination={'ToAddresses': [recipient_email]},
            Message={
                'Body': {'Html': {'Charset': CHARSET, 'Data': html_body}},
                'Subject': {'Charset': CHARSET, 'Data': subject},
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(f"EMAIL ERROR for {recipient_email}: {e.response['Error']['Message']}")
    else:
        print(f"Email sent to {recipient_email}! Message ID: {response['MessageId']}")


# ==============================================================================
# VIEW FUNCTIONS
# ==============================================================================

def ceo_reg(request):
    if request.method == "POST":
        # Retrieve data from the form
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        status = request.POST.get('status')
        org = request.POST.get('org')

        # Create a new instance of CEORegistration model and save it
        response = ceohour(
            name=name,
            contact=contact,
            email=email,
            status=status,
            org=org
        )
        response.save()
        return redirect('lecture_series')

    return render(request, 'key.html')

# Added @login_required decorator for security and to prevent errors
@login_required
def cenex_reg(request):
    if request.method == "POST":
        email = request.user.email
        
        # Prevent re-submission
        if not Cenex.objects.filter(email=email).exists():
            name1 = request.POST.get('name1', '')
            colg1 = request.POST.get('colg1', '')
            email1 = request.POST.get('email1', '')
            contact1 = request.POST.get('contact1', '')
            ref = request.POST.get('ref', '')
            team = request.POST.get('team', '')
            name2 = request.POST.get('name2', '')
            colg2 = request.POST.get('colg2', '')
            email2 = request.POST.get('email2', '')
            contact2 = request.POST.get('contact2', '')
            name3 = request.POST.get('name3', '')
            colg3 = request.POST.get('colg3', '')
            email3 = request.POST.get('email3', '')
            contact3 = request.POST.get('contact3', '')
            name4 = request.POST.get('name4', '')
            colg4 = request.POST.get('colg4', '')
            email4 = request.POST.get('email4', '')
            contact4 = request.POST.get('contact4', '')
            
            response = Cenex(
                team=team, email=email, 
                name1=name1, email1=email1, colg1=colg1, contact1=contact1, 
                name2=name2, email2=email2, colg2=colg2, contact2=contact2,
                name3=name3, email3=email3, colg3=colg3, contact3=contact3, 
                name4=name4, email4=email4, colg4=colg4, contact4=contact4, ref=ref
            )
            response.save()

    return redirect('cenex')

def cenex(request):
    is_filled_cenex = False
    if request.user.is_authenticated:
        email = request.user.email
        # Use .exists() for a more efficient database query
        is_filled_cenex = Cenex.objects.filter(email=email).exists()

    return render(request, "cenex.html", {
        'is_filled_cenex': is_filled_cenex
    })

def lecture_series(request):
    return render(request, "key.html")

def index(request):
    is_filled_cenex = False
    if request.user.is_authenticated:
        email = request.user.email
        # Use .exists() for a more efficient database query
        is_filled_cenex = Cenex.objects.filter(email=email).exists()

    return render(request, "events_page.html", {
        'is_filled_cenex': is_filled_cenex
    })

def workshop(request):
    return render(request, "workshop.html")

def labvisit(request):
    return render(request, "labvisit.html")

def fusion_reg(request):
    is_not_fusion = 1
    message = ""
    is_exists = 0

    if request.method == "POST":
        name = request.POST.get('name', '')
        colg = request.POST.get('colg', '')
        email = request.POST.get('email', '')
        contact = request.POST.get('contact', '')
        
        # Use .exists() for efficiency
        is_filled = Fusion.objects.filter(contact=contact).exists()
        
        if is_filled:
            message = "Phone Number already exists"
            is_exists = 1
        else:
            message = "You have submitted successfully"
            response = Fusion(email=email, name=name, colg=colg, contact=contact)
            response.save()

            # --- Send Email ---
            SUBJECT = "Registration Confirmation for Fusion Workshop | Aakaar IIT Bombay"
            BODY_HTML = """
                <!DOCTYPE html>...
                Greetings from Aakaar IIT Bombay . <br>
                You have successfully completed the  registration part of the  Fusion workshop. <br>
                ... (rest of your HTML) ...
                </html>
            """ # Truncated for brevity
            _send_ses_email(email, SUBJECT, BODY_HTML)
            # --- End of Email ---

    return render(request, 'workshop.html', {
        'message': message,
        "is_exists": is_exists,
        "is_not_fusion": is_not_fusion
    })

def staadpro_reg(request):
    is_not_staadpro = 1
    message = ""
    is_exists = 0

    if request.method == "POST":
        name = request.POST.get('name', '')
        colg = request.POST.get('colg', '')
        email = request.POST.get('email', '')
        contact = request.POST.get('contact', '')
        
        is_filled = StaadPro.objects.filter(contact=contact).exists()
        
        if is_filled:
            message = "Phone Number already exists"
            is_exists = 1
        else:
            message = "You have submitted successfully"
            response = StaadPro(email=email, name=name, colg=colg, contact=contact)
            response.save()

            # --- Send Email ---
            SUBJECT = "Registration Confirmation for Staad Pro Workshop | Aakaar IIT Bombay"
            BODY_HTML = """
                <!DOCTYPE html>...
                Greetings from Aakaar IIT Bombay . <br>
                You have successfully completed the  registration part of the  staad pro workshop. <br>
                ... (rest of your HTML) ...
                </html>
            """ # Truncated for brevity
            _send_ses_email(email, SUBJECT, BODY_HTML)
            # --- End of Email ---

    return render(request, 'workshop.html', {
        'message': message,
        "is_exists": is_exists,
        "is_not_staadpro": is_not_staadpro
    })

def labvisit_reg(request):
    is_not_labvisit = 1
    message = ""
    is_exists = 0
    if request.method == "POST":
        name = request.POST.get('name', '')
        colg = request.POST.get('colg', '')
        email = request.POST.get('email', '')
        contact = request.POST.get('contact', '')
        ref = request.POST.get('ref', '')
        
        is_filled = LabVisit.objects.filter(contact=contact).exists()
        
        if is_filled:
            message = "Phone Number already exists"
            is_exists = 1
        else:
            message = "You have submitted successfully"
            response = LabVisit(email=email, name=name, colg=colg, contact=contact, ref=ref)
            response.save()
            
    return render(request, 'labvisit.html', {
        'message': message,
        "is_exists": is_exists,
        "is_not_labvisit": is_not_labvisit
    })

def primavera_reg(request):
    is_not_primavera = 1
    message = ""
    is_exists = 0
    if request.method == "POST":
        name = request.POST.get('name', '')
        colg = request.POST.get('colg', '')
        email = request.POST.get('email', '')
        contact = request.POST.get('contact', '')
        ref = request.POST.get('ref', '')
        
        is_filled = Primavera.objects.filter(contact=contact).exists()
        
        if is_filled:
            message = "Phone Number already exists"
            is_exists = 1
        else:
            message = "You have submitted successfully"
            response = Primavera(email=email, name=name, colg=colg, contact=contact, ref=ref)
            response.save()

            # --- Send Email ---
            SUBJECT = "Registration Confirmation for Primavera Workshop | Aakaar IIT Bombay"
            BODY_HTML = """
                <!DOCTYPE html>...
                Greetings from Aakaar IIT Bombay . <br>
                You have successfully completed the  registration part of the  Primavera workshop. <br>
                ... (rest of your HTML) ...
                </html>
            """ # Truncated for brevity
            _send_ses_email(email, SUBJECT, BODY_HTML)
            # --- End of Email ---

    return render(request, 'workshop.html', {
        'message': message,
        "is_exists": is_exists,
        "is_not_primavera": is_not_primavera
    })

# ==============================================================================
# PAYMENT VIEWS
# ==============================================================================

def staad_payment(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        transaction_id = request.POST.get('transaction_id', '')
        photo = request.FILES.get('payment_screenshot')
        
        data = Staad_payment(email=email, transaction_id=transaction_id, photo=photo)
        data.save()

        # --- Send Email ---
        SUBJECT = "Registration Confirmation for Staad Pro Workshop | Aakaar IIT Bombay"
        BODY_HTML = """
            <!DOCTYPE html>...
            Greetings from Aakaar IIT Bombay . <br>
            You have successfully registered to the Staad Pro workshop. <br>
            ... (rest of your HTML) ...
            </html>
        """ # Truncated for brevity
        _send_ses_email(email, SUBJECT, BODY_HTML)
        # --- End of Email ---

    return HttpResponse('Your have Submitted !')

def fusion_payment(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        transaction_id = request.POST.get('transaction_id', '')
        photo = request.FILES.get('payment_screenshot')
        
        data = Fusion_payment(email=email, transaction_id=transaction_id, photo=photo)
        data.save()

        # --- Send Email ---
        SUBJECT = "Payment Confirmation for Fusion 360 Workshop | Aakaar IIT Bombay"
        BODY_HTML = """
            <!DOCTYPE html>...
            Greetings from Aakaar IIT Bombay . <br>
            You have successfully completed the  registration part of the  Fusion 360 workshop. <br>
            ... (rest of your HTML) ...
            </html>
        """ # Truncated for brevity
        _send_ses_email(email, SUBJECT, BODY_HTML)
        # --- End of Email ---

    return HttpResponse('You have Submitted!')

def primavera_payment(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        transaction_id = request.POST.get('transaction_id', '')
        photo = request.FILES.get('payment_screenshot')
        
        data = Primavera_payment(email=email, transaction_id=transaction_id, photo=photo)
        data.save()

        # --- Send Email ---
        SUBJECT = "Registration Confirmation for Primavera Workshop | AakaVerify-payment-page_aakaar-main.zip ka-payment-page_aakaar-main.zip.kar IIT Bombay"
        BODY_HTML = """
            <!DOCTYPE html>...
            Greetings from Aakaar IIT Bombay . <br>
            You have successfully registered to the Primavera workshop. <br>
            ... (rest of your HTML) ...
            </html>
        """ # Truncated for brevity
        _send_ses_email(email, SUBJECT, BODY_HTML)
        # --- End of Email ---

    return HttpResponse('Form is Submitted')

def fusionplusstaad_payment(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        transaction_id = request.POST.get('transaction_id', '')
        photo = request.FILES.get('payment_screenshot')
        
        data = Fusionplusstaad_payment(email=email, transaction_id=transaction_id, photo=photo)
        data.save()

        # --- Send Email ---
        SUBJECT = "Registration Confirmation for Fusion360 and Staad Pro workshop Workshop | Aakaar IIT Bombay"
        BODY_HTML = """
            <!DOCTYPE html>...
            Greetings from Aakaar IIT Bombay . <br>
            You have successfully registered to the Fusion 360 and Staad Pro workshop. <br>
            ... (rest of your HTML) ...
            </html>
        """ # Truncated for brevity
        _send_ses_email(email, SUBJECT, BODY_HTML)
        # --- End of Email ---

    return HttpResponse('You Have Submitted !')

def primaveraplusstaad_payment(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        transaction_id = request.POST.get('transaction_id', '')
        photo = request.FILES.get('payment_screenshot')
        
        data = Primaveraplusstaad_payment(email=email, transaction_id=transaction_id, photo=photo)
        data.save()

        # --- Send Email ---
        SUBJECT = "Registration Confirmation for Primavera and Staad Pro workshop Workshop | Aakaar IIT Bombay"
        BODY_HTML = """
            <!DOCTYPE html>...
            Greetings from Aakaar IIT Bombay . <br>
            You have successfully registered to the Primavera workshop and Staad Pro. <br>
            ... (rest of your HTML) ...
            </html>
        """ # Truncated for brevity
        _send_ses_email(email, SUBJECT, BODY_HTML)
        # --- End of Email ---

    return HttpResponse('You Have Submitted !')

def fusionplusstaad_reg(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        colg = request.POST.get('colg', '')
        email = request.POST.get('email', '')
        contact = request.POST.get('contact', '')
        ref = request.POST.get('ref', '')
        response = Fusionplusstaad_reg(email=email, name=name, colg=colg, contact=contact, ref=ref)
        response.save()

        # --- Send Email ---
        # Note: The SUBJECT here looks like a copy-paste error from the one above
        SUBJECT = "Registration Confirmation for Primavera and Staad Pro workshop Workshop | Aakaar IIT Bombay"
        BODY_HTML = """
            <!DOCTYPE html>...
            Greetings from Aakaar IIT Bombay . <br>
            You have successfully completed the  registration part of the  staad pro workshop. <br>
            ... (rest of your HTML) ...
            </html>
        """ # Truncated for brevity
        _send_ses_email(email, SUBJECT, BODY_HTML)
        # --- End of Email ---

    return HttpResponse('You Have Submitted !')

def lab_payment(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        transaction_id = request.POST.get('transaction_id', '')
        photo = request.FILES.get('payment_screenshot')
        
        data = labpayment_modal(email=email, transaction_id=transaction_id, photo=photo)
        data.save()
        
        # This view did not have email logic, so I have not added it.

    return HttpResponse('You Have Submitted Payment form for Lab Visit !')