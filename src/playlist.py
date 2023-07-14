from src.channel import Channel
from datetime import timedelta


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str):

        """
        Инициализация класса PlayList

        """
        self.playlist_id = playlist_id
        self._response = self.youtube.playlists().list(part="snippet,contentDetails", id=self.playlist_id).execute()
        self.title_list = self._response["items"][0]["snippet"]["title"]
        self.url_list = f"https://www.youtube.com/playlist?list={playlist_id}"

    @property
    def total_duration(self) -> datetime.timedelta:
        """Возвращает общую длительность плейлиста.
        Returns:
            timedelta: Общая длительность плейлиста.
        """
        response = self.videos
        duration = datetime.timedelta()
        for item in response["items"]:
            duration += isodate.parse_duration(item["contentDetails"]["duration"])
        return duration

    @property
    def videos(self):
        """
        Метод возвращает список видео из плейлиста

        """
        response = self.youtube.playlistItems().list(part="contentDetails", playlistId=self.playlist_id).execute()
        video_id = []
        for item in response["items"]:
            video_id.append(item["contentDetails"]["videoId"])

        response = self.youtube.videos().list(part='contentDetails,statistics',
                                              id=','.join(video_id)
                                              ).execute()
        return response

    def show_best_video(self) -> str:
        """
        метод возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)

        """
        response = self.videos
        movie = max(response["items"], key=lambda x: int(x["statistics"]["likeCount"]))
        return f"https://youtu.be/{movie['id']}"