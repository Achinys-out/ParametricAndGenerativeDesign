module screwHead(height, headHeight, radius) {
    translate([0, 0, height]) {
        difference() {
            topWidth = (radius + 3) * 2;
            height = headHeight + 2;
            cylinder(headHeight, radius, radius + 5);
            union() {
                translate([0,0,height+1]) {
                    cube([topWidth, 2, height], center=true);
                };
                rotate([0,0,90]) {
                    translate([0,0,height+1])
                    cube([topWidth, 2, height], center=true);
                }
            }
        }
    };
}

module screwTip(radius) {
    rotate([0,180,0]) {
        cylinder(1, radius, radius-1);
    }
}

module screwSpiral(height, radius) {
    translate([0,0,3]) {
        linear_extrude(height = height-9, scale = 1.1, twist = 4000) {
            translate([radius/2,radius/2,0]) {
                circle(2);
            }
        };
    }
}
        

module screw(height, radius, headHeight) {
    union() {
        // base
        cylinder(height, radius, radius);
        
        // head
        screwHead(height, headHeight, radius);

        // spiral
        screwSpiral(height, radius);

        // tip
        screwTip(radius);
    }
}

screw(height = 50, radius = 4, headHeight = 8);