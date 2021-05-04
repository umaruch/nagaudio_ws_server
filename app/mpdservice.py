"""
Сервис, отвечающий за управление плеером MPD, и только за него

Статус: вроде закончено, нужно только доделать обработку ошибок
"""
import json
from mpd.asyncio import MPDClient, CommandError


class MPDService:
    def __init__(self, host, port):
        self.host, self.port = host, port
        self.client = MPDClient()

    async def play(self, args_dict=None):
        await self.client.play()

    async def pause(self, args_dict=None):
        await self.client.pause()

    async def next(self, args_dict=None):
        try:
            await self.client.next()
        except CommandError:
            await self.client.play(0)

    async def prev(self, args_dict=None):
        try:
            await self.client.previous()
        except CommandError:
            await self.client.play(0)

    async def volume(self, args_dict=None):
        await self.client.setvol(args_dict["value"])

    async def time(self, args_dict=None):
        await self.client.seekcur(args_dict["value"])

    async def random(self, args_dict=None):
        await self.client.random(args_dict["value"])

    async def repeat(self, args_dict=None):
        value = args_dict["value"]
        if value == 0:
            await self.client.repeat(0)
            await self.client.single(0)
        if value == 1:
            await self.client.repeat(1)
            await self.client.single(0)
        if value == 2:
            await self.client.repeat(1)
            await self.client.single(1)

    async def _full_status(self, args_dict=None):
        # Получение полного статуса, включающего в себя статус плеера и текущий плейлист
        current_playlist = await self.client.playlistinfo()
        status = await self.client.status()
        return {
            "cmd": "GET_FULL",
            "data": {
                "status": status,
                "playlist": current_playlist,
            }
        }

    async def status(self, args_dict=None):
        # Получение текущего статуса плеера
        status = await self.client.status()
        return {
            "cmd": "GET_STATUS",
            "data": status
        }

    async def stats(self):
        # Получение статистики работы плеера
        return await self.client.stats()

    async def playlists_list(self, args_dict=None):
        # Получение списка плейлистов
        playlists = await self.client.listplaylists()
        return {
            "cmd": "GET_PLAYLISTS",
            "data": playlists
        }

    async def playlist_info(self, args_dict=None):
        # Получение информации о любом из плейлистов
        name = args_dict["name"]
        if name == "current":
            playlist_info = await self.client.playlistinfo()
        else:
            playlist_info = await self.client.listplaylistinfo(name)

        return {
            "cmd": "GET_PLAYLIST",
            "data": playlist_info
        }

    async def delete_playlist(self, args_dict=None):
        # Удаление выбранного плейлиста
        name = args_dict["name"]
        await self.client.rm(name)
        return {
            "cmd": "DELETE_PLAYLIST",
            "status": 1
        }

    async def rename_playlist(self, args_dict=None):
        # Переименование сохраненного плейлиста
        current_name = args_dict["currentname"]
        new_name = args_dict["newname"]
        await self.client.rename(current_name, new_name)
        return {
            "cmd": "RENAME",
            "status": 1
        }

    async def swap_songs(self, args_dict=None):
        # Перемещение треков в плейлисте местами
        playlist_name = args_dict.get("name", None)
        pos_1 = args_dict["pos1"]
        pos_2 = args_dict["pos2"]
        if playlist_name:
            await self.client.playlistmove(playlist_name, pos_1, pos_2)
        else:
            await self.client.swap(pos_1, pos_2)

        return {
            "cmd": "SWAP",
            "status": 1
        }

    async def delete_from_playlist(self, args_dict=None):
        # Удаление трека из плейлиста по его позиции
        playlist_name = args_dict.get("name", None)
        pos = args_dict["pos"]

        if playlist_name:
            await self.client.playlistdelete(playlist_name, pos)
        else:
            await self.client.delete(pos)

        return {
            "cmd": "DELETE",
            "status": 1
        }

    async def add_song_to_playlist(self, args_dict=None):
        # Добавление трека в плейлист
        playlist_name = args_dict.get("name", None)
        file_uri = args_dict.get["path"]

        if playlist_name:
            await self.client.playlistadd(playlist_name, file_uri)
        else:
            await self.client.add(file_uri)

        return {
            "cmd": "ADD",
            "status": 1
        }

    async def change_playlist_or_song(self, args_dict=None):
        # Смена текущего трека или плейлиста
        playlist_name = args_dict.get("name", None)
        pos = args_dict.get("pos", None)

        if not playlist_name:
            await self.client.play(pos)
        else:
            await self.client.clear()
            await self.client.load(playlist_name)
            if not pos:
                await self.client.play()
            else:
                await self.client.play(pos)

        return {
            "cmd": "CHANGE",
            "status": 1
        }

    async def save_playlist(self, args_dict=None):
        # Сохранить текущий список воспроизведения в плейлист
        playlist_name = args_dict.get["name"]

        await self.client.save(playlist_name)

        return {
            "cmd": "SAVE_PLAYLIST",
            "status": 1
        }

    async def browse_files(self, args_dict=None):
        # Просмотр файловой системы устройства
        dir_uri = args_dict.get("path", None)
        if dir_uri:
            data = await self.client.lsinfo(dir_uri)
        else:
            data = await self.client.lsinfo()

        return {
            "cmd": "BROWSE",
            "data": data
        }

    async def update_database(self, args_dict=None):
        # Обновление базы данных mpd
        await self.client.update()

        return {
            "cmd": "UPDATE",
            "status": 1
        }

    async def play_browse_files(self, args_dict=None):
        uri = args_dict["path"]
        await self.client.clear()
        await self.client.add(uri)
        await self.client.play()

        return {
            "cmd": "PLAY_BROWSE",
            "status": 1
        }
