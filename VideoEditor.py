from MusicVideo import MusicVideo
import ffmpeg
import json
import os

VIDEO_LENGTH = 60
FADE_DURATION = 2
FONT_SIZE = 70 
OVERLAY_DURATION = 5
FONT_COLOR = 'yellow'
FONT_FILE = 'Lato-Bold.ttf'
WIDTH = 1920
HEIGHT = 1080 

class VideoEditor:
    def all_edits(self, music_video):
        video = self.get_video_stream(music_video.file_in)
        audio = self.get_audio_stream(music_video.file_in)
        
        video_trim, audio_trim = self.trim(video, audio, music_video.start, music_video.end)
        
        #music_video.width, music_video.height = self.get_resolution(music_video.file_in)
        video_scale = self.scale(video_trim, WIDTH, HEIGHT)
        video_overlay = self.overlay(video_scale, music_video)

        video_fade, audio_fade = self.fade(video_overlay, audio_trim, FADE_DURATION)

        self.combine_video_audio(video_fade, audio_fade, music_video.file_out)

        os.remove(music_video.file_in)

    def concatenate_all(self, videos, output_path, num_videos):
        video_streams = []
        audio_streams = []
        
        for video in videos:
            video_streams.append(ffmpeg.input(video.file_out).video)
            audio_streams.append(ffmpeg.input(video.file_out).audio)

        video_and_audio_streams = [(video_streams[i], audio_streams[i]) for i in range(num_videos)]
        joined = ffmpeg.concat(*[item for sublist in video_and_audio_streams for item in sublist], n=120, v=1, a=1, unsafe=True)

        output = ffmpeg.output(joined, output_path)
        output.run()    

    def get_video_stream(self, input_path):
        input_stream = ffmpeg.input(input_path)
        return input_stream.video

    def get_audio_stream(self, input_path):
        input_stream = ffmpeg.input(input_path)
        return input_stream.audio

    def trim(self, video_stream, audio_stream, start, end):
        video_trim = video_stream.trim(start=start, end=end).setpts('PTS-STARTPTS')
        audio_trim = audio_stream.filter_('atrim', start=start, end=end).filter_('asetpts', 'PTS-STARTPTS')
        return video_trim, audio_trim

    def scale(self, video_stream, width_in, height_in):
        video_scale = video_stream.filter_('scale', width=width_in, height=height_in)
        video_setsar = video_scale.filter_('setsar', sar='1')
        video_fps = video_setsar.filter('fps', fps=24, round='up')
        return video_fps

    def combine_video_audio(self, video_stream, audio_stream, output_path):
        joined = ffmpeg.concat(video_stream, audio_stream, v=1, a=1).node
        ffmpeg.output(joined[0], joined[1], output_path).run()

    def concat(self, input_path_1, input_path_2, output_path):
        input_stream_1 = ffmpeg.input(input_path_1)
        input_stream_2 = ffmpeg.input(input_path_2)

        joined =  ffmpeg.concat(input_stream_1.video, input_stream_1.audio, input_stream_2.video, input_stream_2.audio, n=4, v=1, a=1)
        output = ffmpeg.output(joined, output_path)
        output.run()

    def fade(self, video_stream, audio_stream, duration):
        video_fade = video_stream.filter('fade', t="in", st=0, d=duration)
        video_fade = video_fade.filter('fade', t="out", st=(VIDEO_LENGTH - duration), d=duration)
        audio_fade = audio_stream.filter('afade', t="in", st=0, d=duration)
        audio_fade = audio_fade.filter('afade', t="out", st=(VIDEO_LENGTH - duration), d=duration)
        return video_fade, audio_fade

    def overlay(self, video_stream, music_video):
        #x_pos = music_video.width * 0.02
        #y_pos = music_video.height * 0.92
        x_pos = WIDTH * 0.02
        y_pos = HEIGHT * 0.92
        enable_string = "between(t," + str(0) + "," + str(OVERLAY_DURATION) + ")"
        video_overlay = ffmpeg.drawtext(video_stream, text=music_video.overlay_text, x=x_pos, y=y_pos, fontsize=FONT_SIZE, enable=enable_string, fontcolor=FONT_COLOR, fontfile=FONT_FILE)
        enable_string = "between(t," + str(VIDEO_LENGTH - OVERLAY_DURATION) + "," + str(VIDEO_LENGTH) + ")"
        video_overlay = ffmpeg.drawtext(video_overlay, text=music_video.overlay_text, x=x_pos, y=y_pos, fontsize=FONT_SIZE, enable=enable_string, fontcolor=FONT_COLOR, fontfile=FONT_FILE)
        return video_overlay

    def get_resolution(self, input_path):
        probe = ffmpeg.probe(input_path)
        video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
        width = video_streams[0]['coded_width']
        height = video_streams[0]['coded_height']
        return (width, height)