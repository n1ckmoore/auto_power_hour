import ffmpeg

class MusicVideo:
    artist = ""
    song = ""
    url = ""
    file_download = ""
    file_in = ""
    file_out = ""
    overlay_text = ""
    input_stream = ""
    output_stream = ""
    start = 0
    end = 0
    width = 0
    height = 0

    def __init__(self, artist, song, url, start):
        self.artist = artist
        self.song = song
        self.url = url
        self.start = int(start)
        self.overlay_text = artist + " - " + song
        self.file_download = "NOT SET"
        self.file_in = "NOT SET"
        self.file_out = self.overlay_text + "_edit" ".mp4"
        self.end = self.start + 60

        print("File out: " + self.file_out)