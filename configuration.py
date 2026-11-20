BASE_URL = "https://dev.vrvr-dev.ru"

LOGIN_PATH = "/api/auth/login"
UI_LOGIN_URL = BASE_URL + "/auth/login"

CHANNELS_PATH = "/api/channels"                    # POST, GET list
DELETE_CHANNEL_PATH = "/api/channels/{channel_id}" # DELETE
CHANNEL_PATH = "/api/channels/{channel_id}"        # GET 
UPDATE_CHANNEL_PATH = "/api/channels/{channel_id}" # PUT

DELETE_FOLDER_PATH = "/api/channels/{channel_id}/folders/{folder_id}"  # DELETE
