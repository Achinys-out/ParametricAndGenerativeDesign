$fn=50;

module main(head_height, head_radius, body_height, body_radius, tip_height) {
  translate([0, 0, body_height]){
    union(){
      head(head_radius, head_height);
      {
        translate([0, 0, (-(body_height / 2))]){
          cylinder(r1=body_radius, r2=body_radius, h=body_height, center=true);
        }
      }
      {
        translate([0, 0, (-(body_height + tip_height))]){
          cylinder(r1=0, r2=body_radius, h=tip_height, center=false);
        }
      }
      translate([0, 0, (-body_height-1)]){
        scale([0.45, 0.45, 0.6]){
          spiral2(body_height);
        }
      }
    }
  }
}

module head(radius, height) {
  union(){
    head_cylinder_height = height * (2 / 3);
    difference() {
      {
        cylinder(r1=radius, r2=radius, h=(height / 3), center=false);
      }

      head_cut(radius);
    }
    translate([0, 0, (-head_cylinder_height)]){
      {
        cylinder(r1=(radius / 3), r2=radius, h=head_cylinder_height, center=false);
      }
    }
  }
}

module head_cut(radius) {
  cut_radius = radius * (5 / 4);
  cut_width = radius / 5;
  union(){
    rotate([0, 0, 90]){
      cube([cut_radius, cut_width, 100], center=true);
    }
    cube([cut_radius, cut_width, 100], center=true);
  }
}

module spiral1(b_height, twist) {
  translate([0, 0, 2]){
    linear_extrude( height=(b_height * (5 / 3)), twist=twist, scale=[1, 1], center=false){
      translate([1, 7, 0]){
        circle(r=3);
      }
    }
  }
}

module spiral2(b_height) {
  translate([0, 0, b_height]){
    for (i = [0 : abs(3) : 360 - 3]) {
      hull() {
      rotate([0, 0, (i * 6)]){
        translate([0, 0, (i / 10)]){
          translate([2, 0, -10]){
            rotate([15, 0, 0]){
              difference() {
                rotate([2, 0, 0]){
                  translate([1, 0, -10]){
                    {
                      $fn=12;
                      cylinder(r1=5, r2=5, h=1, center=true);
                    }
                  }
                }

                cube([10, 5, 10], center=true);
                cube([10, 5, 10], center=true);
              }
            }
          }
        }
      }
      rotate([0, 0, ((i + 3) * 6)]){
        translate([0, 0, ((i + 3) / 10)]){
          translate([2, 0, -10]){
            rotate([15, 0, 0]){
              difference() {
                rotate([2, 0, 0]){
                  translate([1, 0, -10]){
                    {
                      $fn=12;
                      cylinder(r1=5, r2=5, h=1, center=true);
                    }
                  }
                }

                cube([10, 5, 10], center=true);
                cube([10, 5, 10], center=true);
              }
            }
          }
        }
      }
      }
     }
  }
}

main(head_height=5, head_radius=7, body_height=23, body_radius=3, tip_height=4);