from fastapi import APIRouter, UploadFile, Form, File, Depends, Request

from sqlalchemy.orm import Session
from db import get_db
from whatsappnudge import controllers, schemas
from whatsappnudge.utils import Response
import datetime
from typing import List,Optional

from logger import log


wn = APIRouter()


@wn.get("/test")
def test():
    return {"hello": "world"}

@wn.get("/nudges")
async def get_nudges(db: Session = Depends(get_db)):
    try:
        log.info("API - /nudges")
        res = await controllers.get_nudges(db)

        log.info("API - /nudges | success")
        if res:
            return Response(res, 200)

        return Response([], 200, True, "Data not exist")
    except Exception as e:
        log.info("API - /nudges | error")
        log.error("Error in get_nudges route")
        log.error(e)
        return Response('error', 500, False, "Server error")



@wn.get("/directorate")
async def get_directorate(db: Session = Depends(get_db)):
    try:
        log.info("API - /directorate")
        res = await controllers.get_distinct_directorate(db)

        log.info("API - /directorate | success")
        if res:
            return Response(res, 200)
        
        return Response([], 200, True, "Data not exist")
    except Exception as e:
        log.info("API - /directorate | error")
        log.error("Error in get_directorate route")
        log.error(e)
        return Response('error', 500, False, "Server error")


@wn.get("/designations")
async def get_designations(directorate: str, db: Session = Depends(get_db)):
    try:
        log.info("API - /designations?directorate={0}".format(directorate))

        res = await controllers.get_distinct_designations_by_directorate(db, directorate)

        log.info("API - /designations?directorate={0} | success".format(directorate))
        if res:
            return Response(res, 200)

        return Response([], 200, True, "Data not exist")
    except Exception as e:
        log.info("API - /designations?directorate={0} | error".format(directorate))

        log.error("Error in get_designations route")
        log.error(e)
        return Response('error', 500, False, "Server error")


@wn.get("/districts")
async def get_districts(directorate: str, designation: str, db: Session = Depends(get_db)):
    try:
        log.info("API - /districts?directorate={0}&designation={1}".format(directorate, designation))

        res = await controllers.get_distinct_districts_by_directorate_and_designation(db, directorate, designation)

        log.info("API - /districts?directorate={0}&designation={1} | success".format(directorate, designation))
        if res:
            return Response(res, 200)

        return Response([], 200, True, "Data not exist")
    except Exception as e:
        log.info("API - /districts?directorate={0}&designation={1} | error".format(directorate, designation))

        log.error("Error in get_districts route")
        log.error(e)
        return Response('error', 500, False, "Server error")


@wn.post("/sent")
async def sent_message_single_mobile(payload: schemas.SingleSent, db: Session = Depends(get_db)):
    try:
        log.info("API - /sent")
        log.info("Inputs: mobile - {0}, nudge - {1}".format(payload.mobile, payload.nudge))
           
        res = await controllers.sent_message_single_mobile(db, payload.mobile, payload.nudge)
        if res:
            log.info("API - /sent | success")
            return Response(res, 200, True, "Message sent successfully.")
        else:
            log.info("API - /sent | failed")
            return Response(False, 500, False, "Message not able to sent.")
    except Exception as e:
        log.info("API - /sent | error")

        log.error("Error in sent_message_single_mobile route")
        log.error(e)
        return Response('error', 500, False, "Server error")


@wn.post("/sent-bulk")
async def sent_message_bulk(payload: schemas.BulkSent, db: Session = Depends(get_db)):
    try:
        log.info("API - /sent-bulk")
        log.info("Inputs: nudge - {0}, directorate - {1}, district - {2}, designation - {3}".format(payload.nudge, payload.directorate, payload.district, payload.designation))

        res = await controllers.sent_message_bulk(db, payload)
        if res:
            log.info("API - /sent-bulk | success")
            return Response(res, 200, True, "Event logged successfully. Sending process will initiate within 2 min.")
        else:
            log.info("API - /sent-bulk | failed")
            return Response(False, 500, False, "Message not able to sent.")
    except Exception as e:
        log.info("API - /sent-bulk | error")
        log.error("Error in sent_message_bulk route")
        log.error(e)
        return Response('error', 500, False, "Server error")



@wn.post("/whatsapp-history-manually")
async def get_whatsapp_history_manually(payload: schemas.WhatsAppHistoryManually, db: Session = Depends(get_db)):
    try:
        await controllers.get_whatsapp_history_manually(db, payload)
        return Response(True, 200)
    except Exception as e:
        log.info("API - /get-whatsapp-history-manually | error")
        log.error("Error in get_whatsapp_history_manually route")
        log.error(e)
        return Response('error', 500, False, "Server error")
