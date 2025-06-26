import os
import json
from pathlib import Path
from datetime import datetime
import yt_dlp

class YouTubeChannelDownloader:
    def __init__(self, download_dir="./downloads"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        self.db_file = self.download_dir / "downloaded_videos.json"
        self.downloaded_videos = self._load_downloaded_videos()
        
    def _load_downloaded_videos(self):
        """Loads the list of already downloaded videos"""
        if self.db_file.exists():
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading database: {e}")
                return {}
        return {}
    
    def _save_downloaded_videos(self):
        """Saves the list of downloaded videos"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.downloaded_videos, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Error saving database: {e}")
    
    def _add_downloaded_video(self, video_id, video_info):
        """Adds a video to the list of downloaded videos"""
        channel_id = video_info.get('channel_id', 'unknown')
        if channel_id not in self.downloaded_videos:
            self.downloaded_videos[channel_id] = {}
        
        self.downloaded_videos[channel_id][video_id] = {
            'title': video_info.get('title', ''),
            'upload_date': video_info.get('upload_date', ''),
            'downloaded_at': datetime.now().isoformat(),
            'duration': video_info.get('duration', 0)
        }
        self._save_downloaded_videos()
    
    def get_channel_videos(self, channel_url, max_videos=None):
        """Gets the complete list of channel videos"""
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'ignoreerrors': True,
        }
        
        if max_videos:
            ydl_opts['playlistend'] = max_videos
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(channel_url, download=False)
                return info
        except Exception as e:
            print(f"❌ Error getting video list: {e}")
            return None
    
    def filter_new_videos(self, channel_info):
        """Filters only new videos that have not yet been downloaded"""
        if not channel_info or 'entries' not in channel_info:
            return []
        
        channel_id = channel_info.get('channel_id', channel_info.get('id', 'unknown'))
        downloaded_for_channel = self.downloaded_videos.get(channel_id, {})
        
        new_videos = []
        for video in channel_info['entries'][0]['entries']:
            if video and video.get('id'):
                video_id = video['id']
                if video_id not in downloaded_for_channel:
                    new_videos.append(video)
        return new_videos

    def configure_ydl_opts(self, audio_only=False, max_videos=None):
        """Configures yt-dlp options"""

        format_selector = 'best[height<=1080]'
        outtmpl = str(self.download_dir / '%(uploader)s/%(upload_date)s - %(title)s.%(ext)s')
        
        if audio_only:
            format_selector = 'bestaudio/best'
            outtmpl = str(self.download_dir / '%(uploader)s/%(upload_date)s - %(title)s.%(ext)s')
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': outtmpl,
            'writeinfojson': False, 
            'writesubtitles': False,
            'writeautomaticsub': False,
            'ignoreerrors': True,
            'no_warnings': False,
        }
        
        # Hook to track successful downloads
        def download_hook(d):
            if d['status'] == 'finished':
                video_info = d.get('info_dict', {})
                if video_info.get('id'):
                    self._add_downloaded_video(video_info['id'], video_info)
        
        ydl_opts['progress_hooks'] = [download_hook]
        
        if max_videos:
            ydl_opts['playlistend'] = max_videos
            
        return ydl_opts

    def download_channel(self, channel_url, audio_only=False, max_videos=None):
        """Downloads channel videos"""
        
        print(f"🔍 Analyzing channel: {channel_url}")
        
        channel_info = self.get_channel_videos(channel_url, max_videos)
        if not channel_info:
            return False
        
        channel_title = channel_info.get('title', 'Unknown Channel')
        channel_uploader = channel_info.get('uploader', 'Unknown Uploader')
        total_videos = len(channel_info.get('entries', []))
        
        print(f"📺 Channel: {channel_title}")
        print(f"👤 Uploader: {channel_uploader}")
        print(f"🎬 Total videos: {total_videos}")
        
        new_videos = self.filter_new_videos(channel_info)
        videos_to_download = len(new_videos)
        
        if videos_to_download == 0:
            print("✅ No new videos found! Channel is already up to date.")
            return True
        
        print(f"🆕 New videos found: {videos_to_download}")
        print(f"⬇️  Downloading only new videos...")
        
        video_urls = [f"https://www.youtube.com/watch?v={video['id']}" 
                        for video in new_videos if video.get('id')]
                 
        print(f"📁 Destination folder: {self.download_dir.absolute()}")
        print("-" * 50)
        
        ydl_opts = self.configure_ydl_opts(audio_only, max_videos)
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if video_urls:
                    for video_url in video_urls:
                        try:
                            test = ydl.download([video_url])
                        except Exception as e:
                            print(f"⚠️  Error downloading video {video_url}: {e}")
                    
            print("✅ Download completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error during download: {e}")
            return False
    
youtube_downloader = YouTubeChannelDownloader()