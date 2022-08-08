import os, random
from moviepy.editor import AudioFileClip, afx
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

if args.mix < 1:
    parser.error("Mix must be at least 1")



length_in_min = args.duration
min_pause_in_sec = args.min_silence
max_pause_in_sec = args.max_silence
mixing = args.mix


usedir = {}


def safe_clip():
    audioClip.write_audiofile(args.output, fps=44100)

print("length                   = " + str(length_in_min)+" min")
print("min pause                = " + str(min_pause_in_sec)+" sec")
print("max pause                = " + str(max_pause_in_sec)+" sec")
print("max audio overlays       = " + str(mixing))
print("output file              = " + args.output)
print("background audio file    = " + (args.background if args.background != "" else "none"))
print("start offset             = " + str(args.start_offset)+" sec")

files = list(filter(lambda f: os.path.isfile(args.folder + "/" + f) and f.endswith((".mp3", ".m4a")), os.listdir(args.folder)))

# if a background sound is given set background clip and remove it from the file list


res = []
if args.background != "":
    try:
        files.remove(args.background)
    except:
        pass
    audioClip = afx.audio_loop(AudioFileClip(args.folder+"/"+args.background, fps=44100), duration=length_in_min * 60).fx(afx.audio_fadeout, duration=2).fx(afx.audio_normalize).volumex(0.5)
    res.append(audioClip)


for f in files:
    usedir[f] = 0

print("\n---USAGE---")

curr = random.randint(min_pause_in_sec, max_pause_in_sec)

while curr < length_in_min * 60:
    max = 0
    for f in random.sample(files, random.randint(1,mixing)):
        usedir[f] += 1
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





