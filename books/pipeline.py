import logging

def debug_user_creation(backend, uid, user = None, response = None, *args,**kwargs):
    logger = logging.getLogger('social_auth')
    if user is None:
        print("user",user)
        logger.debug(f"Attempting to create a new user with UID: {uid}")
    else:
        print("username:",user.username)
        logger.debug(f"User already exists: {user.username}")
    