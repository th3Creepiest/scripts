import subprocess
import yt_dlp


def is_ffmpeg_installed() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_m4a(url: str):
    video_info = yt_dlp.YoutubeDL().extract_info(url=url, download=False)
    file_out = f"./downloads/{video_info['title']}.m4a"
    options = {"format": "bestaudio/best", "keepvideo": False, "outtmpl": file_out}

    print(f"Downloading... {file_out}")
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_info["webpage_url"]])
    print(f"Download complete... {file_out}")


if __name__ == "__main__":
    import sys

    if not is_ffmpeg_installed():
        print("FFmpeg is not installed. Please install FFmpeg to use this script.")
        sys.exit(1)

    download_m4a(url=input("Enter URL of YouTube video: "))
