
# Building
function rebuild() {
  cd $WS_DIR
  rm -r build/
  rm -r devel/
  rosdep install --from-paths src --ignore-src -r -y
  catkin_make
  source ./devel/setup.bash
  cd $OLDPWD
}

function frame () {
  rosrun tf view_frames
  evince frames.pdf
}
