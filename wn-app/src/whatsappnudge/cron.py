import json
import datetime
from config import settings
import os
from whatsappnudge import models, services, constants, controllers

from sqlalchemy.orm import Session, load_only, lazyload, joinedload, subqueryload, selectinload, sessionmaker
from sqlalchemy import asc, desc, and_, func, or_
from fastapi import FastAPI, HTTPException, APIRouter, UploadFile, Form, File, Depends, Request
from fastapi_utils.tasks import repeat_every

from logger import log

from db import engine, get_db
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()




''' ******************** CRON JOB for Message sent ******************** '''

async def cron_job_whatsapp_message_sent_bulk():
    log.info('*cron_job_whatsapp_message_sent_bulk STARTED')
    # log cron job
    cron_job_log_obj = await log_cron_job({'job_type': constants.CRON_JOB_TYPE["MESSAGE_SENT"]})

    try:
        # fetch mobile numbers
        msg_logs = session.query(models.MessageLog).filter(
            models.MessageLog.status == constants.MESSAGE_SENT_LOG_STATUS["PENDING"]
        ).order_by(models.MessageLog.created_at.desc()).all()

        log.info("Total mobile to sent whatsApp msg: {0}".format(len(msg_logs)))

        for msg in msg_logs:
            # sent whatsapp messages
            whatsapp_res = await services.sent_whastApp_message(msg.mobile, msg.nudge)
            if whatsapp_res:
                await update_status_log_message_sent(msg.mobile, constants.MESSAGE_SENT_LOG_STATUS["SUCCESS"], constants.MESSAGES["MESSAGE_SENT_SUCCESS"])
            else:
                await update_status_log_message_sent(msg.mobile, constants.MESSAGE_SENT_LOG_STATUS["FAILED"], constants.MESSAGES["MESSAGE_SENT_FAILED"])

        # update cron job status
        await update_cron_job_log_status({'job_id': cron_job_log_obj.id, 'job_status':constants.CRON_JOB_STATUS["COMPLETED"],})


        return True
    except Exception as e:
        # update cron job status - failed
        await update_cron_job_log_status({'job_id': cron_job_log_obj.id, 'job_status':constants.CRON_JOB_STATUS["FAILED"],})
        session.rollback()
        log.error('Error in cron_job_whatsapp_message_sent_bulk')
        log.error(e)
        return False
    finally:
        session.close()
        log.info('*cron_job_whatsapp_message_sent_bulk FINISHED')




async def update_status_log_message_sent(mobile, status, description):
    try:
        msg_log_obj = session.query(models.MessageLog).filter(models.MessageLog.mobile == mobile)
        if msg_log_obj:
            msg_log_obj.update(
                {
                    models.MessageLog.status: status, 
                    models.MessageLog.description: description,
                    models.MessageLog.sent_at: datetime.datetime.now(),
                    models.MessageLog.updated_at: datetime.datetime.now(),
                }, 
                synchronize_session="fetch"
            )
            session.commit()
        log.info("sent_whastApp_message status updated on table")
        return True
    except Exception as e:
        session.rollback()
        log.error('Error in update_status_log_message_sent')
        log.error(e)
        return False






''' ******************** CRON JOB for Message History ******************** '''


async def cron_job_whatsapp_message_history():
    log.info('**cron_job_whatsapp_message_history STARTED')
    # log cron job
    cron_job_log_obj = await log_cron_job({'job_type': constants.CRON_JOB_TYPE["MESSAGE_HISTORY"]})

    try:
        # get whatsapp history
        vendor_username = "OCAC"
        fetch_date = (datetime.datetime.now() + datetime.timedelta(-1)).date() #fetch date should be yesterday date

        whatsapp_history_res = await services.get_whatsapp_message_history(vendor_username, fetch_date)
        if whatsapp_history_res:
            for history_data in whatsapp_history_res["results"]:
                mobile = history_data["Phone Number"][2:]
                
                msg_history_obj = await get_history_data(vendor_username, fetch_date, mobile)
                if msg_history_obj:
                    # if already exists, update
                    log.info('Data already exist, so updated on table')

                    msg_history_obj.customer_name = history_data["Customer Name"], 
                    msg_history_obj.promt_topic = history_data["Prompt Topic"], 
                    msg_history_obj.first_promt_responses = history_data["First Prompt Responses"], 
                    msg_history_obj.second_promt_responses = history_data["Second Prompt Responses"], 
                    msg_history_obj.third_promt_responses = history_data["Third Prompt Responses"], 
                    msg_history_obj.rating = history_data["Rating"], 
                    msg_history_obj.address = history_data["Address"], 
                    msg_history_obj.request_about = history_data["Request About"], 
                    msg_history_obj.request_type = history_data["Request Type"],
                    msg_history_obj.feedback = history_data["Feedback"],
                    msg_history_obj.orig_message_created_at = datetime.datetime.strptime(history_data["Date Created"], '%b %d %Y %I:%M:%S %p')
                    msg_history_obj.updated_at=datetime.datetime.now()

                    session.commit()
                    session.refresh(msg_history_obj)
                else:
                    #else, create
                    log.info('Data not exist, so created')

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
                        orig_message_created_at=datetime.datetime.strptime(history_data["Date Created"], '%b %d %Y %I:%M:%S %p')
                    )
                    session.add(msg_history_obj)
                    session.commit()
                    session.refresh(msg_history_obj)

        # update cron job status - success
        await update_cron_job_log_status({'job_id': cron_job_log_obj.id, 'job_status':constants.CRON_JOB_STATUS["COMPLETED"],})

        return True
    except Exception as e:
        # update cron job status - failed
        await update_cron_job_log_status({'job_id': cron_job_log_obj.id, 'job_status':constants.CRON_JOB_STATUS["FAILED"],})
        session.rollback()
        log.error('Error in cron_job_whatsapp_message_history')
        log.error(e)
        return False
    finally:
        session.close()
        log.info('**cron_job_whatsapp_message_history FINISHED')



async def get_history_data(vendor_username, fetch_date, mobile):
    log.info("get_history_data - {0} | {1} | {2}".format(vendor_username, fetch_date, mobile))
    nudges_res = session.query(models.MessageHistory).filter(
        models.MessageHistory.vendor_username == vendor_username,
        models.MessageHistory.fetch_date == fetch_date,
        models.MessageHistory.mobile == mobile
    ).first()
    return nudges_res




''' ******************** LOG and UPDATE ******************** '''

async def log_cron_job(data):
    try:
        
        cron_job_log_obj = models.CronJobLog(
            job_type=data["job_type"], 
            job_status=constants.CRON_JOB_STATUS["RUNNING"],
            job_description=constants.MESSAGES["DESCRIPTION_CRON_JOB_RUNNING"],
        )
        session.add(cron_job_log_obj)
        session.commit()
        session.refresh(cron_job_log_obj)
        

        log.info("log_cron_job: job_type -> {0}, status -> {1}, job_description -> {2}".format(data["job_type"], constants.CRON_JOB_STATUS["RUNNING"], constants.MESSAGES["DESCRIPTION_CRON_JOB_RUNNING"]))

        return cron_job_log_obj
    except Exception as e:
        session.rollback()
        log.error('Error in log_cron_job')
        log.error(e)
        return False


async def update_cron_job_log_status(data):
    try:
        cron_job_log_obj = session.query(models.CronJobLog).filter(models.CronJobLog.id == data["job_id"])
        if cron_job_log_obj:
            cron_job_log_obj.update(
                {
                    models.CronJobLog.job_status: data["job_status"], 
                    models.CronJobLog.job_description: constants.MESSAGES["DESCRIPTION_CRON_JOB_COMPLETED"],
                    models.CronJobLog.job_completed_at: datetime.datetime.now(),
                    models.CronJobLog.updated_at: datetime.datetime.now(),
                }, 
                synchronize_session="fetch"
            )
            session.commit()

        log.info("update_cron_job_log_status: job_id -> {0}, status -> {1}, job_description -> {2}".format(data["job_id"], data["job_status"], constants.MESSAGES["DESCRIPTION_CRON_JOB_COMPLETED"]))

        return True
    except Exception as e:
        session.rollback()
        log.error('Error in update_cron_job_log_status')
        log.error(e)
        return False


