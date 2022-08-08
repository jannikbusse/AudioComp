TIME=30
MIN=30
MAX=120

python3 main.py -d $TIME -f Burg -b am_amb70_birds.mp3 --mix 2 --offset 10 -o out2/burg.mp3 -ms $MIN -xs $MAX
python3 main.py -d $TIME -f Dungeon -b backmp3.mp3 --mix 2 --offset 10 -o out2/dungeon.mp3 -ms $MIN -xs $MAX
python3 main.py -d $TIME -f Wald -b am_amb70_birds.mp3 --mix 2 --offset 10 -o out2/wald.mp3 -ms $MIN -xs $MAX
python3 main.py -d $TIME -f Wasser -b wasser.mp3 --mix 2 --offset 10 -o out2/wasser.mp3 -ms $MIN -xs $MAX
python3 main.py -d $TIME -f Bar -b campmp3.mp3 --mix 2 --offset 10 -o out2/bar.mp3 -ms $MIN -xs $MAX