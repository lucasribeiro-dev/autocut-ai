import os
import subprocess
import whisper
import moviepy as mp
from typing import List, Dict, Tuple
import os
from dotenv import load_dotenv
from helpers import format_timestamp,timestamp_to_seconds
load_dotenv()


class VideoManager:
    def __init__(self):
        self.whisper_model = whisper.load_model("medium")

    def transcribe_video(self, video_path: str) -> Tuple[str, List[Dict]]:
        """
        Transcribe video using Whisper and generate SRT file.
        
        Args:
            video_path: Path to the input video file
            
        Returns:
            Tuple containing full transcription text and segments with timestamps
        """
        audio = mp.AudioFileClip(video_path)
        audio_path = "temp_audio.wav"
        audio.write_audiofile(audio_path)
        
        result = self.whisper_model.transcribe(audio_path)
        
        os.remove(audio_path)
        
        srt_content = ""
        for i, segment in enumerate(result["segments"], 1):
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            srt_content += f"{i}\n{start_time} --> {end_time}\n{segment['text'].strip()}\n\n"
        
        srt_path = os.path.splitext(video_path)[0] + ".srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
        
        return result["text"], result["segments"]

    def remove_silences(self, video_path: str, segments: List[Dict], silence_threshold: float = 2.0) -> str:
        """
        Remove segments with silence longer than threshold.
        
        Args:
            video_path: Path to the input video file
            segments: List of segments from Whisper transcription
            silence_threshold: Minimum duration of silence to remove (in seconds)
            
        Returns:
            Path to the processed video file
        """
        keep_segments = []
        for i in range(len(segments) - 1):
            current_end = segments[i]["end"]
            next_start = segments[i + 1]["start"]
            if next_start - current_end < silence_threshold:
                keep_segments.append(segments[i])
        keep_segments.append(segments[-1])
        
        cuts = []
        for segment in keep_segments:
            cuts.append((segment["start"], segment["end"]))
        
        video = mp.VideoFileClip(video_path)
        clips = []
        for start, end in cuts:
            clips.append(video.subclipped(start, end))
        
        final_video = mp.concatenate_videoclips(clips)
        
        output_path = os.path.splitext(video_path)[0] + "_processed.mp4"
        final_video.write_videofile(output_path)
        
        return output_path

    def embed_subtitles(self, video_path: str, srt_path: str) -> str:
        """
        Embed subtitles into the video using ffmpeg.
        
        Args:
            video_path: Path to the input video file
            srt_path: Path to the SRT file
            
        Returns:
            Path to the video with embedded subtitles
        """
        output_path = os.path.splitext(video_path)[0] + "_subtitled.mp4"
        
        cmd = [
            "ffmpeg", "-i", video_path,
            "-vf", f"subtitles={srt_path}:force_style='Fontsize=14,PrimaryColour=&HFFFFFF&'",
            "-c:a", "copy",
            output_path
        ]
        
        subprocess.run(cmd, check=True)
        return output_path

    def add_logo(self, video_path: str, logo_path: str, position: str = "bottom-right", size: float = 0.1) -> str:
        """
        Add a logo to the video in the specified position.
        
        Args:
            video_path: Path to the input video file
            logo_path: Path to the logo image file
            position: Position of the logo ('bottom-right', 'bottom-left', 'top-right', 'top-left')
            size: Size of the logo relative to video height (0.0 to 1.0)
            
        Returns:
            Path to the video with logo
        """
        # Load video and logo
        video = mp.VideoFileClip(video_path)
        logo = mp.ImageClip(logo_path)
        
        # Resize logo
        logo_height = int(video.h * size)
        logo = logo.resize(height=logo_height)
        
        # Calculate position
        if position == "bottom-right":
            x_pos = video.w - logo.w - 10
            y_pos = video.h - logo.h - 10
        elif position == "bottom-left":
            x_pos = 10
            y_pos = video.h - logo.h - 10
        elif position == "top-right":
            x_pos = video.w - logo.w - 10
            y_pos = 10
        elif position == "top-left":
            x_pos = 10
            y_pos = 10
        else:
            raise ValueError("Invalid position. Use 'bottom-right', 'bottom-left', 'top-right', or 'top-left'")
        
        # Set position and duration
        logo = logo.set_position((x_pos, y_pos)).set_duration(video.duration)
        
        # Composite video with logo
        final_video = mp.CompositeVideoClip([video, logo])
        
        # Save processed video
        output_path = os.path.splitext(video_path)[0] + "_with_logo.mp4"
        final_video.write_videofile(output_path)
        
        return output_path

    def format_to_instagram(self, video_path: str) -> str:
        """
        Format video to Instagram.
        
        Args:
            video_path: Path to the input video file
            
        Returns:
            Path to the video with Instagram format 
        """
        output_path = os.path.splitext(video_path)[0] + "_instagram.mp4"

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vf", "scale=w=1080:h=1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black",
            "-c:a", "copy",
            output_path
        ]

        subprocess.run(ffmpeg_cmd, check=True)

        return output_path

    def cut_video(self,video_path: str, cuts) -> str:
        """
        Corta o vídeo em segmentos com base nos timestamps fornecidos e salva-os na pasta __videos__.

        Args:
            video_path: Caminho para o arquivo de vídeo de entrada.
            cuts: Lista de dicionários contendo informações de corte com timestamps e títulos.

        Returns:
            Caminho para a pasta contendo todos os vídeos cortados.
        """
        output_dir = "__videos__"
        os.makedirs(output_dir, exist_ok=True)

        video = mp.VideoFileClip(video_path)

        for cut in cuts:
            start_time = timestamp_to_seconds(cut["timestamp_inicio"])
            end_time = timestamp_to_seconds(cut["timestamp_fim"])

            # Garante que o end_time não ultrapasse a duração do vídeo
            end_time = min(end_time, video.duration)

            clip = video.subclipped(start_time, end_time)

            # Sanitiza o título para uso no nome do arquivo
            safe_title = "".join(c for c in cut["titulo_instagram"] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')

            output_path = os.path.join(output_dir, f"{safe_title}.mp4")
            clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        return output_dir

video_manager = VideoManager()