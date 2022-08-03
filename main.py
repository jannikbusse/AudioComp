from email.mime import audio
import sys, os, random
from matplotlib import use
from moviepy.editor import concatenate_audioclips, AudioFileClip, afx
import moviepy.editor as mpe
import argparse

#argument parsing
parser = argparse.ArgumentParser(description='Generate a random audio file')
parser.add_argument('-d', '--duration', type=int, default=10, help='Duration of the audio file')
parser.add_argument('-f', '--folder', type=str, default="input", help='Folder to look for clips in')
parser.add_argument('-o', '--output', type=str, default="out.mp3", help='Output file')
parser.add_argument('-b', '--background', type=str, default="", help='Background audio file')
parser.add_argument('-ms', '--min-silence', type=int, default=1, help='Minimum silence between clips')
parser.add_argument('-xs', '--max-silence', type=int, default=10, help='Maximum silence between clips')
parser.add_argument('--mix', type=int, default=1, help='Number of clips to mix')
parser.add_argument('--offset', type=int, default=0, help='Max seconds the start of each mixed clip offsets (a random number will be chosen)')
parser.add_argument('--start_offset', type=int, default=0, help='Seconds to start the audio clip')

args = parser.parse_args()

if not os.path.isdir(args.folder):
    parser.error("Folder does not exist")

if not (args.background == "" or os.path.isfile(args.folder +"/"+ args.background)):
    parser.error("Background audio file not found")


#silence_file = "silence.mp3"
length_in_min = args.duration
min_pause_in_sec = args.min_silence
max_pause_in_sec = args.max_silence
mixing = args.mix

#current_mp3_time = 0

usedir = {}

#audioClip = AudioFileClip("silence.mp3")
#silence_clip = AudioFileClip(silence_file)

""" def add_silence(seconds):
    global audioClip
    global silence_clip
    
    for i in range(int(float(seconds)/silence_clip.duration)):
        final_clip = concatenate_audioclips([audioClip, silence_clip])
        audioClip = final_clip """

""" def concatenate_audio_moviepy(clip):
    global audioClip
    clip.fps = 44100
    
    final_clip = concatenate_audioclips([audioClip, clip.fx(afx.audio_normalize).volumex(0.7)])
    audioClip = final_clip """

""" def mix_clips(clips): #todo shift clips back and forth
    for s in clips:
        usedir[s] += 1

    new_audioclip = mpe.CompositeAudioClip([AudioFileClip("input/"+c) for c in clips])
    return new_audioclip """

def safe_clip():
    audioClip.write_audiofile("out.mp3", fps=44100)

#if len(sys.argv) <= 2:
 #   exit()

"""
length_in_min    = int(sys.argv[1])
min_pause_in_sec = int(sys.argv[2])
max_pause_in_sec = int(sys.argv[3])
mixing =           max(int(sys.argv[4]), 1)
if len(sys.argv) > 5:
    background_clip = sys.argv[5]
else:
    background_clip = None
"""

print("length                   = " + str(length_in_min))
print("min pause                = " + str(min_pause_in_sec))
print("max pause                = " + str(max_pause_in_sec))
print("max audio overlays       = " + str(mixing))

files = os.listdir(args.folder)

# if a background sound is given set background clip and remove it from the file list


res = []
if args.background != "":
    files.remove(args.background)
    audioClip = afx.audio_loop(AudioFileClip(args.folder+"/"+args.background, fps=44100), duration=length_in_min * 60).fx(afx.audio_fadeout, duration=2).fx(afx.audio_normalize)
    res.append(audioClip)

#clips = [AudioFileClip(args.folder+"/"+f) for f in files]

for f in files:
    usedir[f] = 0

#add_silence(3)
print("\n---USAGE---")

curr = random.randint(min_pause_in_sec, max_pause_in_sec)

while curr < length_in_min * 60:
    max = 0
    for f in random.sample(files, mixing):
        clip = AudioFileClip(args.folder + "/"+ f, fps=44100).set_start(curr+random.randint(0, args.offset)).fx(afx.audio_normalize)
        if clip.end > max:
            max = clip.end
        res.append(clip)
    curr = max + random.randint(min_pause_in_sec, max_pause_in_sec)


audioClip = mpe.CompositeAudioClip(res).set_duration(length_in_min * 60).set_start(args.start_offset, change_end=False)

for k in files:
    print(k + " was used " + str(usedir[k]) + " times")
print()
safe_clip()





