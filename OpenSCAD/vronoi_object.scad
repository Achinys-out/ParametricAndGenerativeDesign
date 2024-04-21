module voronoiObject() {
    n = 22;             // number of points to generate - less = faster rendering, but less voronoid object, more = slower rendering, but mode voronoid object
    range = 32;         // main object radius
    points = points(n, -range, range); // generating 3D points

//// exmaple1:
//    difference() {
//        sphere(range, $fn=30);
//        pointsToVoronoiObjects(pts=points, range=range, spacing=1, rounded=6);
//        sphere(range-2, $fn=10);    
//    };

//// exmaple2:
//    union() {
//        intersection() {
//            cube(range*2, center=true);
//            pointsToVoronoiObjects(pts=points, range=range, spacing=1, rounded=6);
//        };
//        minkowski() {
//            cube((range*2-range), center=true);
//            sphere(r=6, $fn=10);
//        }
//    };
    
//// exmaple3:
//    union() {
//        intersection() {
//            sphere(range, $fn=20);
//            pointsToVoronoiObjects(pts=points, range=range, spacing=2, rounded=6);
//        };
//        sphere(range-10, $fn=10);    
//    };

}

module pointsToVoronoiObjects(pts, range, spacing, rounded){
    for (p = pts) {
        minkowski() {
        intersection_for(p1 = pts) {
            if (p!=p1) {
                yAngle = atan2(p1[2] - p[2], distance(p - p1)); 
                zAngle = atan2(p[1] - p1[1], p[0] - p1[0]);
          
                translate((p+p1)/2 - normalize(p1-p) * (spacing+rounded)) {
                    rotate([0, yAngle, zAngle])
                    translate([0,-range, -range])
                    cube([range, 2*range, 2*range]);
                }
            }
        }
        sphere(r=rounded, $fn=10);
        };
    }
}

// helper functions
function distance(v) = sqrt((v[0] * v[0]) + (v[1] * v[1]) + (v[2] * v[2])); 
function normalize(v) = v / (distance(v));
function points(n, minVal, maxVal) = [for (i = [0 : 1 : n-1]) rands(minVal, maxVal, 3)];
    
voronoiObject();