#!/usr/bin/tcsh

#SBATCH -A local

#SBATCH -p COMPUTE

# set v1 = `SAcommon | gawk '{if (NR==1) print $0}'`
# set v2 = `SAcommon | gawk '{if (NR==2) print $0}'`






setenv TRACE_DIR /mnt/beegfs/iconst01/spec2017/


set binary=$1
set n_warm=$2
set n_sim=$3
set trace=$4
set optionlist=`echo $5`
set psolist=`echo $6`
set masklist=`echo $7`
set dsalgolist=`echo $8`
set windowlist=`echo $9`
set srlist=`echo $10`
set brlist=`echo $11`
set boolist=`echo $12`
set hitlist=`echo $13`
set demlist=`echo $14`
set d_optionlist=`echo $15`
set my_id=$16
set suffix=$17

setenv RESULTS ../BENCH_DIR/${suffix}/Results

#echo $optionlist

foreach option ($optionlist)
foreach pso ($psolist)
foreach mask ($masklist)
foreach dsalgo ($dsalgolist)
foreach window ($windowlist)
foreach srt ($srlist)
foreach brt ($brlist)
foreach boost ($boolist)
foreach hit ($hitlist)
foreach dem ($demlist)
foreach d_option ($d_optionlist)

set rdir=results-$binary-$option-$d_option-$pso-$mask-$dsalgo-$window-$srt-$brt-$boost-$hit-$dem-$my_id
mkdir -p $RESULTS/$rdir
set outp=$RESULTS/$rdir/$trace.out

#echo $outp

./bin/$binary -warmup_instructions ${n_warm} -simulation_instructions ${n_sim} -rrip_policies $option -dirty_rrip_policies $d_option -psel_width $pso -psel_mask $mask -hit_mask $hit -dsalgo $dsalgo -window_size $window -sr_thr $srt -br_thr $brt -boost $boost -demote_mask $dem -traces ${TRACE_DIR}${trace}.trace.gz >& $outp

end
end
end
end
end
end
end
end
end
end
end
