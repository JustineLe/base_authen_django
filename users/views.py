from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data

            name = data['name']
            email = data['email']
            email = email.lower()
            password = data['password']
            re_password = data['re_password']

            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(email=email).exists():
                        User.objects.create_user(name=name, email=email, password=password)
                        return Response(
                            {'success': 'User created successfully.'},
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        return Response(
                            {'error': 'User with this email already exists.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'error': 'Password must be at least 8 characters.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': 'Passwords do not match.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': 'Something went wrong while registering.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
