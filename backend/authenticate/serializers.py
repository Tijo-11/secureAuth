import re #Imports Python's built-in regular expression module for pattern matching and text processing.
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ #Imports Django's translation function to mark strings for lazy translation using the alias '_'.
#Useful for making strings translatable in multilingual applications.
from django.contrib.auth import get_user_model
from django.core.validators import validate_email as django_validate_email
'''Imports a function that returns the currently active User model.
Useful for supporting custom user models instead of directly importing django.contrib.auth.models.User.
django.contrib.auth.models.User is Django’s default built-in User model.Incudes username, password (hashed),
email first_name, last_name is_staff, is_superuser, is_active last_login, date_joined and Methods like
set_password(), check_password(), get_full_name().
If you use a custom user model (recommended for flexibility), you shouldn’t import User directly.
Instead, use:from django.contrib.auth import get_user_model
User = get_user_model()
This ensures your project works whether you're using the default or a custom User model.'''
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

User = get_user_model()
#you can safely use get_user_model() without defining a custom user model in your models.py. If you haven’t 
# defined a custom user model, get_user_model() simply returns Django’s default User model, which lives in:
#django.contrib.auth.models.User
#This makes your code future-proof — if you later switch to a custom user model, you won’t need to change 
# your imports. This is better to  ensures compatibility across project than from django.contrib.auth.models 
# import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    
    class Meta:
        model = User #User will point to the default Django user model (django.contrib.auth.models.User), 
#unless you've defined a custom one in settings.py with AUTH_USER_MODEL.
        fields = ('id', 'username', 'email', 'password')
    def validate_username(self, value): #The method name must be validate_<field_name>. Here field name is username
        #so value becomes username passed
        reserved_usernames = ['admin', 'superuser', 'null', 'undefined']
#Names like null, undefined, or none could: Be misinterpreted by JavaScript/Python code. Cause bugs or 
# display weirdly in templates or URLs.Some names may conflict with URL paths (e.g., /admin, /login, etc.)
# Impersonation – Users shouldn't register as admin, root, or superuser, as that could mislead others into
# thinking they have special access.
        if value.lower() in reserved_usernames:
            raise serializers.ValidationError("This username is reserved and can not be used")
        if not re.match(r'^[a-zA-Z0-9_.-]+$', value):#^ and $ mean the pattern must match the entire string
            #+ means one or more allowed characters
            raise serializers.ValidationError("Username can only contain letters, numbers, underscores, dots, or hyphens.")
        if len(value)<5:
            raise serializers.ValidationError("Username must be at least 5 characters long.")
        return value
    
    def validate_email(self, value):
        # Use Django's built-in email validator
        try:
            django_validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid Email Address")
        # Custom rule: Block certain domains
        if value.endswith('@tempmail.com'):
            raise serializers.ValidationError("Temporary emails are not allowed.")
        
        return value
    
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError("e.messages")
        return value
    
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email = validated_data['email'],
            password= validated_data['password'],
            )
#In Django REST Framework (DRF), when your serializer runs validation, each validated field is automatically 
# stored in validated_data as a key–value pair

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only =True) #DRF doesn't have a PasswordField. write_only=True: 
    #so the password is never returned in API responses.
    
    def validate(self, data):
#the data dictionary contains the validated values of the fields defined in your serializer — 
# like username and password. validate(self, data) is the global validation method in DRF serializers.
#DRF calls it after all individual field validations have passed (validate_username(), validate_password(), etc.)

        user = authenticate(username= data['username'], password = data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid Username or Password", code=401)
        data['user'] = user
        return data
#This works inside the serializer, but Django REST Framework only calls validate() after you call is_valid()
# in the view or controller logic:  just make sure to call is_valid() in view before accessing validated_data.
        
            
        
