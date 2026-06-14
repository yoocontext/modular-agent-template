from typing import Protocol


class IS3Client(Protocol):
    async def put_object(
        self,
        bucket: str,
        key: str,
        body: bytes,
        content_type: str | None = None,
    ) -> None: ...

    async def get_object(self, bucket: str, key: str) -> bytes: ...

    async def delete_object(self, bucket: str, key: str) -> None: ...
