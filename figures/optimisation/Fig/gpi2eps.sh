#!/bin/bash

# Compile gnuplot files passed as arguments to .eps.

# Initialize tdir variable.
tdir=""

# Error stop function definition.
quit() {
  echo "$1"
  [ ! -z "$tdir" ] && [ -d "$tdir" ] && rm -rf "$tdir"
  exit 1
}

help_and_quit() {
  echo "Usage: ${0##*/} <dir1> [<dir2> [...]]"
  echo
  echo "This script processes file <dir>/<dir>.gpi into ./<dir>.eps"
  echo
  quit "Quitting."
}

# Checks command line.
(($#<1)) && help_and_quit
for d in "$@" ; do
  case "$d" in
  --help|-h) help_and_quit ;;
  -*) help_and_quit ;;
  esac
done

# Check required programs are available.
for p in gnuplot latex dvips ps2eps ; do
  type -P "$p" >& /dev/null || quit "$p not in PATH."
done

# Loop over .gnuplot files in current directory.
for d in "$@" ; do
  [ -d "$d" ] || { echo "Directory $d does not exist." ; continue ; }
  while [ "${d%/}" != "$d" ] ; do
    d="${d%/}"
  done
  stem="${d##*/}"
  for ext in gpi gnu gnuplot ; do
    [ -f "$d/$stem.$ext" ] && break
    ext=""
  done
  [ -z "$ext" ] && { echo "File $d/$d.gpi not found." ; continue ; }
  f="$stem.$ext"
  echo -n "Processing $d/$f... "

  # See what size plot we want.
  size="5,3"
  (($(grep -cE "^##VTALL *$" "$d/$f" 2>/dev/null)>0)) && size="5,5.5"
  (($(grep -cE "^##TALL *$" "$d/$f" 2>/dev/null)>0)) && size="5,4.5"
  (($(grep -cE "^##tall *$" "$d/$f" 2>/dev/null)>0)) && size="5,3.5"
  (($(grep -cE "^##SHORT *$" "$d/$f" 2>/dev/null)>0)) && size="5,2.5"
  sz=$(grep -E "^##SIZE=" "$d/$f" 2>/dev/null)
  [ ! -z "$sz" ] && size="${sz##*=}"

  # Make a temporary directory.
  tdir=$(mktemp -d 2> /dev/null)
  [ -d "$tdir" ] || quit "Could not create temporary directory."

  # Copy gnuplot file with extra header.
  cat > "$tdir/$f" <<__EOF
set terminal cairolatex eps standalone size $size header "\\\\usepackage{eepic,epic,amsfonts,times,upgreek} \\\\DeclareOldFontCommand{\\\\rm}{\\\\rmfamily}{\\\\mathrm} \\\\DeclareOldFontCommand{\\\\bf}{\\\\bfseries}{\\\\mathbf}"
set output '$stem.tex'
__EOF
  cat "$d/$f" >> "$tdir/$f"

  # Copy relevant data files.
  {
    while read g ; do
      if grep "$g" "$d/$f" >& /dev/null ; then
        cp "$d/$g" "$tdir"/ >& /dev/null
      elif [[ "$g" == *.dat ]] ; then
        cp "$d/$g" "$tdir"/ >& /dev/null
      fi
    done
  } < <(cd "$d" && /bin/ls -1 2> /dev/null)

  # Run gnuplot on file.
  (cd "$tdir" && gnuplot "$f" >& /dev/null) || quit "gnuplot failed."
  [ -f "$tdir/$stem.tex" ] || quit "gnuplot has not produced .tex file."

  # Run latex on latex file.
  (cd "$tdir" && latex "$stem.tex" >& /dev/null)\
     || quit "latex failed."
  [ -f "$tdir/$stem.dvi" ] || quit "latex has not produced .dvi file."

  # Run dvips on dvi file.
  (cd "$tdir" && dvips -o "$stem.ps" "$stem.dvi" >& /dev/null)\
     || quit "dvips failed"
  [ -f "$tdir/$stem.ps" ] || quit "dvips has not produced .ps file."

  # Run ps2eps on ps file.
  (cd "$tdir" && ps2eps -f "$stem.ps" >& /dev/null)
  [ -f "$tdir/$stem.eps" ] || quit "ps2eps has not produced .eps file."

  # Copy eps to current directory.
  mv -f "$tdir/$stem.eps" .
  rm -rf "$tdir"
  echo " done"

done
