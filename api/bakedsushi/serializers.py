from rest_framework import serializers
from .models import ContactListModel

class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactListModel
        fields = '__all__'

def filter_heic_files(images):
    """Filter out .heic files from images array"""
    if not images:
        return images

    filtered_images = []
    seen_urls = set()

    for image in images:
        if isinstance(image, dict) and 'url' in image:
            url = image['url']
            # Check if it's a .heic file
            if url.lower().endswith('.heic'):
                continue
            # Check for duplicates
            if url in seen_urls:
                continue
            seen_urls.add(url)
            filtered_images.append(image)
        elif isinstance(image, str):
            # Handle direct URL strings
            if image.lower().endswith('.heic'):
                continue
            if image in seen_urls:
                continue
            seen_urls.add(image)
            filtered_images.append(image)

    return filtered_images