
import os
import grpc
from fastapi import FastAPI, Request
import uvicorn
import uuid
import asyncio
import multiprocessing as mp
import structlog
from adapters.api.v1.routes.fastapi import router as v1_router
from application.Treasury import Treasury
from adapters.grpc.procedures import treasury_pb2_grpc
from adapters.grpc.TreasuryGrpcCtrl import TreasuryGrpcCtrl
from domain.subscription.adapters.PurchaseSubsPersistence import PurchaseSubsPersistence

treasury_app = Treasury()

# Coroutines to be invoked when the event loop is shutting down.
_cleanup_coroutines = []
app = FastAPI()
app.include_router(v1_router, prefix="/v1")


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.on_event("startup")
async def startup_event() -> None:
    print("startup_event, creating indexes...")
    await PurchaseSubsPersistence.init_indexes()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    # whatever to do on shutdown
    pass


@app.middleware("http")
async def add_correlation_id_to_requests(request: Request, call_next):
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        api_rest_request_url=request.url.path,
        api_rest_request_method=request.method,
        api_rest_request_id=str(uuid.uuid4()),
    )
    return await call_next(request)


async def grpc_server() -> None:
    logger = structlog.get_logger().bind(module="GRPC")
    try:
        # mybe you want to open connections to DBs here
        
        # start grpc server
        grpc_port = '50052' if os.getenv('ENV') == 'local' else '50051'
        channel = grpc.aio.insecure_channel(f'localhost:{grpc_port}', options=[('grpc.default_encoding', 'utf-8')])
        server = grpc.aio.server(channel)
        treasury_pb2_grpc.add_TreasuryServicer_to_server(TreasuryGrpcCtrl(treasury_app), server)
        listen_addr = f'[::]:{grpc_port}'
        server.add_insecure_port(listen_addr)
        logger.info("Starting server on %s", listen_addr)
        await server.start()
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True, error=str(e), stack_trace=e.__traceback__)

    async def server_graceful_shutdown():
        logger.info("Starting graceful shutdown...")
        # Shuts down the server with 10 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        # Close DBs connections
        await treasury_app.clients_info_db.close_connection()
        await server.stop(10)

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()


def run_async_grpc_server():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(grpc_server())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()


def run_grpc_server():
    mp.set_start_method("spawn")
    p = mp.Process(target=run_async_grpc_server)  # , daemon=True)
    p.start()


if __name__ == "__main__":
    run_grpc_server()
    port = 8081 if os.getenv('ENV') == 'local' else 8080
    uvicorn.run(app, host="0.0.0.0", port=port)
