from managers.video_manager import video_manager
from dotenv import load_dotenv
from helpers import markdown_json_to_dict
from prompts.cut_to_instagram.handler import cut_viral_prompt_to_instagram
from prompts.cut_viral_prompt.handler import cut_viral_prompt
from helpers import markdown_json_to_dict
import os

load_dotenv()

def process_instagram_video(path):
    text, segments = video_manager.transcribe_video(path)
    srt_path = os.path.splitext(path)[0] + ".srt"

    with open(srt_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    video_manager.embed_subtitles(path, srt_path)
    path_instagram = video_manager.format_to_instagram(path)

    cut_viral_to_instagram = cut_viral_prompt_to_instagram.send_prompt(srt_content)
    cut_viral_to_instagram = markdown_json_to_dict(cut_viral_to_instagram)

    video_manager.cut_video(path_instagram, cut_viral_to_instagram['cortes_virais'])


def process_regular_video(path):
    text, segments = video_manager.transcribe_video(path)
    srt_path = os.path.splitext(path)[0] + ".srt"

    with open(srt_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    video_manager.embed_subtitles(path, srt_path)

    cut_viral = cut_viral_prompt.send_prompt(srt_content)

    cut_viral_dict = markdown_json_to_dict(cut_viral)
    video_manager.cut_video(path, cut_viral_dict['cortes_virais'])


def main():
    path = input("Enter the path to the video: ").strip()
    is_instagram = input("Is the video for Instagram? (y/n): ").strip().lower()

    if is_instagram == 'y':
        process_instagram_video(path)
    else:
        process_regular_video(path)

if __name__ == "__main__":
    main()