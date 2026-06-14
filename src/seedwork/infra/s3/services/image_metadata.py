class ImageMetadataService:
    def content_type(self, filename: str) -> str:
        suffix = filename.rsplit(".", maxsplit=1)[-1].lower()
        return {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "webp": "image/webp",
        }.get(suffix, "application/octet-stream")
