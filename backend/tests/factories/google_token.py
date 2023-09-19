from app.schemas.auth import GoogleDecodedJWT
from factory import Factory, Faker


class GoogleTokenFactory(Factory):
    class Meta:
        model = GoogleDecodedJWT

    iss = "accounts.google.com"
    azp = "1234567890.apps.googleusercontent.com"
    aud = "1234567890.apps.googleusercontent.com"
    sub = "110169484474386276334"
    email = Faker("email")
    email_verified = True
    given_name = Faker("first_name")
    family_name = Faker("last_name")
    iat = 1516239022
    exp = 1516242622
    name = Faker("name")
    picture = Faker("image_url")
    locale = "en"
    jti = "1234567890abcdefghijklmnopqrstuvwxyz"
    alg = "RS256"
    kid = "1234567890abcdefghijklmnopqrstuv"
    typ = "JWT"
    nbf = 1516239022
    hd = "example.com"
