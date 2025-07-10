trap "echo 'Terminating all child processes'; kill -- -$$" SIGINT SIGTERM EXIT

./run.sh local Blender M10 Onepoint &
./run.sh local Bwaves M10 Onepoint &
./run.sh local Cam4 M10 Onepoint &
./run.sh local cactuBSSN M10 Onepoint &
./run.sh local Exchange M10 Onepoint &
./run.sh local Gcc M10 Onepoint &
./run.sh local Lbm M10 Onepoint &
./run.sh local Mcf M10 Onepoint &
./run.sh local Parest M10 Onepoint &
./run.sh local Povray M10 Onepoint &
./run.sh local Wrf M10 Onepoint &
./run.sh local Xalancbmk M10 Onepoint &
./run.sh local Fotonik3d M10 Onepoint &
./run.sh local Imagick M10 Onepoint &
./run.sh local Leela M10 Onepoint &
./run.sh local Omnetpp M10 Onepoint &
./run.sh local Perlbench M10 Onepoint &
./run.sh local Roms M10 Onepoint &
./run.sh local x264 M10 Onepoint &
./run.sh local Xz M10 Onepoint &
./run.sh global Blender:Bwaves:Cam4:cactuBSSN:Exchange:Gcc:Lbm:Mcf:Parest:Povray:Wrf:Xalancbmk:Fotonik3d:Imagick:Leela:Omnetpp:Perlbench:Roms:x264:Xz M10 Onepoint