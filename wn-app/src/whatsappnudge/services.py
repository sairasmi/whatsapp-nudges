import requests
import datetime
import json
from config import settings

from logger import log

async def sent_whastApp_message(mobile, nudge):
    try:        
        url = settings.WHATSAPP_MSG_SENT_API
        log.info("sent_whastApp_message to {0} - {1}".format(mobile, nudge))

        if not nudge:
            nudge = "Pest Incidence"

        payload = json.dumps({
            "sender": f"91{mobile}",
            "message": nudge
        })

        headers = {
            'Authorization': settings.WHATSAPP_MSG_SENT_TOKEN,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        
        if response.status_code==200:
            log.info("Response from {0} | with inputs - {1} | Response code - {2}".format(url, payload, response.status_code))

            return response.json()
        else:
            log.info("Response from {0} | with inputs - {1} | Response - {2}: {3}".format(url, payload, response.status_code, response.text))
            
            return False
    except Exception as e:
        log.error('Error in sent_whastApp_message')
        log.error(e)





async def get_whatsapp_message_history(vendor_username, fetch_date):
    try:
        url = settings.WHASTAPP_HISTORY_API

        payload = json.dumps({
            "vendor_username": vendor_username,
            "start_date": str(fetch_date),
            "end_date": str(fetch_date),
            "data_page_limit":10000000000
        })

        headers = {
            'Authorization': settings.WHASTAPP_HISTORY_TOKEN,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)


        if response.status_code==200:
            log.info("Response from {0} | with inputs - {1} | Response code - {2}".format(url, payload, response.status_code))
            return response.json()
        else:
            log.info("Response from {0} | with inputs - {1} | Response - {2}: {3}".format(url, payload, response.status_code, response.text))
            return False
    except Exception as e:
        log.error(e)
        log.error('Error in get_whatsapp_message_history')
