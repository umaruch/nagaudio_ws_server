from app.extensions import mpd_client


# Словарь соотношений команда-функция
routes = {
    "SET_PAUSE": mpd_client.pause,
    "SET_PLAY": mpd_client.play,
    "SET_NEXT": mpd_client.next,
    "SET_PREV": mpd_client.prev,
    "SET_REPEAT": mpd_client.repeat,
    "SET_RANDOM": mpd_client.random,
    "SET_VOLUME": mpd_client.volume,
    "SET_TIME": mpd_client.time,
    "GET_STATUS": mpd_client.status,
    "GET_PLAYLISTS": mpd_client.playlists_list,
    "GET_PLAYLIST": mpd_client.playlist_info,
    "DELETE_PLAYLIST": mpd_client.delete_playlist,
    "RENAME_PLAYLIST": mpd_client.rename_playlist,
    "SWAP": mpd_client.swap_songs,
    "DELETE": mpd_client.delete_from_playlist,
    "ADD": mpd_client.add_song_to_playlist,
    "BROWSE": mpd_client.browse_files,
    "CHANGE": mpd_client.change_playlist_or_song,
    "SAVE_PLAYLIST": mpd_client.save_playlist,
    "UPDATE": mpd_client.update_database,
    "PLAY_BROWSE": mpd_client.play_browse_files,
    "GET_DEVICE": None,
    "REBOOT": None,
    "RENAME_DEVICE": None,
    "CHANGE_PROFILES": None,
    "GET_NETWORK": None,
    "CHANGE_NETWORK": None
}
