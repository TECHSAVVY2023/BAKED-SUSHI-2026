import os
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.shortcuts import redirect
import urllib.parse
import base64

from .utils.auth import is_authorized, create_jwt

def get_frontend_url():
    return os.getenv("FRONTEND_BAKEDSUSHI_URL").rstrip('/')

def get_backend_url(request):
    host = request.get_host()
    if host.startswith('127.0.0.1'):
        host = host.replace('127.0.0.1', 'localhost')
    return f"{request.scheme}://{host}"

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        redirect_uri = f"{get_backend_url(request)}/api/ra/auth/google/callback/"
        
        origin = request.GET.get('origin', get_frontend_url())
        state_data = {
            'redirect_uri': redirect_uri,
            'frontend_url': origin.rstrip('/')
        }
        import json
        state = base64.b64encode(json.dumps(state_data).encode('utf-8')).decode('utf-8')
        
        url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
            "state": state
        })
        return redirect(url)

class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return redirect(f"{get_frontend_url()}/login?error=no_code")
            
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        secret = os.getenv("AUTH_SECRET", getattr(settings, 'AUTH_SECRET', ''))
        
        frontend_url = get_frontend_url()
        redirect_uri = f"{get_backend_url(request)}/api/ra/auth/google/callback/"

        state_param = request.GET.get('state')
        if state_param:
            try:
                import json
                state_data = json.loads(base64.b64decode(state_param).decode('utf-8'))
                redirect_uri = state_data.get('redirect_uri', redirect_uri)
                frontend_url = state_data.get('frontend_url', frontend_url)
            except Exception:
                pass

        try:
            # Exchange auth code for access token
            token_res = requests.post('https://oauth2.googleapis.com/token', data={
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code',
            }).json()
            
            if 'access_token' not in token_res:
                return redirect(f"{frontend_url}/login?error=oauth_failed")
                
            # Get user profile
            profile_res = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers={
                'Authorization': f"Bearer {token_res['access_token']}"
            }).json()
            
            if not is_authorized(profile_res):
                return redirect(f"{frontend_url}/login?error=unauthorized")
                
            # Create JWT
            jwt = create_jwt({
                'id': profile_res.get('sub'),
                'name': profile_res.get('name'),
                'email': profile_res.get('email'),
                'picture': profile_res.get('picture')
            }, secret)
            
            # Redirect to frontend dashboard with token
            return redirect(f"{frontend_url}/dashboard?token={jwt}")
            
        except Exception as e:
            return redirect(f"{frontend_url}/login?error=oauth_failed")

class AuthMeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(request.user.payload)

class AuthLogoutView(APIView):
    def post(self, request):
        return Response({"status": "logged_out"})
