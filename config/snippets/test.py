import random

from rest_framework import status
from rest_framework.test import APITestCase

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
        for i in range(5):
            Snippet.objects.create(code='1')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        for snippet_data in response.data:
            self.assertIn('title', snippet_data)
            self.assertIn('code', snippet_data)
            self.assertIn('linenos', snippet_data)
            self.assertIn('language', snippet_data)
            self.assertIn('style', snippet_data)

            self.assertEqual('1', snippet_data['code'])

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
        snippets = [Snippet.objects.create(code='1') for i in range(5)]
        snippet = random.choice(snippets)
        url = f'/api-view/snippets/{snippet.pk}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 4)
        self.assertFalse(Snippet.objects.filter(pk=snippet.pk).exists())
