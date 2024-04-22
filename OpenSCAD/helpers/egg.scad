eggConstant = 1.28;

module ellipse(width, height) {
  scale([1, height/width, 1]) circle(r=width/2);
}

module eggOutline(width, size){
    translate([0, width/2, 0]) union(){
        rotate([0, 0, 180]) difference(){
            ellipse(width, 2*size-width);
            translate([-size/2, 0, 0]) square(size);
        }
        circle(r=width/2);
    }
}

module egg(size){
    width = size / 1.28;
    rotate_extrude()
        difference(){
            eggOutline(width, size);
            translate([-size, 0, 0]) square(2*size, center=true);
        }
}

// egg(30);