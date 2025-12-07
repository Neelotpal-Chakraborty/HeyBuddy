class OAuthClient:

    @staticmethod
    def get_login_url():
        # Google/Auth0 redirect URL
        return "https://accounts.google.com/o/oauth2/v2/auth?..."

    @staticmethod
    def exchange_code_for_user(code: str):
        # Call OAuth provider, return user info
        return {
            "email": "test@example.com",
            "name": "Test User",
            "sub": "12345"
        }
