# From here: https://superuser.com/a/556031
INPUT=$1
OUTPUT=$INPUT.gif
WIDTH=320
FPS=10
# crop should be specified as an FFMPEG string:
# crop=out_w:out_h:x:y
CROP=$2
START_TIME=${3:-0}
LENGTH=${4:-5}
ffmpeg -y -ss $START_TIME -t $LENGTH -i $INPUT -vf "fps=$FPS,crop=$CROP,scale=$WIDTH:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 $OUTPUT
