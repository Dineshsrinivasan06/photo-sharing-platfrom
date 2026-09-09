from importlib import import_module

from .config import settings


cloudinary = import_module("cloudinary")

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)


def upload_photo(file):
    uploader = import_module("cloudinary.uploader")
    result = uploader.upload(
        file,
        folder="photo-sharing-platform"
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
        "file_size": result.get("bytes", 0),
    }