from cloudinary import uploader


def upload_image(file, folder="products"):
    upload_result = uploader.upload(file, folder=folder)
    return upload_result.get("secure_url")
