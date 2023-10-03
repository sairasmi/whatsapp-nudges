import os


def Response(data, status_code, success=True, message="OK"):
    data = {
        "success" : success,
        "error" : not success,
        "message": message,
        "data" : data,
        "status_code" : status_code,
    }
    return data

def get_list_mobiles_from_string(mobile_list: str, separator: str):
    if not mobile_list:
        return []
    mobile_list = mobile_list.split(f"{separator}")
    if not mobile_list:
        return []
    return map(lambda v: v.strip(), mobile_list)
    

def create_folder(folder_path):
    try:
        os.mkdir(folder_path)
    except Exception as e:
        pass
