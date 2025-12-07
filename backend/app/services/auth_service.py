from app.utils.oauth_client import OAuthClient
from app.core.jwt_manager import JWTManager

class AuthService:

    @staticmethod
    def redirect_to_sso():
        return {"url": OAuthClient.get_login_url()}

    @staticmethod
    def handle_callback(code: str):
        user_info = OAuthClient.exchange_code_for_user(code)
        access = JWTManager.create_access_token(user_info)
        refresh = JWTManager.create_refresh_token(user_info)
        return {
            "access_token": access,
            "refresh_token": refresh,
            "user": user_info
        }
