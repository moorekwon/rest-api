from rest_framework import serializers

from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('author', 'pk', 'title', 'code', 'linenos', 'language', 'style', 'created')


class SnippetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('title', 'code', 'linenos', 'language', 'style', 'created')

    def to_representation(self, instance):
        return SnippetSerializer(instance).data
