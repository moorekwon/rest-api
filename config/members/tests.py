from django.test import TestCase

# Create your tests here.
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User
from .serializers import UserSerializer


class AuthAPITest(APITestCase):
    def test_token_api(self):
        url = '/members/auth-token/'
        username = 'test_username'
        password = 'test_password'

        # 유저 생성
        user = baker.make(User, username=username)
        user.set_password(password)
        user.save()

        # 전송돼 올 것이라 가정한 데이터
        data = {
            'username': username,
            'password': password,
        }

        # POST 방식으로 요청 보내봄
        response = self.client.post(url, data)

        # 상태코드 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 토큰이 왔는지
        # 유저정보가 왔는지
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

        # 정상적인게 왔는지
        # User 인스턴스를 serialize한 결과가 response.data의 'user' key의 value(object)와 같은지 확인
        self.assertEqual(
            UserSerializer(user).data,
            response.data['user']
        )
        # response.data의 'token' key의 value가 user와 연결된 Token의 key인지 확인
        self.assertIsNotNone(user.auth_token)
        self.assertEqual(
            user.auth_token.key,
            response.data['token']
        )
