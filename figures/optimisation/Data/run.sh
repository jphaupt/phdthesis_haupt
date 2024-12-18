#!/bin/bash

((keep=0))
[ "$1" = "--keep" ] && ((keep=1))

# Check for polyfit.
polyfit=$HOME/dev/polyfit/polyfit
if [ -d "$polyfit" ] || [ ! -x "$polyfit" ] ; then
  echo "This script requires a POLYFIT binary at $polyfit."
  echo
  echo "It should be possible to correct this with:"
  echo "  mkdir -p $HOME/dev && cd $HOME/dev"
  echo "  git clone https://github.com/plopezrios/polyfit"
  echo "  cd polyfit && ./compile.sh"
  exit 1
fi

# Basis set info for plots.
bs[2]="cc-pvdz" ; nbs[2]=14
bs[3]="cc-pvtz" ; nbs[3]=30
bs[4]="cc-pvqz" ; nbs[4]=55
bs[5]="cc-pv5z" ; nbs[5]=91
bs[6]="cc-pv6z" ; nbs[6]=140

# Allow running without having to change into the Data directory.
cd $(dirname $0)

# Get SHCI results by extrapolation.
for s in c n o c2 cn n2 o2 ; do
  [ -f "shci_$s.dat" ] || continue
  $polyfit > "shci_$s.log" <<__EOF
set echo
load "shci_$s.dat" type xdxy using 4,5,6 by \$1
evaluate f at X=0
plot f at X=-0.050:0:1001 to "shci_$s.plot"
__EOF
  echo -n "."
  ((ibs=1))
  f="shci_Eext_$s.dat"
  rm -f "$f"
  echo "#basis- no- Energy/Ha" > "$f"
  case "$s" in
  c|n|o) natom=1 ;;
  *) natom=2 ;;
  esac
  while read x x x e de ; do
    ((ibs++))
    printf "%-7s %3s %.7f %.7f\n" "${bs[$ibs]}" $((natom*nbs[ibs]))\
       "$e" $(printf "%f" $de) >> "$f"
  done < <(grep -E "^EVAL  " "shci_$s.log")
done

# Get FCIQMC results for atoms and no3 molecules from (single) selected
# number of walkers.
for s in {c,n,o}{,_tc} {c,n,o,c2,cn,n2,o2}_tc_{no3,emin} ; do
  [ -f "fciqmc_$s.dat" ] || continue
  echo -n "."
  ((ibs=1))
  f="fciqmc_1shot_$s.dat"
  rm -f "$f"
  echo "#basis- no- -Nwalk-- Energy/Ha" > "$f"
  case "$s" in
  c|n|o|c_*|n_*|o_*) natom=1 ;;
  *) natom=2 ;;
  esac
  while read x nw x x x e de x x ; do
    ((ibs++))
    printf "%-7s %3s %8s %.7f %.7f\n" "${bs[$ibs]}" $((natom*nbs[ibs]))\
       "$nw" "$e" "$de" >> "$f"
  done < <(grep -E "1 [01] *$" "fciqmc_$s.dat")
done

# Get FCIQMC results for molecules by extrapolation.
for s in {c2,cn,n2,o2}{,_tc} ; do
  [ -f "fciqmc_$s.dat" ] || continue
  $polyfit > fciqmc_$s.log <<__EOF
set echo
load "fciqmc_$s.dat" type xydyw using 2,6,7,2 where \$8==1 by \$1
set X 1/x
set wexp 1/3
set fit 0,1/3
evaluate f at X=0
plot f at X=0:2.e-5:1001 wrt 0 to "fciqmc_Erel_$s.plot"
plot f at X=0:2.e-5:1001 to "fciqmc_Etot_$s.plot"
__EOF
  echo -n "."
  ((ibs=1))
  f="fciqmc_Eext_$s.dat"
  rm -f "$f"
  echo "#basis- no- Energy/Ha" > "$f"
  case "$s" in
  *) natom=2 ;;
  esac
  while read x x x e de ; do
    ((ibs++))
    printf "%-7s %3s %.7f %.7f\n" "${bs[$ibs]}" $((natom*nbs[ibs]))\
       "$e" $(printf "%f" $de) >> "$f"
  done < <(grep -E "^EVAL  " "fciqmc_$s.log")
done

# Print total energies as used in table:total_energies.
t="table_Etot.txt"
echo "#sys-- -basis- Energy/Ha" > "$t"
for s in c n o c2 cn n2 o2 ; do
  case "$s" in
  c|n|o)
    ftag="1shot"
    fcol=4 ;;
  c2|cn|n2|o2)
    ftag="Eext"
    fcol=3 ;;
  esac
  for m in "" "_tc" ; do
    echo -n .
    for ((ibs=2; ibs<=6; ibs++)) ; do
      e=$(set -- $(grep -E "^${bs[$ibs]} " fciqmc_${ftag}_$s$m.dat) ;\
          echo ${@:$fcol:1})
      [ -z "$e" ] && continue
      printf "%-6s %-7s %.4f\n" "$s$m" "${bs[$ibs]}" "$e" >> "$t"
    done
  done
done

# Compute atomization energies.  This populates table:atomization and
# fig:bsdep-dimers-nontc.
t="table_Eat.txt"
echo "#sys-- -basis- Energy/mHa" > "$t"
for s in c2 cn n2 o2 ; do
  case "$s" in
  c2|n2|o2)
    na1=2
    a1=${s:0:1}
    na2=0
    a2="" ;;
  cn)
    na1=1
    na2=1
    a1=c
    a2=n ;;
  esac
  for m in "" "_tc" ; do
    echo -n .
    f="fciqmc_Eat_$s$m.dat"
    rm -f "$f"
    echo "#basis- no- Energy" > "$f"
    for ((ibs=2; ibs<=6; ibs++)) ; do
      ea1=$(set -- $(grep -E "^${bs[$ibs]} " fciqmc_1shot_${a1}$m.dat) ;\
            echo $4 $5)
      [ -z "$ea1" ] && continue
      ea2="0 0"
      [ -z "$a2" ] || ea2=$(set -- $(grep -E "^${bs[$ibs]} "\
                                     fciqmc_1shot_${a2}$m.dat) ; echo $4 $5)
      em=$(set -- $(grep -E "^${bs[$ibs]} " fciqmc_Eext_$s$m.dat) ; echo $3 $4)
      [ -z "$em" ] && continue
      set -- $em $ea1 $ea2
      e=$(bc -l <<<"-($1)+$na1*($3)+$na2*($5)")
      de=$(bc -l <<<"sqrt(($2)^2+$na1*($4)^2+$na2*($6)^2)")
      printf "%-7s %3s %.7f %.7f\n" "${bs[$ibs]}" $((2*nbs[ibs])) "$e" "$de"\
         >> "$f"
      printf "%-6s %-7s %.1f\n" "$s$m" "${bs[$ibs]}" "$(bc -l <<<"1000*($e)")"\
         >> "$t"
    done
  done
done

# Generate a *reconstructed* extrapolated atomization energy corresponding
# to an energy minimized Jastrow.  This is the "properly" extrapolated energy
# plus the difference between same-population varmin and emin results.
# This populates fig:bsdep-dimers-emin.
for s in c2 cn n2 o2 ; do
  echo -n .
  case "$s" in
  c2|n2|o2)
    na1=2
    a1=${s:0:1}
    na2=0
    a2="" ;;
  cn)
    na1=1
    na2=1
    a1=c
    a2=n ;;
  esac
  f="fciqmc_Eat_${s}_tc_emin.dat"
  rm -f "$f"
  echo "#basis- no- Energy" > "$f"
  for ((ibs=2; ibs<=6; ibs++)) ; do
    line=$(grep -E "^${bs[$ibs]} " fciqmc_1shot_${s}_tc_emin.dat)
    [ -z "$line" ] && continue
    nw=$(set -- $line ; echo $3)
    ee=$(set -- $line ; echo $4 $5)
    # Get the varmin number at the *closest* nw.
    dnw_min=-1
    ev=0
    while read x nwv x x x e de x x ; do
      ((dnw=nwv-nw))
      dnw=${dnw#-}
      if ((dnw_min<0)) || ((dnw<dnw_min)) ; then
        ((dnw_min=dnw))
        ev="$e $de"
      fi 
    done < <(grep -E "^${bs[$ibs]} " fciqmc_${s}_tc.dat)
    [ "$ev" = 0 ] && continue
    ea1e=$(set -- $(grep -E "^${bs[$ibs]} " fciqmc_1shot_${a1}_tc_emin.dat) ;\
          echo $4 $5)
    [ -z "$ea1e" ] && continue
    ea2e="0 0"
    [ -z "$a2" ] || ea2e=$(set -- $(grep -E "^${bs[$ibs]} "\
                                   fciqmc_1shot_${a2}_tc_emin.dat) ; echo $4 $5)
    ea1v=$(set -- $(grep -E "^${bs[$ibs]} " fciqmc_1shot_${a1}_tc.dat) ;\
          echo $4 $5)
    [ -z "$ea1v" ] && continue
    ea2v="0 0"
    [ -z "$a2" ] || ea2v=$(set -- $(grep -E "^${bs[$ibs]} "\
                                   fciqmc_1shot_${a2}_tc.dat) ; echo $4 $5)
    eat=$(set -- $(grep -E "^${bs[$ibs]} " fciqmc_Eat_${s}_tc.dat) ; echo $3 $4)
    set -- $eat $ee $ea1e $ea2e $ev $ea1v $ea2v
    e=$(bc -l <<<"($1)\
                + (-($3) + $na1*($5)    + $na2*($7))\
                - (-($9) + $na1*(${11}) + $na2*(${13}))")
    de=$(bc -l <<<"sqrt( ($2)^2\
                       + ($4)^2    + $na1*($6)^2    + $na2*($8)^2\
                       + (${10})^2 + $na1*(${12})^2 + $na2*(${14})^2 )")
    printf "%-7s %3s %.7f %.7f\n" "${bs[$ibs]}" $((2*nbs[ibs])) "$e" "$de"\
       >> "$f"
  done
done

# Get the difference between atomization energies with and without the no3
# approximation at from same-population enegies.  This populates
# table:no3_Eat_error.
t="table_no3_bias.txt"
echo "#sys-- -basis- bias/mHa" > "$t"
for s in c2 cn n2 o2 ; do
  echo -n .
  case "$s" in
  c2|n2|o2)
    na1=2
    a1=${s:0:1}
    na2=0
    a2="" ;;
  cn)
    na1=1
    na2=1
    a1=c
    a2=n ;;
  esac
  for ((ibs=2; ibs<=6; ibs++)) ; do
    line=$(grep -E "^${bs[$ibs]} " fciqmc_1shot_${s}_tc_no3.dat)
    [ -z "$line" ] && continue
    nw=$(set -- $line ; echo $3)
    en=$(set -- $line ; echo $4 $5)
    # Get the full-dynamics number at the *closest* nw.
    dnw_min=-1
    ef=0
    while read x nwv x x x e de x x ; do
      ((dnw=nwv-nw))
      dnw=${dnw#-}
      if ((dnw_min<0)) || ((dnw<dnw_min)) ; then
        ((dnw_min=dnw))
        ef="$e $de"
      fi 
    done < <(grep -E "^${bs[$ibs]} " fciqmc_${s}_tc.dat)
    [ "$ef" = 0 ] && continue
    ea1n=$(set -- $(grep -E "^${bs[$ibs]} " fciqmc_1shot_${a1}_tc_no3.dat) ;\
          echo $4 $5)
    [ -z "$ea1n" ] && continue
    ea2n="0 0"
    [ -z "$a2" ] || ea2n=$(set -- $(grep -E "^${bs[$ibs]} "\
                                    fciqmc_1shot_${a2}_tc_no3.dat) ; echo $4 $5)
    ea1f=$(set -- $(grep -E "^${bs[$ibs]} " fciqmc_1shot_${a1}_tc.dat) ;\
          echo $4 $5)
    [ -z "$ea1f" ] && continue
    ea2f="0 0"
    [ -z "$a2" ] || ea2f=$(set -- $(grep -E "^${bs[$ibs]} "\
                                   fciqmc_1shot_${a2}_tc.dat) ; echo $4 $5)
    set -- $en $ea1n $ea2n $ef $ea1f $ea2f
    e=$(bc -l <<<"(-($1) + $na1*($3) + $na2*($5))\
                - (-($7) + $na1*($9) + $na2*(${11}))")
    de=$(bc -l <<<"sqrt( ($2)^2 + $na1*($4)^2    + $na2*($6)^2\
                       + ($8)^2 + $na1*(${10})^2 + $na2*(${12})^2 )")
    printf "%-6s %-7s %.2f(%.0f)\n" "$s" "${bs[$ibs]}"\
       "$(bc -l <<<"1000*($e)")" "$(bc -l <<<"100000*($de)")" >> "$t"
  done
done

# Done.
echo

# Copy files to plot directories.
# fig:bsdep-atoms-emin
d=../Fig/bsdep-atoms-emin
if [ -d "$d" ] ; then
  cp "benchmark_Etot.dat" $d/
  for s in c n o ; do
    cp "fciqmc_1shot_${s}_tc.dat" $d/
    cp "fciqmc_1shot_${s}_tc_emin.dat" $d/
  done
fi

# fig:dual-extrap-*
for s in c2 cn n2 o2 ; do
  d=../Fig/dual-extrap-$s
  [ -d "$d" ] || continue
  cp "shci_$s.plot" $d/shci.plot
  cp "fciqmc_$s.dat" $d/fciqmc.dat
  cp "fciqmc_Etot_$s.plot" $d/fciqmc_Etot.plot
done

# fig:extrap-dimers-tc
d=../Fig/extrap-dimers-tc
if [ -d "$d" ] ; then
  for s in c2 cn n2 o2 ; do
    cp "fciqmc_${s}_tc.dat" $d/
    cp "fciqmc_Etot_${s}_tc.plot" $d/
    cp "fciqmc_Eext_${s}_tc.dat" $d/
  done
fi

# fig:bsdep-dimers-emin
d=../Fig/bsdep-dimers-emin
if [ -d "$d" ] ; then
  cp "benchmark_Eat.dat" $d/
  for s in c2 cn n2 o2 ; do
    cp "fciqmc_Eat_${s}_tc.dat" $d/
    cp "fciqmc_Eat_${s}_tc_emin.dat" $d/
  done
fi

# fig:bsdep-dimers-nontc.
d=../Fig/bsdep-dimers-nontc
if [ -d "$d" ] ; then
  cp "benchmark_Eat.dat" $d/
  for s in c2 cn n2 o2 ; do
    cp "fciqmc_Eat_${s}_tc.dat" $d/
    cp "fciqmc_Eat_${s}.dat" $d/
  done
fi

# Clean up.
if ((!keep)) ; then
  rm -rf *.log *.plot fciqmc_1shot_*.dat fciqmc_Eext_*.dat\
     fciqmc_Eat_*.dat shci_Eext_*.dat
fi
