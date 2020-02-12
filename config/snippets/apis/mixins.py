'''
model, serializer가 달라짐
generic -> 같은 로직을 쓰는 부분을 다 구현해놓고, 다른 부분을 쓸 수 있게 해줌
'''
from rest_framework import generics, mixins

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetListCreateAPIView(mixins.ListModelMixin,
                               generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SnippetRetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                          mixins.UpdateModelMixin,
                                          mixins.DestroyModelMixin,
                                          generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
