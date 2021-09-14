from rest_framework import (
    serializers,
)
from .models import (
    Images,
)


class ImageListSerialaizer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = '__all__'