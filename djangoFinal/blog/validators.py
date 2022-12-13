from django.core import exceptions


def validate_only_alphabet(value):
    for ch in value:
        if not ch.isalpha():
            raise exceptions.ValidationError('Ensure this value contains only letters.')


def validate_image_size(image):
    file_size = image.file.size
    limit_mb = 5
    if file_size >= limit_mb * 1024 * 1024:
        raise exceptions.ValidationError("Max file size is 5.00 MB")
