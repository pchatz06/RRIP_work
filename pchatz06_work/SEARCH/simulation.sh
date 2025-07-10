trap "echo 'Terminating all child processes'; kill -- -$$" SIGINT SIGTERM EXIT

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <mutation_rate: (M5, M10, etc)> <crossover (Onepoint/Uniform)>"
    exit 1
fi

mutation_rate="$1"       # 'local' or 'global'
crossover="$2"
echo $mutation_rate
echo $crossover

./run.sh local Blender "$1" "$2" &
./run.sh local Bwaves "$1" "$2" &
./run.sh local Cam4 "$1" "$2" &
./run.sh local cactuBSSN "$1" "$2" &
./run.sh local Exchange "$1" "$2" &
./run.sh local Gcc "$1" "$2" &
./run.sh local Lbm "$1" "$2" &
./run.sh local Mcf "$1" "$2" &
./run.sh local Parest "$1" "$2" &
./run.sh local Povray "$1" "$2" &
./run.sh local Wrf "$1" "$2" &
./run.sh local Xalancbmk "$1" "$2" &
./run.sh local Fotonik3d "$1" "$2" &
./run.sh local Imagick "$1" "$2" &
./run.sh local Leela "$1" "$2" &
./run.sh local Omnetpp "$1" "$2" &
./run.sh local Perlbench "$1" "$2" &
./run.sh local Roms "$1" "$2" &
./run.sh local x264 "$1" "$2" &
./run.sh local Xz "$1" "$2" &
./run.sh global Blender:Bwaves:Cam4:cactuBSSN:Exchange:Gcc:Lbm:Mcf:Parest:Povray:Wrf:Xalancbmk:Fotonik3d:Imagick:Leela:Omnetpp:Perlbench:Roms:x264:Xz "$1" "$2"