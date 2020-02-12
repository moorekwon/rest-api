from django.urls import path, include
from . import views
from . import apis
from .apis import mixins, generics, viewsets

app_name = 'snippets'

urlpatterns_api_view = [
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>/', views.snippet_detail),

    # class-based view 사용하는 경우, as_view 함수 호출
    # 클래스 자체를 전달하는 것이 아니라, as_view()로 함수를 만들어서 그 함수를 전달
    # 클래스를 호출하면 인스턴스가 호출되고, 함수를 호출하면 해당값이 바로 호출
    # path('snippets/', apis.SnippetListCreateAPIView.as_view()),
    # path('snippets/<int:pk>/', apis.SnippetRetrieveUpdateDestroyAPIView.as_view()),

    # path('snippets/', mixins.SnippetListCreateAPIView.as_view()),
    # path('snippets/<int:pk>/', mixins.SnippetRetrieveUpdateDestroyAPIView.as_view()),

    path('snippets/', generics.SnippetListCreateAPIView.as_view()),
    path('snippets/<int:pk>/', generics.SnippetRetrieveUpdateDestroyAPIView.as_view())
]

urlpatterns_viewset = [
    path('snippets/', viewsets.SnippetViewSet.as_view({
        'get': 'list',
        'post': 'create'})),
    path('snippets/<int:pk>/', viewsets.SnippetViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'}))
]

urlpatterns = [
    path('api-view/', include(urlpatterns_api_view)),
    path('viewsets/', include(urlpatterns_viewset))
]
