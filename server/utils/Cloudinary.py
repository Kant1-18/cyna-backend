from cloudinary import uploader


class ImageUploader:

    @staticmethod
    def product(file, folder="products"):
        upload_result = uploader.upload(file, folder=folder)
        return upload_result.get("secure_url")
