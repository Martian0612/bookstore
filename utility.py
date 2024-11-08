from django.urls import reverse
from urllib.parse import quote
from django.core.mail import send_mail
from django.conf import settings

def send_activation_mail(user, token):
    print("Inside the mail function.")
    # activation_url = reverse('activate_account',kwargs= {'token':token})
    activation_url = reverse('activate_account',args= [token])
    full_url = f"http://127.0.0.1:8000{quote(activation_url)}"

    subject = 'Activate your BookBuddy Hub account'
    message = f"Hi {user.username}, \n\nThank you for registering at BookBuddyHub ! Please click the link below to activate your account:\n{full_url}\n\nThank you!"
    # Send the email
    # send_mail(
    #     'Activate your account',
    #     f'Click the following link to activate your account: {full_url}',
    #     'testing7403@gmail.com',
    #     [user.email],
    # )

    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently = False
    )
    
def send_reset_password_mail(user,token):
    print("inside the reset passowrd mail.")
    reset_url = reverse('password_reset_validate_token',args= [token])
    # reset_url = reverse('reset_password',args= [token])
    full_url = f"http://127.0.0.1:8000{quote(reset_url)}"

    subject = 'Reset your BookBuddy Hub account password'
    message = f"Dear {user.username},\n We have received your request for reset password.\n To reset, please click the link below: \n\n{full_url}\n\n This link is valid for two hours from your request initiation for password recovery.\n\n Note: This is a system generated e-mail, please do not reply to it."
    send_mail(subject,
              message,
              settings.DEFAULT_FROM_EMAIL,
              [user.email],
              fail_silently = False)

def send_password_update_mail(user):
    print("Inside password confirm mail.")
    subject = 'Password update info.'
    message = f"Dear {user.username}, \n Your password is updated successfully.\n\n If it is not done by you, then please write us back at BookBuddyHub@gmail.com."
    send_mail(subject, 
              message,
              settings.DEFAULT_FROM_EMAIL,
              [user.email],
              fail_silently = False)
                



