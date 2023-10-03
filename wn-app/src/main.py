from fastapi import FastAPI, Depends
from config import settings
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from db import database, Base, engine, metadata

from whatsappnudge.router import wn
from whatsappnudge.cron import cron_job_whatsapp_message_sent_bulk, cron_job_whatsapp_message_history
from db import get_db
from sqlalchemy.orm import Session

from apscheduler.schedulers.asyncio import AsyncIOScheduler



from logger import log
log.info("............... APPLICATION STARTED ...............")


Base.metadata.create_all(engine)
app = FastAPI()


# schedule cron jobs
scheduler = AsyncIOScheduler()
scheduler.add_job(cron_job_whatsapp_message_history, 'cron', hour=settings.SCHEDULER_TIME_HOUR_HISTORY_API, minute=settings.SCHEDULER_TIME_MINUTE_HISTORY_API)

scheduler.add_job(cron_job_whatsapp_message_sent_bulk, 'cron', minute=f"*/{str(settings.SCHEDULER_TIME_MINUTE_BULK_SENT_API)}")
scheduler.start()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(content=exc.detail, status_code=200)

app.include_router(wn, prefix= '/wn', tags=["WN"])
