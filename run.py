import os
import sys
from stat import FILE_ATTRIBUTE_INTEGRITY_STREAM
from VideoEditor import VideoEditor
from CsvToVideo import CsvToVideo
from yt_dlp import YoutubeDL

if len(sys.argv) >= 1:
    filepath = sys.argv[1]
    print("Filepath:", filepath)
else:
    print("Try again")

editor = VideoEditor()
c2v = CsvToVideo()

videos = c2v.read_csv(filepath)

ydl = YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
with ydl:

    for video in videos:
        info = ydl.extract_info(video.url, download=False)
        video.file_in = info['id'] + "." + info['ext']
        error_code = ydl.download(video.url)

for video in videos:
    editor.all_edits(video)

editor.concatenate_all(videos, "_FINAL_CUT_v3.mp4", len(videos))