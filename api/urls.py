from django.urls import path
from books.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('api/books_info/<str:book_id>/', BookInfoAPIView.as_view(), name = 'book-info'),
    path('api/books_search/', BookSearchAPIView.as_view(), name = 'book-search'),
    path('register/',RegisterAPIView.as_view(), name = 'user-register'),
    path('login/',LoginAPIView.as_view(),name = 'user-login'),
    path('logout/',LogoutAPIView.as_view(), name = 'user-logout'),
    path('register/activate/<str:token>/' , ActivateAccountView.as_view(), name = 'activate_account' ),
    path('api/password-reset/',PasswordResetRequestView.as_view(), name = 'password_reset'),
    # path('api/password-reset/validate-token/',PasswordResetTokenValidationView.as_view(), name = 'password_reset_validate_token'),
    path('api/password-reset/validate-token/<str:token>/',PasswordResetTokenValidationView.as_view(), name = 'password_reset_validate_token'),
    # path('api/password-reset/confirm/',PasswordResetConfirmView().as_view(), name = 'passform_reset_confirm'),
    path('api/password-reset/confirm/<str:token>/',PasswordResetConfirmView().as_view(), name = 'password_reset_confirm'),
    path('api/token/', TokenObtainPairView.as_view(), name= 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(),name = 'token_verify'),
    
    # Google login flow urls
    path('auth/google/', GoogleLogin.as_view(),name = 'google_login'),
    path('auth/complete/google-oauth2/',GoogleCallback.as_view(), name = 'google_callback')
]