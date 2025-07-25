from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request:Request): #request:Request is a type hint in Python indicating that the request 
        #parameter of the authenticate method is an instance of the Request class from Django REST Framework (DRF),
        # specifically rest_framework.request.Request
        refresh = request.COOKIES.get('refresh_token')
        access_token  = request.COOKIES.get('access_token') #Retrieves the value of 'access_token' from the request's cookies.
                        ## Returns None if the cookie is not present.
        if not (refresh and access_token):
            return None
        
        try:
            validated_token = self.get_validated_token(access_token)#Validates the given access token using the method get_validated_token.
            #The get_validated_token() method comes from TokenAuthentication classes in Django REST Framework SimpleJWT.
        except (InvalidToken, TokenError) as e:
            raise AuthenticationFailed('Invalid or expired access token') from e
        
        #from e links the new exception (AuthenticationFailed) to the original exception (e) that caused it.
        #So instead of hiding the original error, Python shows the full traceback
        #AuthenticationFailed: Invalid or expired access token, The above exception was the direct cause of the following exception:
        
        
        user = self.get_user(validated_token)
        #The method get_user() comes from the JWTAuthentication class in Django REST Framework SimpleJWT.
        return user, validated_token
    #If you only return the user, request.auth will be None, and you won’t be able to access token info later (like scopes or custom claims).
    
            
            
            
        








'''The `authenticate.py` file in your `authenticate` app defines a custom authentication class, 
`CustomJwtAuthentication`, which extends `JWTAuthentication` from `rest_framework_simplejwt` to handle HTTP-only
cookie-based JWT authentication for your Django REST Framework (DRF) app. This class overrides the `authenticate` 
method to extract `refresh_token` and `access_token` from HTTP-only cookies in the request, rather than from 
headers, aligning with your app’s cookie-based authentication strategy. It validates the access token using 
`get_validated_token`,raising an `AuthenticationFailed` exception if the token is invalid or expired. If valid, 
it retrieves the associated user with `get_user` and returns the user and token for DRF to authenticate the 
request. The commented-out code suggests an optional email verification check, which could raise a 
`PermissionDenied` error if the user’s email isn’t verified. This file is crucial for enforcing secure, 
cookie-based JWT authentication, ensuring only valid, authenticated users access protected API endpoints.
It integrates with your `settings.py` where `CustomJwtAuthentication` is set as the default authentication
class in `REST_FRAMEWORK`. This custom logic allows seamless integration with your React (Vite) frontend, 
which relies on cookies for authentication.'''