import os
import boto3
import json
import datetime as dt
from botocore.exceptions import ClientError

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# import data tables from database
from .models import Submission , Seismic ,BridgeIt ,ConquerIt

# Create your views here.

def registerLogiq(request):
    return render(request, "submission.html")

def msewall_view(request):
    return render(request, "msewall.html")

def idp(request):
    return render(request, "idp.html")

def index(request):
    user = request.user
    is_filled = False
    is_filled_seismic = False
    is_filled_bridgeit = False
    is_filled_conquerit = False

    if user.is_authenticated:
        email = user.email
        is_filled = Submission.objects.filter(email=email).exists()
        is_filled_seismic = Seismic.objects.filter(email=email).exists()
        is_filled_bridgeit = BridgeIt.objects.filter(email=email).exists()
        is_filled_conquerit = ConquerIt.objects.filter(email=email).exists()

    return render(request, "compi_page.html", {
        'is_filled': is_filled,
        'is_filled_seismic': is_filled_seismic,
        'is_filled_bridgeit': is_filled_bridgeit,
        'is_filled_conquerit': is_filled_conquerit
    })

def logiq(request):
    is_filled = False
    if request.user.is_authenticated:
        is_filled = Submission.objects.filter(email=request.user.email).exists()
    
    return render(request, "logiq.html", { 'is_filled': is_filled })

@login_required
def submitted(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        user = request.user
        mail = user.email

        colgName = request.POST.get('colgName', '')
        branch = request.POST.get('branch', '')
        mobileNo = request.POST.get('mobileNo', '')
        emails = request.POST.get('emails', '')
        program = request.POST.get('program', '')
        year = request.POST.get('year', '')
        address = request.POST.get('address', '')
        roll_no = request.POST.get('roll_no', '')
        ref = request.POST.get('ref', '')
        
        # Avoid re-submission if already registered
        if not Submission.objects.filter(email=mail).exists():
            response = Submission(
                name=name, email=mail, colgName=colgName, branch=branch, 
                mobileNo=mobileNo, year=year, roll_no=roll_no, 
                address=address, program=program, ref=ref, emails=emails
            )
            response.save()

    return redirect('index')

def seismic(request):
    is_filled_seismic = False
    if request.user.is_authenticated:
        is_filled_seismic = Seismic.objects.filter(email=request.user.email).exists()

    return render(request, "seismic.html", { 'is_filled_seismic': is_filled_seismic })

@login_required
def seismic_reg(request):
    if request.method == "POST":
        email = request.user.email
        
        # Avoid re-submission
        if not Seismic.objects.filter(email=email).exists():
            name1 = request.POST.get('name1', '')
            colg1 = request.POST.get('colg1', '')
            email1 = request.POST.get('email1', '')
            contact1 = request.POST.get('contact1', '')
            category = request.POST.get('category', '')
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
            
            response = Seismic(
                team=team, email=email, 
                name1=name1, email1=email1, colg1=colg1, contact1=contact1, 
                name2=name2, email2=email2, colg2=colg2, contact2=contact2,
                name3=name3, email3=email3, colg3=colg3, contact3=contact3, 
                name4=name4, email4=email4, colg4=colg4, contact4=contact4, 
                category=category, ref=ref
            )
            response.save()

    return redirect('seismic')

def bridgeit(request):
    is_filled_bridgeit = False
    if request.user.is_authenticated:
        is_filled_bridgeit = BridgeIt.objects.filter(email=request.user.email).exists()

    return render(request, "bridgeit.html", { 'is_filled_bridgeit': is_filled_bridgeit })

@login_required
def bridgeit_reg(request):
    if request.method == "POST":
        email = request.user.email
        
        # Avoid re-submission
        if not BridgeIt.objects.filter(email=email).exists():
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
            
            response = BridgeIt(
                team=team, email=email, 
                name1=name1, email1=email1, colg1=colg1, contact1=contact1, 
                name2=name2, email2=email2, colg2=colg2, contact2=contact2,
                name3=name3, email3=email3, colg3=colg3, contact3=contact3, 
                name4=name4, email4=email4, colg4=colg4, contact4=contact4,  
                ref=ref
            )
            response.save()
        
        # --- Commented-out email logic ---
        # I have NOT enabled this, but I have made it secure by
        # replacing the hard-coded keys with environment variables.
        
        # AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
        # AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
        # AWS_REGION = "us-east-1"
        
        # if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        #     print("Email not sent: AWS credentials are not configured in environment.")
        # else:
        #     SENDER = "Competitions | Aakaar IIT Bombay <competition@aakaariitbombay.org>"
        #     RECIPIENT = email
        #     SUBJECT = "BridgeIT Competition | Aakaar IIT Bombay"
        #     BODY_HTML = """ ... YOUR HTML ... """
        #     CHARSET = "UTF-8"
        #     client = boto3.client(
        #         'ses', 
        #         region_name=AWS_REGION,
        #         aws_access_key_id=AWS_ACCESS_KEY_ID,
        #         aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        #     )
        #     try:
        #         response = client.send_email(...) # Your email sending logic
        #     except ClientError as e:
        #         print(f"Email Error: {e.response['Error']['Message']}")
        #     else:
        #         print(f"Email sent! Message ID: {response['MessageId']}")

    return redirect('bridgeit')

def conquerit(request):
    is_filled_conquerit = False
    if request.user.is_authenticated:
        is_filled_conquerit = ConquerIt.objects.filter(email=request.user.email).exists()

    return render(request, "conquerit.html", { 'is_filled_conquerit': is_filled_conquerit })

@login_required
def conquerit_reg(request):
    if request.method == "POST":
        email = request.user.email
        name1 = "" # Initialize name1

        # Avoid re-submission
        if not ConquerIt.objects.filter(email=email).exists():
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
            
            response = ConquerIt(
                team=team, email=email, 
                name1=name1, email1=email1, colg1=colg1, contact1=contact1, 
                name2=name2, email2=email2, colg2=colg2, contact2=contact2,
                name3=name3, email3=email3, colg3=colg3, contact3=contact3, 
                name4=name4, email4=email4, colg4=colg4, contact4=contact4,  
                ref=ref
            )
            response.save()
            
            # Send confirmation email AFTER successful save
            _send_conquerit_confirmation(email, name1)

    return redirect('conquerit')

# --- Helper Function for Sending Email ---
def _send_conquerit_confirmation(recipient_email, name):
    """
    Sends a confirmation email for ConquerIT registration.
    """
    # --- THIS IS THE SECURE WAY ---
    # Load credentials from environment variables
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = "us-east-1"
    
    # Stop if keys are not set
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        print("EMAIL NOT SENT: AWS keys are not configured in the environment.")
        return

    SENDER = "Competitions | Aakaar IIT Bombay <competition@aakaariitbombay.org>"
    RECIPIENT = recipient_email
    SUBJECT = "Successful Registration for ConquerIT !"
    
    BODY_HTML = (f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Registration Confirmation</title>
</head>
<body>
    <div class="text">
        <p>Hello {name},</p>
        <p>We are pleased to inform you that your registration for ConquerIT has been successful.</p>
        <p>Thank you for being so interested in this exciting event. </p>
        <br>
        <p>If you have any questions or concerns, please don't hesitate to reach out to us through the mail: <a href="mailto:competition@aakaariitbombay.org">competition@aakaariitbombay.org</a>  </p>
        <p>We look forward to seeing you at ConquerIT and hope that you will find the event to be informative and enjoyable.</p>
        <br>
        <p>Best regards,  <br>
            [Competition Manager <br>
            Aakaar 2023,  <br>
            IIT Bombay]
        </p>
    </div>
</body>
</html>
""") # Used an f-string to insert the name
    
    CHARSET = "UTF-8"
    
    client = boto3.client(
        'ses', 
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    
    try:
        response = client.send_email(
            Destination={ 'ToAddresses': [RECIPIENT] },
            Message={
                'Body': {
                    'Html': { 'Charset': CHARSET, 'Data': BODY_HTML, },
                },
                'Subject': { 'Charset': CHARSET, 'Data': SUBJECT, },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(f"EMAIL ERROR: {e.response['Error']['Message']}")
    else:
        print(f"Email sent to {RECIPIENT}! Message ID: {response['MessageId']}")