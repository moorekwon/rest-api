from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView


class AuthTokenAPIView(APIView):
    def post(self, request):
        # url과 view 연결, postman에 작성
        # postman의 body에 작성한 내용이
        #   send 버튼을 누른뒤 이 view의 request.data에 원하는 데이터가 오는지 확인

        # 적절한 데이터가 온다면, authenticate() 함수 사용
        #   User 객체 얻어냄
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)

        # 얻어낸 User 객체와 연결되는 Token을 get_or_create()로 가져오거나 생성
        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed()

        # 생성된 Token의 key 속성을 적절히 반환
        data = {
            'token': token.key,
        }
        return Response(data)
