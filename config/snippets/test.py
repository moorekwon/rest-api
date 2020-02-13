import random

from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from members.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetTest(APITestCase):
    '''
    postman이 하는 일을 코드로 자동화
    db는 분리됨
    '''

    def test_snippet_list(self):
        url = '/api-view/snippets/'
        # client -> requests와 비슷한 포지션
        response = self.client.get(url)

        # print('response.data >> ', response.data)
        # assertEqual -> status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # 5개의 Snippet을 만들고 응답 객체 개수 비교
        # user = User.objects.create(username='test')

        # for i in range(5):
        #     Snippet.objects.create(code='1', author=user)

        baker.make(Snippet, _quantity=5)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        for snippet_data in response.data:
            self.assertIn('author', snippet_data)
            self.assertIn('title', snippet_data)
            self.assertIn('code', snippet_data)
            self.assertIn('linenos', snippet_data)
            self.assertIn('language', snippet_data)
            self.assertIn('style', snippet_data)

            # self.assertEqual('1', snippet_data['code'])

            # 전달된 Snippet object(dict)의 'pk'에 해당하는 실제 Snippet model instance를
            # SnippetSerializer를 통해 serialize한 값과 snippet_data가 같은지 비교
            pk = snippet_data['pk']
            snippet = Snippet.objects.get(pk=pk)
            self.assertEqual(SnippetSerializer(snippet).data, snippet_data)

    def test_snippet_create(self):
        '''
        Snippet 객체 만들기
        '''
        url = '/api-view/snippets/'

        # 클라이언트로부터 전달될 json 객체를 parse한 python 객체
        data = {
            'code': 'def abc():'
        }

        # 인증이 안돼있으면 실패함을 기대
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 특정 유저로 인증된 상태라면, 생성됨을 기대
        user = baker.make(User)
        self.client.force_login(user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 응답에 돌아온 객체가 SnippetSerializer로 실제 model instance를 serialize한 결과와 같은지 확인
        pk = response.data['pk']
        snippet = Snippet.objects.get(pk=pk)
        self.assertEqual(SnippetSerializer(snippet).data, response.data)
        # 전체 Snippet 객체 개수가 1개인지 확인(orm)
        self.assertEqual(Snippet.objects.count(), 1)

    def test_snippet_delete(self):
        '''
        미리 객체를 5개 만들어놓음
        delete api를 적절히 실행한 후, 객체가 4개가 되었는지 확인
        지운 객체가 실제로 존재하지 않는지 확인
        '''
        # user = User.objects.create(username='test')
        # snippets = [Snippet.objects.create(code='1', author=user) for i in range(5)]

        snippets = baker.make(Snippet, _quantity=5)
        snippet = random.choice(snippets)
        url = f'/api-view/snippets/{snippet.pk}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 4)
        self.assertFalse(Snippet.objects.filter(pk=snippet.pk).exists())
