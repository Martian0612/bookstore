from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from rest_framework_simplejwt.tokens import RefreshToken
from utility import *
from .tokens import create_custom_access_token

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate_username(self, data):

#         user = User.objects.filter(username = data).exists()
#         if not user:
#             raise serializers.ValidationError("Username doesn't exist.")
        
#     def validate_email(self, data):
#         user = User.objects.filter(email = data).exists()

#         if not user:
#             raise serializers.ValidationError("Email doesn't exist.")



# class RegisterSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField()
    
#     def validate(self,data):
#         if data['username']:
#             user = User.objects.filter(username = data['username']).exists()
#             if user:
#                 raise serializers.ValidationError("Username is already taken!")
#             # if user doesn't exist then it need to be of certain type -> 
#             else:
#                 if len(data['username']) not in range(8,21):
#                     raise serializers.ValidationError("Username must be in between 8 to 20 of length.")
                
#                 if not data['username'].isalnum():
#                     raise serializers.ValidationError("Username must contain both numbers and alphabets.")
                
#                 # this if condition is redundant or this check need not to be in this way.
#                 if data['username']:
#                     not_allowed_chars = "!@#$%^&*()+?=,<>/"
#                     if any(c in not_allowed_chars for c in data['username']):
#                         raise serializers.ValidationError("Only (_ , - , .) are allowed as a special character.")

#                     allowed_chars = "_-."
#                     allowed_chars_bool = False
#                     for c in allowed_chars:
#                         if c in data['username']:
#                             allowed_chars_bool = True
#                             break
#                     if not allowed_chars_bool:
#                         raise serializers.ValidationError("Username must contain _ , - or .")
                    
#                     # upper and lower case letters are initally False, means no upper and lower case letters exist.
#                     upper_bool, lower_bool = False, False
#                     username = data['username']

#                     for c in username:
#                         if c.isupper():
#                             upper_bool = True
                        
#                         elif c.islower():
#                             lower_bool = True
                    
#                     if not upper_bool:
#                         raise serializers.ValidationError("Username must contain a upper case letter.")
                    
#                     if not lower_bool:
#                         raise serializers.ValidationError("Username must contain a lower case letter.")

#         if data['email']:
#             user = User.objects.filter(email = data['email']).exists()
#             if user:
#                 raise serializers.ValidationError("Email already exist!")
            
#         # There is some logic issue.
#         if data['first_name'] or data['last_name']:
#             f_name = data['first_name']
#             l_name = data['last_name']
#             special_characters = "!@#$%^&*()-+?_=,<>/"

#             if any(c in special_characters for c in f_name):
#                 raise serializers.ValidationError('First name cannot contain special characters.')
            
#             elif any(c in special_characters for c in l_name):
#                 raise serializers.ValidationError('Last name cannot contain special characters.')
                
#         return data
    
#     def create(self, validated_data):
#         user = User.objects.create(username = validated_data['username'], email = validated_data['email'],first_name = validated_data['first_name'], last_name = validated_data['last_name'])
#         user.set_password(validated_data['password'])
#         user.save()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = False)
    username = serializers.CharField(required = False)
    password = serializers.CharField(write_only = True)

    def validate(self, data):

        # If none of username or email was passed.
        if not data.get('username') and not data.get('email'):
            raise serializers.ValidationError("Either email or username is required.")
        
        # # If username was use for login.
        # if data.get('username'):
        #     user = User.objects.filter(username = data.get('username')).exists()

        #     if not user:
        #         raise serializers.ValidationError("No such username exist.")
        
        # # If email was use for login.
        # if data.get('email'):
        #     user = User.objects.filter(email = data.get('email')).exists()

        #     if not user:
        #         raise serializers.ValidationError("No such email exist.")
            
        # Check if user exists for username or email
        if data.get('username'):
            if not User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("Username doesn't exist.")
            
        if data.get('email'):
            if not User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError("Email doesn't exist.")

        return data

class RegisterSerialzier(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)
    first_name = serializers.CharField(required = False)
    last_name = serializers.CharField(required = False)

    def validate(self, data):

        # Email validation
        if data.get('email'):
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError("Email already exists!")
        
        special_characters = "!@#$%^&*()-+?_=,<>/"
        # First name and Last name (It cannot contain special characters)
        if data.get('first_name') or data.get('last_name'):
            f_name = data.get('first_name')
            if any(c in special_characters for c in f_name):
                raise serializers.ValidationError("First name cannot contain special characters.")
            
            l_name = data.get('last_name')
            if any(c in special_characters for c in l_name):
                raise serializers.ValidationError("Last name cannot contain special characters.")
            
        # Username Validation
        if data.get('username'):
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("Username is already taken!")
            
            # If username doesn't already exist, then creating the new user account.
            else:
                user = data['username']
                
                # Checking the length
                if  len(user) < 8 or len(user) > 20:
                    raise serializers.ValidationError("Username must be between 8 and 20 characters.")
                
                # Checking alphanumeric characters (if alphanumeric characters are not present, it means they are special characters.)
    
                # if not user.isalnum():
                #     raise serializers.ValidationError("Username must contain only alphanumeric characters.")
                if not any(c.isdigit() for c in user):
                    raise serializers.ValidationError("Username must contain alteast one digit.")
                
                allowed_special_chars = "_-."

                if not any(c in allowed_special_chars for c in user):
                    raise serializers.ValidationError("Username must contain _ , - or .")
                
                if not any(c.isupper() for c in user):
                    raise serializers.ValidationError("Username must contain atleast one uppercase letter.")
                
                if not any(c.islower() for c in user):
                    raise serializers.ValidationError("Username must contain aleast one lowercase letter.")
        
        # Validating password
        if data.get('password'):
            
            passwd = data.get('password')

            # Password length
            if len(passwd) < 8:
                raise serializers.ValidationError("Password must be atleast 8 characters long.")
        
            if not any(c.isupper() for c in passwd):
                raise serializers.ValidationError("Password must contain at least one uppercase letter.")

            if not any(c.islower() for c in passwd):
                raise serializers.ValidationError("Password must contain at least one lowercase letter.")

            if not any(c.isdigit() for c in passwd):
                raise serializers.ValidationError("Password must contain at least one digit.")

        return data

    def create(self, validated_data)  :
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()

        # # Creating account activation token
        # refresh = RefreshToken.for_user(user)
        # activation_token = {
        #     # 'refresh': str(refresh),
        #     # 'access':str(refresh.access_token)
        # }

        # # Creating account activation token
        # activation_token = create_custom_access_token(user,token_type = 'activation')

        # send_activation_mail(user,activation_token)

        return user
    
class PasswordResetRequestSerializer(serializers.Serializer):
# class ResetPasswordSerializer(serializers.Serializer):
    # def validate(self,data):
    #     email = data.get('email')
    #     user = User.objects.filter(email = email).exists()
    #     if not user:
    #         raise serializers.ValidationError("User with this email doesn't exist.")
    #     reset_password_token = create_custom_access_token(user, token_type='password_reset')
    #     send_reset_password_mail(user, reset_password_token)
    #     passwd = data.get('password')

    #     # Password length
    #     if len(passwd) < 8:
    #         raise serializers.ValidationError("Password must be atleast 8 characters long.")
    
    #     if not any(c.isupper() for c in passwd):
    #         raise serializers.ValidationError("Password must contain at least one uppercase letter.")

    #     if not any(c.islower() for c in passwd):
    #         raise serializers.ValidationError("Password must contain at least one lowercase letter.")

    #     if not any(c.isdigit() for c in passwd):
    #         raise serializers.ValidationError("Password must contain at least one digit.")
    #     user.set_password(passwd)
    #     user.save()

    #############################################################

    # email = serializers.EmailField()
    # user = User.objects.filter(email = email).exists()
    # if not user:
    #     print("user with this email doesn't exist.")
    #     # raise serializers.ValidationError("User with this email doesn't exist.")
    #     raise "User with this email doesn't exist."
    # # reset_password_token = create_custom_access_token(user, token_type='password_reset')
    # # send_reset_password_mail(user, reset_password_token)
    # password = serializers.CharField(write_only = True)
    # def update_password(self, password, user):
    #     user.set_password(password)
    #     user.save()
    # def validate_email(data):
    #####################
    email = serializers.EmailField(required = False)
    username = serializers.CharField(required = False)

    def validate(self, data):

        # If none of username or email was passed.
        
        if not data.get('username') and not data.get('email'):
            raise serializers.ValidationError("Either email or username is required.")
            
        user = None
        # Check if user exists for username or email
        if data.get('username'):
            if not User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("Username doesn't exist.")
            user = User.objects.filter(username = data['username']).first()
            # return user
            
        elif data.get('email'):
            if not User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError("Email doesn't exist.")
            user = User.objects.filter(email = data['email']).first()
            # return user
            
        self.user = user
        return data
    
    def save(self):
        return self.user

######################################
        # reset_password_token = create_custom_access_token(user, token_type='password_reset')
        # send_reset_password_mail(user, reset_password_token)

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only = True, required = True )
    confirm_password = serializers.CharField(write_only = True, required =  True)

    # Override the init method to accept user as a parameter
    def __init__(self, *args, user = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
    def validate(self, data):
        passwd = data.get('new_password')

    # "Martian@0612"
        # Password length
        if len(passwd) < 8:
            raise serializers.ValidationError("Password must be atleast 8 characters long.")
    
        if not any(c.isupper() for c in passwd):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")

        if not any(c.islower() for c in passwd):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")

        if not any(c.isdigit() for c in passwd):
            raise serializers.ValidationError("Password must contain at least one digit.")

        """
        Check that the password and confirm password fields match.
        """

        confirm_passwd = data['confirm_password']
        if passwd != confirm_passwd:
            raise serializers.ValidationError("The two password fields must match.")

        return data
    
    def save(self):

        """
        Save the new password to the user's account.
        """
        print("i got the user ", self.user)
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class BookSerializer(serializers.Serializer):
    likes_count = serializers.IntegerField(read_only = True)
    rating_average = serializers.FloatField(read_only = True)
    rating_count = serializers.IntegerField(read_only = True)
    comment_count = serializers.IntegerField(read_only = True)

    class Meta:
        model = Book
        fields = ['title','author','publisher','published_date','cover_image','genre','description','language','number_of_pages','isbn_number','likes_count','rating_average','rating_count','comment_count']

        def validate_isbn_number(self, value):
            if len(value) != 13:
                return serializers.ValidationError("Isbn number must be of 13 digits.")
            
            if value[:3] != "978" or value[:3] != "979":
                return serializers.ValidationError("Isbn number must start from either 978 or 979.")
            
            
            return value
          
        # likes_count = serializers.SerializerMethodField()
        # def get_likes_count(self, obj):
        #     book_obj = Book.objects.filter(title = obj['title']) 
        #     like_cnt = book_obj.book_like.aggregate(count = Count('user'))
        #     return like_cnt

        
        # rating_average_count = serializers.SerializerMethodField()
        # def rating_average(self,obj):
        #     book_obj = Book.objects.filter(title = obj['title']) 
        #     rating_avg = book_obj.book_rating.aggregate(avg = Avg('rating'))
        #     return rating_avg

        # rating_count = serializers.SerializerMethodField()
        # def rating_count(self,obj):
        #     book_obj = Book.objects.filter(title = obj['title']) 
        #     rating_cnt = book_obj.book_rating.aggregate(count = Count('user'))
        #     return rating_cnt

        # comment_count = serializers.SerializerMethodField()
        # def comment_count(self, obj):
        #     book_obj = Book.objects.filter(title = obj['title']) 
        #     comment_cnt = book_obj.book_comment.aggregate(count = Count('user'))
        #     return comment_cnt

    

        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'