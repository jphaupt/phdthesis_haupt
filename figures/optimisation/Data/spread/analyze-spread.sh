#!/bin/bash

# Reads data from stdin and produces results.

list_nopt=""

while read nopt i v r e t ; do
  [ -z "$nopt" ] && continue
  [ "${nopt:0:1}" = '#' ] && continue
  [ -z "$e" ] && continue
  v="${v%(*}"
  e="${e%(*}"
  t="${t%(*}" # unused
  if ((n_$nopt==0)) ; then
    list_nopt="$list_nopt $nopt"
    ((sum_v_$nopt=0))
    ((sum_r_$nopt=0))
    ((sum_r2_$nopt=0))
    ((sum_e_$nopt=0))
    ((sum_e2_$nopt=0))
  fi
  ((n_$nopt++))
  eval "sum_v_$nopt=\"\$sum_v_$nopt + (\$v)\""
  eval "sum_r_$nopt=\"\$sum_r_$nopt + (\$r)\""
  eval "sum_r2_$nopt=\"\$sum_r2_$nopt + (\$r)^2\""
  eval "sum_e_$nopt=\"\$sum_e_$nopt + (\$e)\""
  eval "sum_e2_$nopt=\"\$sum_e2_$nopt + (\$e)^2\""
  eval "list_r_$nopt=\"\$list_r_$nopt \$r\""
  eval "list_e_$nopt=\"\$list_e_$nopt \$e\""
done

# Find VMC variance from largest VMC runs.
vmc_var=0
max_nopt=0
for nopt in $list_nopt ; do
  ((max_nopt>nopt)) && continue
  ((max_nopt=nopt))
  ((n=n_$nopt))
  vmc_var=$(bc -l <<<$(eval "echo \"(\$sum_v_$nopt)/$n\""))
done

for nopt in $list_nopt ; do
  ((n=n_$nopt))
  mean_r=$(bc -l <<<$(eval "echo \"(\$sum_r_$nopt)/$n\""))
  mean_r2=$(bc -l <<<$(eval "echo \"(\$sum_r2_$nopt)/$n\""))
  mean_e=$(bc -l <<<$(eval "echo \"(\$sum_e_$nopt)/$n\""))
  mean_e2=$(bc -l <<<$(eval "echo \"(\$sum_e2_$nopt)/$n\""))
  sdev_vmc=$(bc -l <<<"sqrt( $vmc_var/$nopt )")
  sdev_r=$(bc -l <<<"sqrt( ($mean_r2 - ($mean_r)^2) * ($n/($n-1)) )")
  sdev_e=$(bc -l <<<"sqrt( ($mean_e2 - ($mean_e)^2) * ($n/($n-1)) )")
  # Find greatest outlier in Eref.
  eval "list_r=\"\$list_r_$nopt\""
  ((i=0))
  max_rdev=0
  imaxr=0
  for r in $list_r ; do
    ((i++))
    rdev=$(bc -l <<<"(($r)-($mean_r))/$sdev_r")
    rdev=${rdev#-}
    bool=$(bc -l <<<"$rdev > $max_rdev")
    if ((bool)) ; then
      max_rdev=$rdev
      ((imaxr=i))
    fi
  done
  # Find greatest outlier in Etot.
  eval "list_e=\"\$list_e_$nopt\""
  ((i=0))
  max_edev=0
  imaxe=0
  for e in $list_e ; do
    ((i++))
    edev=$(bc -l <<<"(($e)-($mean_e))/$sdev_e")
    edev=${edev#-}
    bool=$(bc -l <<<"$edev > $max_edev")
    if ((bool)) ; then
      max_edev=$edev
      ((imaxe=i))
    fi
  done
  r_vr=$(bc -l <<<"$sdev_vmc/$sdev_r")
  r_re=$(bc -l <<<"$sdev_r/$sdev_e")
  r_ve=$(bc -l <<<"$sdev_vmc/$sdev_e")
  echo "* nopt=$nopt ($n instances):"
  printf "  stderr(Eref) = %.6f\n" $sdev_vmc
  printf "  stddev(Eref) = %.6f\n" $sdev_r
  printf "  stddev(E)    = %.6f\n" $sdev_e
  printf "  Eref outlier : #%s (%.2f stddevs)\n" $imaxr $max_rdev
  printf "  Etot outlier : #%s (%.2f stddevs)\n" $imaxe $max_edev
  printf "  factors: %.2f * %.2f = %.2f\n" $r_vr $r_re $r_ve
  #printf "%7s  %5.2f  %5.2f  %5.2f\n" $nopt $r_vr $r_re $r_ve
done
