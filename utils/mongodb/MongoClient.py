
import os
import structlog
import boto3
from motor.motor_asyncio import AsyncIOMotorClient
from config.constants import (
    MONGO_URL,
    ENV,
    AWS_DEFAULT_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_BUCKET_NAME,
    AWS_OBJECT_NAME
)

LOGGER = structlog.get_logger().bind(module="MongoClient")


class MongoClient:
    _client: AsyncIOMotorClient = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if not cls._client:
            cls.connect()
        return cls._client

    @classmethod
    def connect(cls):
        LOGGER.info("Connecting to mongo")
        try:
            if ENV == "local":
                cls._client = AsyncIOMotorClient(MONGO_URL)
                LOGGER.info("mongo connected")
            else:
                cls.get_cert()
                cls._client = AsyncIOMotorClient(
                        MONGO_URL,
                        tls=True,
                        authMechanism="MONGODB-X509",
                        authSource="$external",
                        tlsCertificateKeyFile="/tmp/certificate.pem",
                )
                os.remove('/tmp/certificate.pem')
                LOGGER.info("mongo connected")

        except Exception as err:
            LOGGER.error(f"mongo connection w/error: {err}")
            raise err

    @classmethod
    def close_connection(cls):
        LOGGER.info("Closing mongo connection")
        try:
            cls._client.close()
            LOGGER.info("mongo connection closed")

        except Exception as err:
            LOGGER.error(f"mongo close w/error: {err}")

    @classmethod
    def get_cert(cls) -> None:
        """ Get mongo cert in S3"""
        LOGGER.info("Mongo cert: start")
        s3 = boto3.client(
                "s3",
                region_name=AWS_DEFAULT_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        LOGGER.info("S3 connection success")
        s3.download_file(AWS_BUCKET_NAME, AWS_OBJECT_NAME, "/tmp/certificate.pem")
        LOGGER.info("Mongo cert: success")
