module main(length, width, depth) {
  for (i = [1 : abs(1) : branches]) {
    union(){
      cylinder(r1=(width / reduction), r2=width, h=length, center=false);
      if (depth > 0) {
        translate([0, 0, length]){
          rotate([0, 0, (i * (360 / branches))]){
            rotate([angle, 0, 0]){
              main(length * reduction, width * reduction, depth - 1);
            }
          }
        }
      }

    }
  }

}

length = 30;
width = 7;
depth = 4;
branches = 3;
angle = 30;
reduction = 0.9;
main(length, width, depth);