import requests
import configuration

# сессия хранит cookies (как браузер)
session = requests.Session()

def post_login(body):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = session.post(
        configuration.BASE_URL + configuration.LOGIN_PATH,
        data=body,
        headers=headers
    )

    # сервер кладёт токен в cookie Authorization
    # requests иногда не сохраняет её → кладём вручную
    if "set-cookie" in response.headers:
        raw_cookie = response.headers["set-cookie"]

        # Authorization="bearer xxx";
        token = raw_cookie.split(";")[0].split("=", 1)[1].strip('"')

        session.cookies.set("Authorization", token)

    return response


# ========================================
# CREATE CHANNEL
# ========================================
def post_create_channel(body):
    return session.post(
        configuration.BASE_URL + configuration.CHANNELS_PATH,
        json=body
    )

# ========================================
# DELETE CHANNEL
# ========================================
def delete_channel(channel_id):
    path = configuration.DELETE_CHANNEL_PATH.format(channel_id=channel_id)

    return session.delete(
        configuration.BASE_URL + path
    )

# ========================================
# GET CHANNEL
# ========================================
def get_channels(params=None):
    return session.get(
        configuration.BASE_URL + configuration.CHANNELS_PATH,
        params=params
    )

# ========================================
# GET CHANNEL by id
# ========================================
def get_channel(channel_id):
    path = configuration.CHANNEL_PATH.format(channel_id=channel_id)

    return session.get(
        configuration.BASE_URL + path
    )

# ========================================
# FPM ON
# ========================================
def post_free_play_mode(channel_id, is_free_play_mode: bool):
    return session.post(
        configuration.BASE_URL +
        configuration.CHANNELS_PATH +
        f"/{channel_id}/free-play-mode",
        json={"is_free_play_mode": is_free_play_mode}
    )

# ========================================
# Autoplay/Singleplay
# ========================================
def post_play_mode(channel_id: str, play_mode: str):
    return session.post(
        configuration.BASE_URL +
        configuration.CHANNELS_PATH +
        f"/{channel_id}/play-mode",
        json={"play_mode": play_mode}
    )

# ========================================
# Update channel (PUT)
# ========================================
def put_update_channel(channel_id: str, body: dict):
    return session.put(
        configuration.BASE_URL +
        configuration.CHANNELS_PATH +
        f"/{channel_id}",
        json=body
    )
# ========================================
# CREATE FOLDER
# ========================================
def post_create_folder(channel_id: str, body: dict):
    return session.post(
        configuration.BASE_URL +
        configuration.CHANNELS_PATH +
        f"/{channel_id}/folders",
        json=body
    )
# ========================================
# DELETE FOLDER
# ========================================
def delete_folder(channel_id, folder_id):
    path = configuration.DELETE_FOLDER_PATH.format(
        channel_id=channel_id,
        folder_id=folder_id
    )
    return session.delete(
        configuration.BASE_URL + path
    )
# ========================================
# SWAP FOLDERS POSITION
# ========================================
def post_swap_folders_position(channel_id: str, body: dict):
    return session.post(
        configuration.BASE_URL +
        configuration.CHANNELS_PATH +
        f"/{channel_id}/folders/swap-folders-position",
        json=body
    )