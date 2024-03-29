# LS Colors settings
function general_colours () {
  LS_COLORS=$LS_COLORS:'di=0;36:' ;
  LS_COLORS=$LS_COLORS:'*.rc=0;37:' ;
  LS_COLORS=$LS_COLORS:'*.urdf=0;37:*.world=0;37:' ;
  LS_COLORS=$LS_COLORS:'*.net=0;37:*.tmap=0;37:' ;
  LS_COLORS=$LS_COLORS:'*.tmule=0;37:*.tmod=0;37:' ;
  LS_COLORS=$LS_COLORS:'*.launch=0;37:*.py=0;37:' ;
  LS_COLORS=$LS_COLORS:'*.txt=0;37:*.xml=0;37:*.md=0;37:' ;
  echo $LS_COLORS ;
}
function now1_colours () { echo $(general_colours):'di=0;32:' ; }
function now2_colours () { echo $(general_colours):'di=0;33:' ; }
function conf_colours () { echo $(general_colours):'*.net=0;31:*.tmap=0;32:*.urdf=0;33:*.world=0;34:' ; }
function rosy_colours () { echo $(general_colours):'*.launch=0;33:*.py=0;34:' ; }
function tmul_colours () { echo $(general_colours):'*.tmule=0;31:*.tmod=0;32:' ; }

# Shortcuts
function g () { if [ -d "/media/$USER/HES15591313" ] ; then ls /media/$USER/HES15591313/ | grep "ghp_" ; else ls ~ | grep ghp_ ; fi ; }
function gs () { git status ; }
function r () { rospack list | grep "$WS_DIR/src" ; }
function tttt () {  clear ; temp=$LS_COLORS ; LS_COLORS=$($1) ; echo "$(tree -C -L 7 --noreport $WWS_DIR)" ; export LS_COLORS=$temp ; }
function ttttf () { clear ; temp=$LS_COLORS ; LS_COLORS=$($1) ; echo "$(tree -fC -L 7 --noreport $WWS_DIR)" ; export LS_COLORS=$temp ; }

function tt ()  { echo "$(tttt general_colours)" ; }
function ttc () { echo "$(tttt conf_colours)" ; }
function ttr () { echo "$(tttt rosy_colours)" ; }
function ttm () { echo "$(tttt tmul_colours)" ; }

function ttz1 () { echo "$( ttttf now1_colours | grep --color=never `pwd` | sed -E 's/\/([A-Za-z0-9_]+\/)+//g' )" ; }
function ttz2 () { echo "$( ttttf now2_colours | grep --color=never `pwd` | sed -E 's/\/([A-Za-z0-9_]+\/)+//g' )" ; }
function ttz () { local_a=$(tz1) ; local_b=$(tz2) ; ws_dir=$(tttt now2_colours); echo "${ws_dir//local_a/local_b}" ; }
#tz;tz1;tz2
