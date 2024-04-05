p = 6;
height = 10;

difference() {
    union(){
        for(j=[0:height]) {
            translate([0,0,0.99*j])
            rotate([0,0,p*j])
            polyCircle(p);
        }
    }
    translate([0,0,-1])
    cylinder(height+2, p-1, p-1);
}   
module poly(p) {
    difference(){
        cylinder(r=3, h=1, $fn=p);
        translate([0,0,-p/3])
        cylinder(r=2, h=4, $fn=p);
        }
}
module polyCircle(n) {
    for(i=[0:n-1]) {      
        rotate([0,0,(360/n)*i])
        translate([n-2,0,0])
        poly(n);
    }
}