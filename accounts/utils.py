
import uuid



from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

    return data


def generate_ref_code():

    code = str(uuid.uuid4()).replace("-", "")[:6]

    return code

# def increase_ref_count(code):
#     try:
#         user = User.objects.get(my_ref_code=code)
#         user.my_ref_code = user.my_ref_code + 1
#         user.save()
#     except:
#         pass
