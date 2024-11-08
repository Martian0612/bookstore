from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from datetime import timedelta

def create_custom_access_token(user, token_type = 'general'):
    access_token = AccessToken.for_user(user)

    # Customize expiry time based on token type
    if token_type == 'activation':
        access_token.set_exp(lifetime = timedelta(minutes = 5))

    elif token_type == 'password_reset':
        access_token.set_exp(lifetime = timedelta(hours = 1))

    else:
        access_token.set_exp(lifetime = timedelta(days = 1))
    
    return str(access_token)

def create_token_pair(user):
    refresh = RefreshToken.for_user(user)

    tokens = {
        'refresh': str(refresh),
        'access' : str(refresh.access_token)
    }

    return tokens

def verify_access_token(token):
    try:
        # Creating a token object using existing token to validate whether it expires or not or other sort of validation.
        access_token = AccessToken(token)
        return access_token
    except TokenError as e:
        raise TokenError(f"Token error: {str(e)}")
    
def verify_token_pair(token):
    try:
        refresh_token = RefreshToken(token)
        # Validate if token is valid and has not expired (basically someone rob your credentials, so we are blacklisting them or blocking that access.)
        if refresh_token.check_blacklist():
            raise TokenError("Token has been blacklisted.")
        return refresh_token
    except TokenError as e:
        raise TokenError(f"Token error: {str(e)}")
    

# Incomplete code

# def blacklist_token(token):
#     try:
#         refresh_token = RefreshToken(token)
#         refresh_token.blacklist()
#     except Exception as e:
#         raise TokenError(f"Token could not be blacklisted: {str(e)}")