from pytube import YouTube
from pytube import Playlist
import re

# Gives download progress
def on_progress(stream, chunk, bytes_remaining):
    progress = f"{round(100 - (bytes_remaining/stream.filesize * 100), 2)}%"
    print(f"progress: {progress}")

# Do this on download completion
def on_complete(stream, file_path):
    print("Download Completed")
    print(f"Download path: {file_path}")

def clean_file_name(name):
    # Define a regular expression to match illegal characters in file names
    illegal_chars = r'[\\/:"*?<>|]'
    
    # Replace illegal characters with an underscore
    cleaned_name = re.sub(illegal_chars, '_', name)
    
    return cleaned_name

# Get user input for media type (mp4 or mp3)
media_type = input("Enter the type of media you want to download (mp4 or mp3): ").lower()

# Get user input for single video or playlist
download_type = input("Enter 'single' to download a single video or 'playlist' to download a playlist: ").lower()

if download_type == 'single':
    # Get video URL from user
    video_url = input("Please enter the video URL: ")
    yt = YouTube(url=video_url, on_progress_callback=on_progress, on_complete_callback=on_complete)  # Create Youtube obj

    if media_type == 'mp4':
        stream = yt.streams.get_highest_resolution()
        title = clean_file_name(yt.title)
        print(f"Video title: {title}")
        print(f"Video download quality: {stream.resolution}")
        file_size = round((stream.filesize / 1000000), 2)
        print(f"File Size: {file_size} MB")
        stream.download(filename=f"{title}.mp4")
        print("\n")
    elif media_type == 'mp3':
        audio_stream = yt.streams.filter(only_audio=True).first()
        title = clean_file_name(yt.title)
        print(f"Audio title: {title}")
        print(f"Audio download quality: {audio_stream.abr}")
        file_size = round((audio_stream.filesize / 1000000), 2)
        print(f"File Size: {file_size} MB")
        audio_stream.download(filename=f"{title}.mp3")
        print("\n")
    else:
        print("Invalid media type. Please enter 'mp4' or 'mp3'.")

elif download_type == 'playlist':
    # Get playlist URL from user
    pl_url = input("Please enter Playlist URL: ")

    # Create Playlist obj
    pl = Playlist(pl_url)

    # Num of videos in playlist
    video_count = pl.length
    remaining_video_count = 1

    print(f"\n\nNumber of videos in the playlist: {video_count}")
    print("Downloading started...\n\n")
    print(f"Remaining: {remaining_video_count} out of {video_count}")

    # For every video in the playlist
    for vids in pl.videos:
        vid_url = vids.watch_url
        yt = YouTube(url=vid_url, on_progress_callback=on_progress, on_complete_callback=on_complete)  # Create Youtube obj

        if media_type == 'mp4':
            stream = yt.streams.get_highest_resolution()
            title = clean_file_name(yt.title)
            print(f"Video title: {title}")
            print(f"Video download quality: {stream.resolution}")
            file_size = round((stream.filesize / 1000000), 2)
            print(f"File Size: {file_size} MB")
            stream.download(filename=f"{remaining_video_count} - {title}.mp4")
            remaining_video_count += 1
            print("\n")
        elif media_type == 'mp3':
            audio_stream = yt.streams.filter(only_audio=True).first()
            title = clean_file_name(yt.title)
            print(f"Audio title: {title}")
            print(f"Audio download quality: {audio_stream.abr}")
            file_size = round((audio_stream.filesize / 1000000), 2)
            print(f"File Size: {file_size} MB")
            audio_stream.download(filename=f"{remaining_video_count} - {title}.mp3")
            remaining_video_count += 1
            print("\n")
        else:
            print("Invalid media type. Please enter 'mp4' or 'mp3'.")

        print(f"Remaining: {remaining_video_count} out of {video_count}")

else:
    print("Invalid download type. Please enter 'single' or 'playlist'.")
