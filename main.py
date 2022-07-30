from email.mime import audio
import sys, os, random
from matplotlib import use
from moviepy.editor import concatenate_audioclips, AudioFileClip, afx
import moviepy.editor as mpe

silence_file = "silence.mp3"
length_in_min = 0
min_pause_in_sec = 10
max_pause_in_sec = 100
mixing = 0

current_mp3_time = 0

usedir = {}

audioClip = AudioFileClip("silence.mp3")
silence_clip = AudioFileClip(silence_file)

def add_silence(seconds):
    global audioClip
    global silence_clip
    
    for i in range(int(float(seconds)/silence_clip.duration)):
        final_clip = concatenate_audioclips([audioClip, silence_clip])
        audioClip = final_clip

def concatenate_audio_moviepy(clip):
    global audioClip
    clip.fps = 44100
    
    final_clip = concatenate_audioclips([audioClip, clip.fx(afx.audio_normalize).volumex(0.7)])
    audioClip = final_clip

def mix_clips(clips): #todo shift clips back and forth
    for s in clips:
        usedir[s] += 1

    new_audioclip = mpe.CompositeAudioClip([AudioFileClip("input/"+c) for c in clips])
    return new_audioclip

def safe_clip():
    audioClip.write_audiofile("out.mp3")

if len(sys.argv) <= 2:
    exit()

length_in_min    = int(sys.argv[1])
min_pause_in_sec = int(sys.argv[2])
max_pause_in_sec = int(sys.argv[3])
mixing =           max(int(sys.argv[4]), 1)

print("length                   = " + str(length_in_min))
print("min pause                = " + str(min_pause_in_sec))
print("max pause                = " + str(max_pause_in_sec))
print("max audio overlays       = " + str(mixing))

files = os.listdir('input')
for f in files:
    usedir[f] = 0

add_silence(3)
print("\n---USAGE---")
while audioClip.duration < length_in_min * 60:
    r_pause = random.randint(min_pause_in_sec, max_pause_in_sec)
    add_silence(r_pause)
    #file = random.choice(files)
    li = random.sample(files, mixing)
    concatenate_audio_moviepy(mix_clips(li))
    #concatenate_audio_moviepy(AudioFileClip("input/"+file))

for k in files:
    print(k + " was used " + str(usedir[k]) + " times")
print()
safe_clip()





