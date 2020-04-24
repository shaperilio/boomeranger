# From here: https://superuser.com/a/556031
INPUT=$1
OUTPUT=$INPUT.gif
WIDTH=320
FPS=10
START_TIME=${2:-0}
LENGTH=${3:-5}
ffmpeg -y -ss $START_TIME -t $LENGTH -i $INPUT -vf "fps=$FPS,scale=$WIDTH:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 $OUTPUT
