
import structlog
from piccolo.engine import engine_finder

LOGGER = structlog.get_logger().bind(module="SqlDBConn")


class SqlDBConn:
    @classmethod
    async def connect(cls):
        LOGGER.info("Connecting to PSQL")
        try:
            engine = engine_finder()  # module_name="config.piccolo_conf")
            await engine.start_connection_pool()
            LOGGER.info("PSQL connected")

        except Exception as err:
            LOGGER.error(f"PSQL connection w/error: {err}")

    @classmethod
    async def close_connection(cls):
        LOGGER.info("Closing PSQL connection")
        try:
            engine = engine_finder()  # module_name="config.piccolo_conf")
            await engine.close_connection_pool()
            LOGGER.info("PSQL connection closed")

        except Exception as err:
            LOGGER.error(f"PSQL close w/error: {err}")