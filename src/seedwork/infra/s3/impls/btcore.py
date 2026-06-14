# pyright: reportGeneralTypeIssues=false, reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false

from typing import Any

from aiobotocore.client import AioBaseClient


class S3AiobotoClient:
    def __init__(self, client: AioBaseClient) -> None:
        self._client = client

    async def put_object(
        self,
        bucket: str,
        key: str,
        body: bytes,
        content_type: str | None = None,
    ) -> None:
        params: dict[str, Any] = {
            "Bucket": bucket,
            "Key": key,
            "Body": body,
        }
        if content_type is not None:
            params["ContentType"] = content_type

        await self._client.put_object(**params)

    async def get_object(self, bucket: str, key: str) -> bytes:
        response = await self._client.get_object(Bucket=bucket, Key=key)
        body = response["Body"]
        async with body:
            data = await body.read()
        return bytes(data)

    async def delete_object(self, bucket: str, key: str) -> None:
        await self._client.delete_object(Bucket=bucket, Key=key)
