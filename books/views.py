# For decoding the token
import jwt
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework import authentication, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .books_api import book_search, get_book_info
from .serializers import *
from rest_framework import status
from django.contrib.auth import authenticate
from .tokens import verify_access_token, create_token_pair
from rest_framework_simplejwt.exceptions import TokenError

# For social login
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from social_core.exceptions import MissingBackend
from social_core.backends.google import GoogleOAuth2
from urllib.parse import urlencode
import random
import string
import requests
from rest_framework.permissions import AllowAny
import logging

# Redis imports
from django.core.cache import cache
from datetime import timedelta


# class Books(APIView):
    # def get(self, request,book_id):
    #     id = request.GET.get('book_id')
    #     get_book_info(id)
    #     # info = get_book_info(id)
    #     # return Response(info)
    
    # def search(self, request):
    #     query = request.GET.get('q')
    #     book_obj = book_search(query)
    #     return Response(book_obj)
    

# class RegisterAPI(APIView):

#     def post(self, request):
#         data = request.data
#         serializer = RegisterSerializer(data = data)
#         if not serializer.is_valid():
#             return Response({
#                 'status' : False,
#                 'message' : serializers.errors
#             }, status = status.HTTP_400_BAD_REQUEST)

#         serializer.save()
#         return Response({'status': True, 'message' :'user created'}, status.HTTP_200_OK)
    

# class LoginAPI(APIView):
#     def post(self, request):
#         data = request.data
#         serializer = LoginSerializer(data = data)
#         if not serializer.is_valid():
#             return Response({'status': False, 'message': serializer.errors},status = status.HTTP_400_BAD_REQUEST)
        
#         else:
    
#             # this code is for loggedin the user if username is used.
#             if serializer['username'] != None:
#                 user = authenticate(username = serializer['username'], password = serializer['password'])
            
#             # this code is for loggedin the user if email is used.
#             elif serializer['email'] != None:
#                 user = authenticate(email = serializer['email'], password = serializer['password'])
            
#             if not user:
#                 return Response({
#                     'status': False, 'message': 'Wrong password.'
#                 }, status = status.HTTP_404_NOT_FOUND)

#         return Response({'status': True, 'message':'User loggedin'}, status = status.HTTP_201_CREATED)


class RegisterAPIView(APIView):

    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = RegisterSerialzier(data = data)

        if not serializer.is_valid():
            return Response({
                'status': False, 'message':serializer.errors
            }, status = status.HTTP_400_BAD_REQUEST)
        
        
        serializer.save()
        # Sending mail from view. (Because it is a side effect,not directly related to data storage or transformation.)
        user = serializer.save()
        # Creating account activation token
        activation_token = create_custom_access_token(user,token_type = 'activation')

        send_activation_mail(user,activation_token)
        
        return Response({'status':True, 'message':'User created successfully!'}, status = status.HTTP_201_CREATED)

# class LoginAPI(APIView):

    # def post(self,request):
    #     data = request.data

    #     serializer = LoginSerializer(data = data)
    #     if not serializers.is_valid():
    #         return Response({'status':False, 'message':serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
        
    #     # username_or_email = serializer.validated_data.get('username') or serializer.validated_data.get('email')

    #     # Authenicate the user based on the retrieved username or email.
    #     # user = authenticate(username = username_or_email, password = serializer.validated_data.get('password'))
        
    #     # if serializer.validated_data.get('username'):
    #     #     user = authenticate(username = serializer.validated_data.get('username'), password = serializer.validated_data.get('password'))

    #     # elif serializer.validated_data.get('email'):
    #     #     username = User.objects.filter(email = serializer.validated_data.get('email'))
    #     #     user = authenticate(username = username, password = serializer.validated_data.get('password'))

    #     username = serializer.validated_data.get('username')
    #     if serializer.validated_data.get('email'):
    #         username = User.objects.filter(email = serializer.validated_data.get('email'))
    #         if username != None:
    #             username = username[0]['username']
    #         # or
    #         # username = User.objects.filter(email = serializer.validated_data.get('email')).get('username')
            
    #     user = authenticate(username = username, password = serializer.validated_data.get('password'))

    #     if user is None:
    #          return Response({
    #              'status': False,
    #              'message': 'Invalid credentials, please check your email/username and password.'},
    #              status = status.HTTP_401_UNAUTHORIZED)

    #     # Successful login
    #     return Response({
    #         'status': True,
    #         'message': 'User logged in successfully.'
    #     },
    #     status = status.HTTP_200_OK)

#######################
        # user = None
        # if data.get('username'):
        #     user = authenticate(username = data['username', password = data['password']])
        
        # elif data.get('email'):
        #     user = authenticate(email = data['email'], password = data['password'])

        # if not user:
        #     return Response('Wrong credentials!')
        # return user

class ActivateAccountView(APIView):
    # Why permission is needed in ActivateAccountView
    permission_classes = [AllowAny]
    def get(self, request, token):
        # access_token = AccessToken(token)
        # user = access_token.user
        # if verify_access_token(token):
        #     if user.is_active == False:
        #         user.is_active = True
        #     else:
        #         # Account is already activated so link doesn't work! -> Find the suitable status code for the same.
        #         return Response({"status": False, "message":"Account is already activated"},status = status.HTTP_400_BAD_REQUEST)
        # return Response({"status":True, "message":"Account activated successfully."},status = status.HTTP_200_OK)
        ######################

        # access_token = verify_access_token(token)
        # if access_token:

        #     user = access_token.user
        #     if user.is_active == False:
        #         user.is_active = True
        #         return Response({"status":True, "message": "Account activated successfully"},status = status.HTTP_200_OK)
        #     return Response({"status":False,"message": "Account already activated."},status = status.HTTP_400_BAD_REQUEST)

        #########################
        try:
            # Verify if the token is valid (or raise an error if invalid )
            access_token = verify_access_token(token)

            # Retrieve the user from the token
            # user_id = access_token.user_id
            user_id = access_token['user_id']
            user = User.objects.get(id = user_id)

            if user.is_active:
                return Response({
                    "status": False, "message": "Account is already activated."
                }, status = status.HTTP_400_BAD_REQUEST)
            
            user.is_active = True
            user.save()
            return Response({
                "status": True, "message": "Account activated successfully."
            }, status = status.HTTP_200_OK)

        except TokenError as e:
            return Response({
                "status": False, 
                "message": str(e)
            },
            status = status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return Response({
                "status": False, "message":"Activation failed: User not found."
            }, status = status.HTTP_400_BAD_REQUEST)
        
class LoginAPIView(APIView):

    permission_classes = [AllowAny]
    
    def post(self, request):
        # Check if the user already has a valid token(i.e. they are logged in)
        jwt_authenticator = JWTAuthentication()

        try:
            #  If this succeeds, the user is already authenticated via a valid JWT
            user, _ = jwt_authenticator.authenticate(request)
            print("user is ", user , " _ is ", _)
            # if user:
            return Response({
                'status':False, 
                'message': 'You are already logged in. Logout to login again.'
            },status = status.HTTP_403_FORBIDDEN)

        except Exception:
            print("i am inside excepiton")
            print("if unauthorized login, then do login and create a new token.")
            data = request.data
            serializer = LoginSerializer(data = data)
            if not serializer.is_valid():
                return Response({
                    'status':False, 'message': serializer.errors
                },status = status.HTTP_400_BAD_REQUEST)
            
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            if email:
                user = User.objects.get(email = email)
                # user = User.objects.filter(email = email)
                # if not user.exists():
                #     username = None
                username = user.username
            
            user = authenticate(username = username, password = password)

            if user is None:
                return Response({
                    'status': False, 'message': 'Wrong Password'
                }, status = status.HTTP_401_UNAUTHORIZED)
            
            tokens = create_token_pair(user = user)
            # Successful login
            return Response({
                'status': True,
                'message': 'User logged in successfully.','token':tokens
            },
            status = status.HTTP_200_OK)
        

class LogoutAPIView(APIView):
    def get(self, request):
        # authorization_header = request.headers.get('Authorization')
       
        # Basically to check whether the user is authenticated or not
        jwt_authenticator = JWTAuthentication()

        # Try - catch statement is redundant since everyting is handled by jwtauthentication class and blacklist token middleware.
        # try:
        user, validated_token = jwt_authenticator.authenticate(request)
        if user:
            
            token = request.headers.get("Authorization").split(" ")[1]
            expiration_time = validated_token['exp'] - validated_token['iat']
            print("expiration_time is ", expiration_time)
        
            # Use Djanog cache (backend by Redis) to blacklist the token
            cache.set(f"blacklisted_{token}", "blacklisted", timeout= expiration_time)
            # if user is valid (i.e. it is logged in), then blacklist the token to logout
            
            # return to the login page or for a while return login again to get access of resources
            return Response({
                'status': True,
                'message':'Logout successful, token blacklisted.'
            })
       
        # except Exception:
        #     # for a while(for demo)
        #     return Response({
        #         'status':False, 'message': 'Logout api view is not accessible for unauthneticated user.'
        #     })



class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
# class ResetPasswordView(APIView):
    def post(self, request):
        # Getting email from data.
        data = request.data
        serializer = PasswordResetRequestSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status':False, 'message': serializer.errors
            }, status = status.HTTP_400_BAD_REQUEST)
        
        # user = User.objects.filter(email = data)
        # user.set_password()
        # reset_password_token = create_custom_access_token(user, token_type='password_reset')
        # send_reset_password_mail(user, reset_password_token)
        # Sending reset email from view(Coz it is a side effect and more appropriate here.)
        # serializer.save()
        user = serializer.save()
        reset_password_token = create_custom_access_token(user, token_type='password_reset')
        send_reset_password_mail(user, reset_password_token)
        # Token blacklisted part is yet to add.
        return Response({
            'status':True,'message':'Reset mail send successfully!'
        }
        , status = status.HTTP_200_OK)

    # def get(self,request,token):
    #     try:
    #         # Verify if the token is valid(or raise an error if invalid or expired.)
    #         access_token = verify_access_token(token)

    #         # Retrieve the user from the token
    #         email = access_token['email']
    #         user = User.objects.get(email = email)
    #         user.set_password()

    #         if us


# Endpoint to validate the token and responding appropriate response or error messages.
class PasswordResetTokenValidationView(APIView):
# class ResetTokenView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, token):
        try:
            access_token = verify_access_token(token)
            token_str = str(access_token)
            return Response({
                # "status":True, "message":"Token is validated, you can use it for further task. ",'access_token':access_token
                # "status":True, "message":"Token is validated, you can use it for further task. ","validate_token":access_token
                "status":True, "message":"Token is validated, you can use it for further task. ","token":token_str
            },
            status = status.HTTP_200_OK)
            # redirect_url = reverse('password_reset_Confirm', args= [ access_token])
            # return redirect('password_reset_confirm')
        
        except TokenError as e:
            return Response({
                "status":False,
                "message":str(e)
            },
            status = status.HTTP_400_BAD_REQUEST)
        
    # Bad practice of trying to perform token validation and password update in one view.

    # def post(self, request):
    #     data = request.data
    #     # serialzier = 

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    # def get(self, request, token):
    #         access_token = verify_access_token(token)

    #         # Retrieve the user from the token
    #         # user_id = access_token.user_id
    #         user_id = access_token['user_id']
    #         user = User.objects.get(id = user_id)

    def post(self, request, token):
        secret_key = settings.JWT_SECRET_KEY
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])

        user_id = decoded_token['user_id']
        user = User.objects.get(id = user_id)
        print("user_id is ", user_id)
        print("user is ", user)
        print("token is ", decoded_token)
        data = request.data
        print("data is ", data)
        # combined_data = {"user":user, "data":data} 
        serializer = PasswordResetConfirmSerializer(data = data, user = user,)
        # serializer = PasswordResetConfirmSerializer(combined_data)
        # serializer = PasswordResetConfirmSerializer(data = data, user = user)
        if not serializer.is_valid():
            return Response({
                "status":False, "message":serializer.errors
            },status = status.HTTP_400_BAD_REQUEST)
        serializer.save()
        # Sending the password reset update mail
        send_password_update_mail(user)
        
        expiration_time = decoded_token['exp'] - decoded_token['iat']
        print("expiration time is ", expiration_time)
        # expiration_time = validated_token['exp'] - validated_token['iat']
        cache.set(f"blacklisted_{token}", "blacklisted", timeout= expiration_time)
        return Response({"status":True, "message":"Password updated successfully"}, status = status.HTTP_200_OK)
            
        
######## Google login flow 

# @api_view(['GET']
# def google_login(request):

class GoogleLogin(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        # Base url where we will get user consent to use their data
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        
        # Generate a secure random state string
        state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        request.session['oauth_state'] = state  # Store in session for validation later
        scope = ' '.join(settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE)
        params = {
            "response_type": "code",
            "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "redirect_uri": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI,
            "scope": scope,
            # "state": state  
        }
        
        google_auth_url = f"{base_url}?{urlencode(params)}&state={state}"
        # print(google_auth_url,"printing")
        # print("state that we are sending",state)
        # print("Session at login:", request.session.items())
        return redirect(google_auth_url)

# Configure logging
# logging.basicConfig(level= logging.INFO)

class GoogleCallback(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        # Retrieve the authorization code 
        code = request.GET.get('code')
        state = request.GET.get('state')
        # print("stored state is ", state)
        session_state = request.session.get('oauth_state')
        # print("state that we are receiving", session_state)
        # print("code is ", code)
        # print("state is ", state)
        # print("session_state",session_state)

        # Log the received state and session state
        # logging.info(f"Received state: {state}")
        # logging.info(f"Session state: {session_state}")
        # print("Session at callback:", request.session.items())
        # Validate state to prevent CSRF
        if not code or state != session_state:
            return Response({'error':'Invalid authorization code or state'}, status = 400)
        
        # del request.session['oauth_state']

        # Prepare data to exchange the code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            "redirect_uri": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI ,
            "grant_type":"authorization_code"
        }

        try:
            # Exchange the authorization code for access and Id tokens
            response = requests.post(token_url, data = data)
            response_data = response.json()
            print("Response data from Google:", response_data)

            if response.status_code !=200:
                return Response({'error': response_data.get('error_description', 'Error exchanging code for tokens')}, status = 400)

            # Extract tokens
            access_token = response_data.get('access_token')
            id_token = response_data.get('id_token')

            return Response({'access_token': access_token, 'id_token':id_token})
        
        except Exception as e:
            return Response({'error':str(e)}, status = 500)


# @api_view(['GET'])
# def google_callback(request):

class BookInfoAPIView(APIView):
    def get(self, request, book_id):
        data, status_code = get_book_info(book_id)
        return Response(data, status = status_code)
    
class BookSearchAPIView(APIView):
    def get(self, request):
        search_key = request.GET.get('q','')
        data, status_code = book_search(search_key)
        return Response(data, status = status_code)

class Recommendation(APIView):
    pass