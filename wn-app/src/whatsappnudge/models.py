import datetime
from typing import BinaryIO, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, Boolean, BigInteger, ForeignKey, Text, JSON
from sqlalchemy.sql.sqltypes import DATE

from db import Base


class Nudges(Base):
    __tablename__       = 'nudges'

    id                  = Column(Integer, primary_key=True, index=True)
    name                = Column(String(255), nullable=False)
    nudge_identifier    = Column(String(255), nullable=False)
    isActive            = Column(Boolean, default=True, nullable=False)
    created_at          = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at          = Column(DateTime, default=datetime.datetime.now, nullable=False)



class BlockContactInfo(Base):
    __tablename__       = 't_block_wise_official_contact_info'

    int_id              = Column(Integer, primary_key=True, index=True)
    vch_username        = Column(String(255), nullable=True)
    vch_official_name   = Column(String(255), nullable=True)
    vch_phone_no        = Column(String(10), nullable=True)
    vch_Block           = Column(String(60), nullable=True)
    vch_District        = Column(String(60), nullable=True)
    en_department       = Column(String(60), nullable=True)
    vch_designation     = Column(String(255), nullable=True)
    created_at          = Column(DateTime, default=datetime.datetime.now, nullable=True)
    updated_at          = Column(DateTime, default=datetime.datetime.now, nullable=True)
    deleted_at          = Column(DateTime, default=datetime.datetime.now, nullable=True)



class MessageLog(Base):
    __tablename__       = 'message_log'

    id                  = Column(Integer, primary_key=True, index=True)
    mobile              = Column(String(10), nullable=False)
    nudge               = Column(String(255), nullable=False)
    status              = Column(String(20), nullable=False) ## pending, success, failed
    description         = Column(String(255), nullable=True)
    sent_at             = Column(DateTime, default=None, nullable=True)
    created_at          = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at          = Column(DateTime, default=datetime.datetime.now, nullable=False)



class MessageHistory(Base):
    __tablename__       = 'message_history'

    id                          = Column(Integer, primary_key=True, index=True)
    vendor_username             = Column(String(10), nullable=True)
    fetch_date                  = Column(DATE, nullable=True)
    mobile                      = Column(String(10), nullable=False)
    customer_name               = Column(String(255), nullable=True)
    promt_topic                 = Column(String(255), nullable=True)
    first_promt_responses       = Column(String(255), nullable=True)
    second_promt_responses      = Column(String(255), nullable=True)
    third_promt_responses       = Column(String(255), nullable=True)

    rating                      = Column(String(255), nullable=True)
    address                     = Column(String(255), nullable=True)
    request_about               = Column(String(255), nullable=True)
    request_type                = Column(String(255), nullable=True)
    feedback                    = Column(String(255), nullable=True)
    orig_message_created_at     = Column(DateTime, nullable=True)
    
    created_at                  = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at                  = Column(DateTime, default=datetime.datetime.now, nullable=False)



class CronJobLog(Base):
    __tablename__       = 'cron_job_log'

    id                  = Column(Integer, primary_key=True, index=True)
    job_type            = Column(String(20), nullable=False) #message-sent, message-history
    job_status          = Column(String(20), nullable=False)
    job_description     = Column(String(255), nullable=True)
    job_completed_at    = Column(DateTime, default=None, nullable=True)
    created_at          = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at          = Column(DateTime, default=datetime.datetime.now, nullable=False)