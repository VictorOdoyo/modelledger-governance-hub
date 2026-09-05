from dataclasses import dataclass

import boto3


@dataclass(frozen=True)
class PresignedUpload:
    url: str
    fields: dict[str, str]


class MinioArtifactStore:
    def __init__(self, endpoint_url: str, bucket: str) -> None:
        self.bucket = bucket
        self.client = boto3.client("s3", endpoint_url=endpoint_url)

    def create_upload(self, key: str, content_type: str, expires: int = 900) -> PresignedUpload:
        response = self.client.generate_presigned_post(
            Bucket=self.bucket,
            Key=key,
            Fields={"Content-Type": content_type},
            Conditions=[{"Content-Type": content_type}],
            ExpiresIn=expires,
        )
        return PresignedUpload(url=response["url"], fields=response["fields"])
