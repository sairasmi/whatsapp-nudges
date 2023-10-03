from pydantic import BaseSettings


class Settings(BaseSettings):
    # items_per_user: int = 50
    DB_Dialect:str
    DB_Name:str
    DB_User:str
    DB_Pass:str
    DB_Host:str
    DB_Port:str
    WHATSAPP_MSG_SENT_API:str
    WHATSAPP_MSG_SENT_TOKEN:str
    WHASTAPP_HISTORY_API:str
    WHASTAPP_HISTORY_TOKEN:str
    SEPARATOR:str
    LOGGER_INTERVAL_VALUE:int
    LOGGER_INTERVAL_UNIT:str
    LOGGER_BACKUP_COUNT:int
    SCHEDULER_TIME_HOUR_HISTORY_API:int
    SCHEDULER_TIME_MINUTE_HISTORY_API:int
    SCHEDULER_TIME_MINUTE_BULK_SENT_API:int

    class Config:
        env_file = ".env"


# global instance
settings = Settings()