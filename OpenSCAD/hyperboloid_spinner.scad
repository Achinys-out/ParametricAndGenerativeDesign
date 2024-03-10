for (i = [1 : abs(10) : 360]) {
  rotate(a=i, v=[50, 50, 50]){
    cube([50, 50, 50], center=true);
  }
}