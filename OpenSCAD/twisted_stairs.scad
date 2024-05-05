union(){
  for (i = [1 : abs(10) : 720]) {
    translate([0, 0, (i / 8)]){
      rotate([0, 0, i]){
        cube([10, 50, 4], center=false);
        translate([6, 45, 4]){
          cylinder(r1=2, r2=2, h=12, center=false);
        }
      }
    }
  }
  for (i = [1 : abs(10) : 720]) {
    translate([0, 0, (i / 8)]){
      rotate([0, 0, i]){
        cube([5, 25, 4], center=false);
      }
    }
  }
  difference() {
    difference() {
      translate([0, 0, 15]){
        for (j = [1 : abs(10) : 720 - 10]) {
          hull() {
          translate([0, 0, (j / 8)]){
            rotate([0, 0, j]){
              cube([10, 50, 2], center=false);
            }
          }
          translate([0, 0, ((j + 10) / 8)]){
            rotate([0, 0, (j + 10)]){
              cube([10, 50, 2], center=false);
            }
          }
          }
         }
      }
      cylinder(r1=45, r2=45, h=120, center=false);
    }
    cylinder(r1=45, r2=45, h=120, center=false);
  }
  cylinder(r1=10, r2=10, h=100, center=false);
}