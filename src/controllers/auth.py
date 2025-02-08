from fastapi import Request, HTTPException, Response
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter
from ..settings import settings
import jwt
from datetime import datetime, timedelta

# Create a global oauth
oauth: OAuth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url=settings.ACCESS_TOKEN_URL,
    authorize_url=settings.AUTHORIZE_URL,
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url=settings.METADATA_URL
)

def create_token(payload: dict) -> str:
    token_payload = {
        **payload,
        'exp': datetime.now() + timedelta(hours=30)
    }
    return jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')

def get_user_info(request: Request) -> dict:
    try:
        token = request.cookies["access_token"]
        payload = jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except Exception:
        raise HTTPException(401,"Token invalid")

router = APIRouter()

# Login endpoint
@router.get("/auth/login")
async def login_with_google(request: Request):
    redirect_uri = "http://localhost:8000/auth/callback" # Callback URL
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Callback endpoint
@router.get("/auth/callback")
async def auth_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")
        if not user_info:
            raise HTTPException(status_code=400, detail="User info not available")
        
        # Process user_info
        jwt_token = create_token({"user_info": user_info})

        # Redirect to frontend
        response = RedirectResponse(url="/")
        response.set_cookie(key="access_token", value=jwt_token, max_age=30 * 60, path="/")
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

@router.get("/auth/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}
