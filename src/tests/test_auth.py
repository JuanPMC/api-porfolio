from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app

client = TestClient(app)

def test_login_with_google():
    with patch("src.controllers.auth.oauth.google.authorize_redirect") as mock_authorize_redirect:
        mock_authorize_redirect.return_value = "http://mocked-auth-url"
        response = client.get("/auth/login")
        
        assert response.status_code == 200
        mock_authorize_redirect.assert_called()

def test_auth_callback():
    with patch("src.controllers.auth.oauth.google.authorize_access_token", return_value={"userinfo": {"email": "test@example.com"}}) as mock_authorize_access_token, \
         patch("src.controllers.auth.create_token", return_value="mocked_jwt_token") as mock_create_token:
        
        response = client.get("/auth/callback", follow_redirects=False)
        
        assert response.status_code == 307 # Redirect response
        assert "mocked_jwt_token" in response.headers["set-cookie"]
        mock_create_token.assert_called()
        mock_authorize_access_token.assert_called()

def test_auth_callback_failure():
    with patch("src.controllers.auth.oauth.google.authorize_access_token", side_effect=Exception("OAuth Error")) as mock_authorize_access_token:
        response = client.get("/auth/callback")
        
        assert response.status_code == 400
        assert response.json()["detail"].startswith("Authentication failed")

def test_logout():
    response = client.get("/auth/logout")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}
