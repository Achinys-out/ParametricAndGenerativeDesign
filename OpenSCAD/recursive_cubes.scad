module recursive_cube(x, y, z, u) {
  union(){
    translate([x, y, z]){
      cube([u, u, u], center=true);
    }
    if (u >= 4) {
      union(){
        recursive_cube(x + u / divisor, y + u / divisor, z + u / divisor, u / divisor);
        recursive_cube(x - u / divisor, y + u / divisor, z + u / divisor, u / divisor);
        recursive_cube(x - u / divisor, y - u / divisor, z + u / divisor, u / divisor);
        recursive_cube(x + u / divisor, y - u / divisor, z + u / divisor, u / divisor);
      }
    }

  }
}

divisor = 2;
rotate([0, 180, 0]){
  recursive_cube(0, 0, 0, 100);
}