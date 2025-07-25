#!/bin/bash

nohup ./simulation.sh gcc_r.txt -global M5 Onepoint &
nohup ./simulation.sh mcf_r.txt -global M5 Onepoint &
nohup ./simulation.sh cactuBSSN_r.txt -global M5 Onepoint &
nohup ./simulation.sh namd_r.txt -global M5 Onepoint &
nohup ./simulation.sh parest_r.txt -global M5 Onepoint &
nohup ./simulation.sh lbm_r.txt -global M5 Onepoint &
nohup ./simulation.sh omnetpp_r.txt -global M5 Onepoint &
nohup ./simulation.sh wrf_r.txt -global M5 Onepoint &
nohup ./simulation.sh cam4_r.txt -global M5 Onepoint &
nohup ./simulation.sh fotonik3d_r.txt -global M5 Onepoint &
nohup ./simulation.sh roms_r.txt -global M5 Onepoint &
nohup ./simulation.sh xz_r.txt -global M5 Onepoint &
