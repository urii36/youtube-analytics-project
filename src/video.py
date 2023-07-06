import os

from googleapiclient.discovery import build

from src.channel import Channel


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)


    def __init__(self, video_id: str):
        """
        Инициализация класса Video
        """
        self.video_id = video_id
        youtube = Channel.get_service().videos().list(
            part = 'snippet, statistics', id = self.video_id
        ).execute()
        video_data = youtube.get('items')[0]
        self.__title = video_data.get('snippet').get('title')
        self.__url = f'https://www.youtube.com/watch?v{self.channel_id}'
        self.__view_count = int(video_data.get('statistics').get('viewCount'))
        self.__like_count = int(video_data.get('statistics').get('likeCount'))

    def __str__(self):
        return self.__title

    @property
    def video_id(self) -> str:
        """str: Геттер для идентификатора видео."""
        return self.__video_id

    @video_id.setter
    def video_id(self, value) -> None:
        """str: Cеттер для идентификатора видео."""
        self.__video_id = value


class PLVideo(Video):
    """ Инициализация наследоваемого класса PLVideo """

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id

