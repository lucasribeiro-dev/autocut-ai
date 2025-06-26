from src.managers.video_manager import video_manager
from dotenv import load_dotenv
from helpers import markdown_json_to_dict
from src.prompts.send_prompt import SendPrompt
from src.download_videos.youtube_dowloader import youtube_downloader
import os
import glob

load_dotenv()

def process_regular_video(path):
    text, segments = video_manager.transcribe_video(path)
    srt_path = os.path.splitext(path)[0] + ".srt"

    print("srt_path", srt_path)

    with open(srt_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    # video_manager.embed_subtitles(path, srt_path)

    cut_viral = SendPrompt('src/prompts/texts/cut_to_instagram.txt').build(srt_content)

    cut_viral_dict = markdown_json_to_dict(cut_viral)
    print("cut_viral_dict", cut_viral_dict)
    video_manager.cut_video(path, cut_viral_dict['cortes_virais'])


def main():
    youtube_downloader.download_channel(os.getenv("YOUTUBE_CHANNEL"), max_videos=1)
    video_dir = 'src/download_videos/downloads'
    video_paths = glob.glob(os.path.join(video_dir, '**', '*.mp4'), recursive=True)
    for path in video_paths:
        print(f"Processando: {path}")
        process_regular_video(path)
        os.remove(path)
        print(f"Removido: {path}")

if __name__ == "__main__":
    main()