from rest_framework import serializers

from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet


class SnippetSerializer(serializers.Serializer):
    class Meta:
        model = Snippet
        fields = ('pk', 'title', 'code', 'linenos', 'language', 'style', 'created')
