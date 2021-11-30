from logging import config, getLogger
import time
import random
import string

from fastapi import FastAPI, Request

from app.routers import users, stocks, health

config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = getLogger(__name__)
app = FastAPI()

app.include_router(users.router)
app.include_router(stocks.router)
app.include_router(health.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits,
                   k=10))
    logger.info(f"{request.client.host} - ID={idem} "
                f"start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"{request.client.host} - ID={idem} "
                f"completed_in={formatted_process_time}ms "
                f"status_code={response.status_code}")

    return response

logger.info("Server started")
