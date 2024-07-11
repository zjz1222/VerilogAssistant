quit -sim 

#.main    clear

vlib    ./lib
vlib    ./lib/work

vmap     work ./lib/work

vlog    -work    work    ./design/*.v -l ./design/vcompile.txt
