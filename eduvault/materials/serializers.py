from rest_framework import serializers
from .models import Material

class MaterialSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = '__all__'

    def get_file(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url)