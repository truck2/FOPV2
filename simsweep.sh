#!/bin/bash

lion_low=3
lion_step=1
lion_high=6

wolf_low=3
wolf_step=1
wolf_high=6

rabbit_low=5
rabbit_step=5
rabbit_high=20

for l in `seq $lion_low $lion_step $lion_high`;
do
    for w in `seq $wolf_low $wolf_step $wolf_high`;
    do
        for r in `seq $rabbit_low $rabbit_step $rabbit_high`;
        do
        python3 main.py map.txt 150 0 "$l" "$w" "$r" 
        done 
    done    
done  
