from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .authenticate import CustomJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken,TokenError #to generate and manage JWT refresh and access tokens.
#Commonly used to manually create tokens for a user during login or registration.
from django.views.decorators.csrf import csrf_protect, csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator


class RegisterView(APIView):
    authentication_classes = [] #Disables authentication and permission checks for this view.
    permission_classes = []
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data= data) #Initializes the serializer with incoming data (from a request) for validation and deserialization.
        if serializer.is_valid(): #triggers the serializer’s validation process, including:Field-level validation (e.g., validate_username)
            #Custom validation logic (e.g., validate(self, data)).If everything is valid, serializer.validated_data is populated.

            serializer.save() #Calls the serializer's create() or update() method to save validated data to the database
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
'''Here we are not sending tokens after registration because we need user to verify his email. So he need to
login again. If we want to send tokens we can send that using
refresh = RefreshToken.for_user(user)# manually generate tokens using RefreshToken.for_user(user)
access_token = str(refresh.access_token)
refresh_token = str(refresh) and then adding them to Response'''

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = []
    permission_classes =[]
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data= data)
        serializer.is_valid(raise_exception= True)#In login, you want to fail fast if credentials are invalid.
        # so raise_exception is used here, not in Register. In register view also it should be used
        #It's often recommended for cleaner and safer code
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        response = Response({"detail": "Login successful"},status=status.HTTP_200_OK)
        response.set_cookie(
            key= 'refresh_token',
            value= str(refresh),
            httponly=True,
            secure= True, #Ensures the cookie is only sent over HTTPS connections.
            samesite= 'None' #It allows the cookie to be sent in cross-site requests (e.g., from a different domain).
            #Required when using cookies for authentication in cross-origin setups (like frontend on a different domain).
        )
        response.set_cookie(#This method is provided by Django's HttpResponse (and subclasses like JsonResponse or DRF's Response).
            key='access_token',
            value = str(refresh.access_token),
            httponly= True,
            secure= True,#Helps protect sensitive cookies (like access tokens) from being exposed over insecure (HTTP) requests.
            samesite= 'None' # None must be a string, not Python None. If None will default to 'Lax' or be ignored
        )
        response.set_cookie(
                'csrftoken',
                request.META.get('CSRF_COOKIE'),
                httponly=False,  # Allow axios to read
                secure=True,
                samesite='None',#The csrftoken is typically set by Django’s CsrfViewMiddleware for POST requests, 
                #but it may not be sent correctly
                #due to SameSite='None' or Secure=True misconfiguration.
            )
        
        return response
    
''' Here we are  manually creating the response first. This allows you to attach cookies to the
response before returning it. If you use return Response , You’d have no chance to insert set_cookie() calls
unless you modify the response object first — which would look messy.
return Response(...) Quick for sending JSON/data-only responses
response = Response(...) → set_cookie() → return response :- Used when setting cookies or headers'''




@method_decorator(csrf_exempt, name='dispatch') #Revert to csrf_protect after confirming CORS works and add CSRF token handling in src/axios/index.js 
class RefreshView(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):  # Defines the POST method handler for the APIView.
        # Called when a POST request is made to this view (e.g., for login, registration, form submission).

        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            # If the refresh_token cookie is not present, return 401 (unauthorized)
            return Response({"detail": "Refresh token missing"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # 1. Validate the existing refresh token
            old_token = RefreshToken(refresh_token)  # Initializes a RefreshToken instance from an existing refresh token string.
            # Useful for validating the token or extracting its payload (e.g., user ID).
            # Will raise TokenError if the token is invalid or expired.
            user_id = old_token['user_id']
            # 2. Retrieve the user associated with the refresh token
            user = User.objects.get(id=user_id) # Automatically resolved by SimpleJWT from the token's payload

            # 3. Create a NEW refresh token for this user (token rotation)
            new_refresh = RefreshToken.for_user(user)  # Securely generates a fresh refresh token with new jti, exp, etc.

            # 4. Generate a new Response object to attach cookies
            response = Response({"detail": "Token refreshed"}, status=status.HTTP_200_OK)

            # 5. Set new refresh token in HttpOnly secure cookie
            response.set_cookie(
                key='refresh_token',
                value=str(new_refresh),
                httponly=True,  # Prevents JavaScript access to the cookie — defends against XSS
                secure=True,    # Ensures the cookie is only sent over HTTPS connections
                samesite='None' # Required for cross-site requests (e.g., frontend on different domain)
            )

            # 6. Set new access token in HttpOnly secure cookie
            response.set_cookie(
                key='access_token',
                value=str(new_refresh.access_token),  # access_token is a property on the RefreshToken object
                httponly=True,
                secure=True,
                samesite='None'
            )
            

            return response

        except TokenError as e:
            # If the token is expired or tampered with, log the issue and clear cookies
            print("Refresh token error:", e)
            response = Response({"detail": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)
            response.delete_cookie('refresh_token')  # Force logout on client side
            response.delete_cookie('access_token')
            return response
            


@method_decorator(csrf_protect, name='dispatch')
class GetUser(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user # Retrieves the currently authenticated user from the request.
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200) #Returns serialized user data as JSON.

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @method_decorator(csrf_exempt)  # Remove in production
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
            response = Response({'detail': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            response.delete_cookie('csrftoken')  # Clear CSRF token
            return response
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfTokenView(APIView):
    permission_classes = []
    authentication_classes = []
    
    def get(self, request):
        return Response({'csrfToken': request.META.get('CSRF_COOKIE')}, status=status.HTTP_200_OK)













''' def post(self, request):#Logging out modifies server-side or client-side state (e.g., deleting cookies or invalidating tokens), so:
        #Use POST for operations that cause side effects (per REST best practices).
        #POST requests can be protected by CSRF tokens.
        #Using GET for logout means: could log users out just by visiting a link — not ideal! ''' 
        
        
        
    
        
