from rest_framework import serializers
from .models import ContactListModel

class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactListModel
        fields = '__all__'

    class Meta:
        model = FileUploadModel
        fields = '__all__'

    def validate_file(self, value):
        """Validate uploaded file to reject .heic files"""
        if value:
            filename = value.name.lower()
            if filename.endswith('.heic'):
                raise serializers.ValidationError(
                    "HEIC files are not supported. Please upload JPG, PNG, or WebP images."
                )
        return value