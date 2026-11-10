#!/bin/bash
# usage: master.sh NN  (premix_NN.wav -> final_mix_NN.wav, two-pass loudnorm -14 LUFS, TP -2, linear=false)
n=$1
j=$(ffmpeg -hide_banner -i premix_$n.wav -af loudnorm=I=-14:TP=-2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$j" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -y -v error -i premix_$n.wav -af "loudnorm=I=-14:TP=-2:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=false" -ar 48000 final_mix_$n.wav
ffmpeg -hide_banner -i final_mix_$n.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
