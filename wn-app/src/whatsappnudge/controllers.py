import json
import datetime
from config import settings
import os
from whatsappnudge import models, services, constants

from sqlalchemy.orm import (
    Session,
    load_only,
    lazyload,
    joinedload,
    subqueryload,
    selectinload,
)
from sqlalchemy import asc, desc, and_, func, or_
from fastapi import FastAPI, HTTPException
from whatsappnudge.utils import get_list_mobiles_from_string
from whatsappnudge.cron import get_history_data

from logger import log


async def get_nudges(db: Session):
    log.info("get_nudges")
    nudges_res = db.query(models.Nudges.name).all()
    res = []
    for data in nudges_res:
        res.append(data.name)
    return res


async def get_distinct_directorate(db: Session):
    log.info("get_distinct_directorate")

    depart_res = db.query(models.BlockContactInfo.en_department).distinct().all()
    res = []
    for depart in depart_res:
        res.append(depart.en_department)
    return res


async def get_distinct_designations_by_directorate(db: Session, directorate):
    log.info("get_distinct_designations_by_directorate")
    log.info("input request -> {0}".format(directorate))

    ## get all the directorate values
    directorateList = directorate.split(",")
    designation_res = (
        db.query(models.BlockContactInfo.vch_designation)
        .filter(models.BlockContactInfo.en_department.in_(directorateList))
        .distinct()
        .all()
    )

    res = []
    for designation in designation_res:
        res.append(designation.vch_designation)

    return res


async def get_distinct_districts_by_directorate_and_designation(
    db: Session, directorate, designation
):
    log.info("get_distinct_districts_by_directorate_and_designation")
    log.info(
        "input request -> directorate={0} & designation={1}".format(
            directorate, designation
        )
    )

    ## get all the directorate values
    directorateList = directorate.split(",")
    designationList = designation.split(",")

    districts_res = (
        db.query(models.BlockContactInfo.vch_District)
        .filter(
            models.BlockContactInfo.en_department.in_(directorateList),
            models.BlockContactInfo.vch_designation.in_(designationList),
        )
        .distinct()
        .all()
    )

    res = []
    for district in districts_res:
        res.append(district.vch_District)

    return res


# single message sent
async def sent_message_single_mobile(db: Session, mobile: str, nudge: str):
    mobile_list = get_list_mobiles_from_string(mobile, settings.SEPARATOR)
    log.info("sent_message_single_mobile")
    if mobile_list:
        for mobile in mobile_list:
            whatsapp_res = await services.sent_whastApp_message(mobile, nudge)
            if whatsapp_res:
                await log_message_sent(
                    db,
                    mobile,
                    nudge,
                    constants.MESSAGE_SENT_LOG_STATUS["SUCCESS"],
                    constants.MESSAGES["MESSAGE_SENT_SUCCESS"],
                    datetime.datetime.now(),
                )
            else:
                await log_message_sent(
                    db,
                    mobile,
                    nudge,
                    constants.MESSAGE_SENT_LOG_STATUS["FAILED"],
                    constants.MESSAGES["MESSAGE_SENT_FAILED"],
                    datetime.datetime.now(),
                )
        return True

    return False


# bulk msg sent
async def sent_message_bulk(db: Session, payload):
    log.info("sent_message_bulk")

    # get mobile numbers
    mobile_number_list = []
    mobile_number_list = await get_mobiles_based_on_all_filters(db, payload)

    log.info("sent_message_bulk - mobile list length: ".format(len(mobile_number_list)))

    if mobile_number_list:
        for mobile in mobile_number_list:
            await log_message_sent(
                db,
                mobile,
                payload.nudge,
                constants.MESSAGE_SENT_LOG_STATUS["PENDING"],
                constants.MESSAGES["MESSAGE_SENT_PENDING"],
                None,
            )
    return True


# get mobile numbers based on directorate, designation, district
async def get_mobiles_based_on_all_filters(db: Session, payload):
    log.info("get_mobiles_based_on_all_filters")

    ## get all the directorate values
    directorateList = payload.directorate.split(",")
    designationList = payload.designation.split(",")
    districtList = payload.district.split(",")
    
    mobile_res = (
        db.query(models.BlockContactInfo.vch_phone_no)
        .filter(
            models.BlockContactInfo.en_department.in_(directorateList),
            models.BlockContactInfo.vch_designation.in_(designationList),
            models.BlockContactInfo.vch_District.in_(districtList),
        )
        .distinct()
        .all()
    )
    
    # print(mobile_res)
    res = []
    for data in mobile_res:
        res.append(data.vch_phone_no)
    return res


async def log_message_sent(
    db: Session, mobile, nudge, status, description, sent_at=None
):
    log.info("log_message_sent: message sent has been logged")
    msg_log_obj = models.MessageLog(
        mobile=mobile,
        nudge=nudge,
        status=status,
        description=description,
        sent_at=sent_at,
    )
    db.add(msg_log_obj)
    db.commit()
    db.refresh(msg_log_obj)
    return msg_log_obj


async def get_whatsapp_history_manually(db: Session, payload):
    log.info(
        "get_whatsapp_history_manually | start_date - {0}, end_date - {1}".format(
            payload.start_date, payload.end_date
        )
    )

    start_date = datetime.datetime.strptime(payload.start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(payload.end_date, "%Y-%m-%d")

    delta = datetime.timedelta(days=1)  # difference between current and previous date

    while start_date <= end_date:
        log.info("Fetching WhatsAPP history for - {0}".format(str(start_date.date())))

        # get whatsapp history
        vendor_username = "OCAC"
        fetch_date = start_date.date()

        whatsapp_history_res = await services.get_whatsapp_message_history(
            vendor_username, fetch_date
        )
        if whatsapp_history_res:
            for history_data in whatsapp_history_res["results"]:
                mobile = history_data["Phone Number"][2:]

                msg_history_obj = await get_history_data(
                    vendor_username, fetch_date, mobile
                )
                if msg_history_obj:
                    # if already exists, update
                    log.info("Data already exist, so updated on table")

                    msg_history_obj.customer_name = (history_data["Customer Name"],)
                    msg_history_obj.promt_topic = (history_data["Prompt Topic"],)
                    msg_history_obj.first_promt_responses = (
                        history_data["First Prompt Responses"],
                    )
                    msg_history_obj.second_promt_responses = (
                        history_data["Second Prompt Responses"],
                    )
                    msg_history_obj.third_promt_responses = (
                        history_data["Third Prompt Responses"],
                    )
                    msg_history_obj.rating = (history_data["Rating"],)
                    msg_history_obj.address = (history_data["Address"],)
                    msg_history_obj.request_about = (history_data["Request About"],)
                    msg_history_obj.request_type = (history_data["Request Type"],)
                    msg_history_obj.feedback = (history_data["Feedback"],)
                    msg_history_obj.orig_message_created_at = (
                        datetime.datetime.strptime(
                            history_data["Date Created"], "%b %d %Y %I:%M:%S %p"
                        )
                    )
                    msg_history_obj.updated_at = datetime.datetime.now()

                    db.commit()
                    db.refresh(msg_history_obj)
                else:
                    # else, create
                    log.info("Data not exist, so created")

                    msg_history_obj = models.MessageHistory(
                        vendor_username=vendor_username,
                        fetch_date=fetch_date,
                        mobile=mobile,
                        customer_name=history_data["Customer Name"],
                        promt_topic=history_data["Prompt Topic"],
                        first_promt_responses=history_data["First Prompt Responses"],
                        second_promt_responses=history_data["Second Prompt Responses"],
                        third_promt_responses=history_data["Third Prompt Responses"],
                        rating=history_data["Rating"],
                        address=history_data["Address"],
                        request_about=history_data["Request About"],
                        request_type=history_data["Request Type"],
                        feedback=history_data["Feedback"],
                        orig_message_created_at=datetime.datetime.strptime(
                            history_data["Date Created"], "%b %d %Y %I:%M:%S %p"
                        ),
                    )
                    db.add(msg_history_obj)
                    db.commit()
                    db.refresh(msg_history_obj)
        start_date += delta  # increment start date by timedelta

    return True
