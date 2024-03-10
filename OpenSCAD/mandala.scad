rings = 6;
degree = 0;
for (i = [1 : abs(1) : rings]) {
  degree = i * (360 / rings);
  rotate([0, 0, degree]){
    translate([0, 20, 0]){
      // torus
      rotate_extrude($fn=20) {
        translate([30, 0, 0]) {
          circle(r=4, $fn=10);
        }
      }
    }
  }
}