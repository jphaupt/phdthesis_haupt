#!/bin/bash
# Processes data in rawdata.dat and prints results to stdout (these are the
# contents of results.dat).

infile="rawdata.dat"

# Count sets.
((i=0))
((nset=0))
((iline=0))
prev_basis=""
while : ; do
  read line || break
  ((iline++))
  [ "${line:0:1}" = "#" ] && continue
  set -- $line
  if (($#<4)) ; then
    ((i=0))
    continue
  fi
  if ((i==0)) ; then
    ((nset++))
    set_label[$nset]="$1 $2"
    ((set_nskip[nset]=iline-1))
    if [ ! -z "$prev_basis" ] && [ "$2" != "$prev_basis" ] ; then
      ((set_spacer[nset]=1))
    else
      ((set_spacer[nset]=0))
    fi
    prev_basis="$2"
  fi
  ((i++))
done < "$infile"

cat <<EOF
#           ----------rw.var.min---------- ---------var.Eref.min--------- ---------urw.var.min---------- -----------MAD.min------------ ------------E.min-------------
#sy -basis- -------<E_L>---- ----varE----- -------<E_L>---- ----varE----- -------<E_L>---- ----varE----- -------<E_L>---- ----varE----- -------<E_L>---- ----varE-----
EOF
fmt="%-2s  %-7s %9.4f %6.4f %6.4f %6.4f %9.4f %6.4f %6.4f %6.4f %9.4f %6.4f %6.4f %6.4f %9.4f %6.4f %6.4f %6.4f %9.4f %6.4f %6.4f %6.4f"

# Loop over sets.
for ((iset=1; iset<=nset; iset++)) ; do

  output_line="${set_label[$iset]}"

  # Loop over data columns.
  for ((icol=1; icol<=10; icol++)) ; do

    {
      # Skip lines up to set.
      for ((iline=1; iline<=set_nskip[iset]; iline++)) ; do
        read line
      done
      i=0
      while : ; do
        read line || break
        [ "${line:0:1}" = "#" ] && continue
        set -- $line
        (($#<4)) && break
        shift 3
        xx=${@:$((2*icol-1)):1}
        ((i++))
        x[$i]=$(printf "%.20f" $xx)
      done
    } < "$infile"

    # Get the mean.
    ((n=i))
    sum_x=0
    for ((i=1; i<=n; i++)) ; do
      xx=${x[$i]}
      sum_x="$sum_x + ($xx)"
    done
    ave_x=$(bc -l <<<"($sum_x)/$n")

    # Get various measures of spread.
    sum_dx2=0
    for ((i=1; i<=n; i++)) ; do
      dx=$(bc -l <<<"${x[$i]}-($ave_x)")
      sum_dx2="$sum_dx2 + ($dx)^2"
    done
    stddev_x=$(bc -l <<<"sqrt(($sum_dx2)/($n-1))")

    # Add to ouput line.
    output_line="$output_line $ave_x $stddev_x"

  done

  # Print line.
  ((set_spacer[iset])) && printf "\n\n"
  printf "$fmt\n" $output_line

done
cat <<EOF
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
EOF
