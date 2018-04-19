import subprocess
import time
from utils import to_bytes


class MusicPlayer():

    def __init__(self):
        self.program = 'tizonia'
        self.process = None
        self.play_stream = False

    def kill_any_current_process(self):
        if self.process is not None:
            self.communicate_with_process('q')
            time.sleep(0.8)
            self.process.terminate()
            self.process.kill()
            self.play_stream = False
            self.process = None

    def start_audio_process(self, program_args):
        self.kill_any_current_process()
        self.process = subprocess.Popen(program_args,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.STDOUT)
        self.play_stream = True

    def communicate_with_process(self, input_text):
        input_bytes = to_bytes(input_text)
        if self.process is not None:
            self.process.stdin.write(input_bytes)
            self.process.stdin.flush()

    def skip(self):
        self.communicate_with_process('n')

    def pause(self):
        if self.play_stream:
            self.communicate_with_process(' ')
            self.play_stream = False

    def play(self):
        if not self.play_stream:
            self.communicate_with_process(' ')
            self.play_stream = True

    def previous(self):
        self.communicate_with_process('p')

    def louder(self, amount=3):
        for _ in range(amount):
            self.communicate_with_process('+')
            time.sleep(0.1)

    def loudest(self):
        for _ in range(20):
            self.communicate_with_process('+')
            time.sleep(0.1)

    def quieter(self, amount=3):
        for _ in range(amount):
            self.communicate_with_process('-')
            time.sleep(0.1)

    def quietest(self):
        for _ in range(20):
            self.communicate_with_process('-')
            time.sleep(0.1)
        self.communicate_with_process('+')

    def play_spotify_playlist(self, playlist_name):
        program_option = '--spotify-playlist'
        program_args = [self.program, program_option, playlist_name]
        self.start_audio_process(program_args)

    def play_youtube_mix(self, search_term):
        program_option = '--youtube-audio-mix-search'
        program_args = [self.program, program_option, search_term]
        self.start_audio_process(program_args)

    def play_soundcloud_artist(self, artist_name):
        program_option = '--soundcloud-creator'
        program_args = [self.program, program_option, artist_name]
        self.start_audio_process(program_args)

    def play_soundcloud_likes(self):
        program_option = '--soundcloud-user-likes'
        program_args = [self.program, program_option]
        self.start_audio_process(program_args)
