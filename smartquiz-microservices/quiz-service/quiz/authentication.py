# quiz/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication


class DummyUser:
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role

    @property
    def is_authenticated(self):
        return True


class StatelessJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        user = DummyUser(
            user_id=validated_token.get("user_id"),
            username=validated_token.get("username"),
            role=validated_token.get("role"),
        )

        return (user, validated_token)