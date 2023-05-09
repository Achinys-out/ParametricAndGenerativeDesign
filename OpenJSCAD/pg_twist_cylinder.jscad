var p = 6;
var height = 10;

function main() {
    var objects = new Array();
    for(var i = 0; i < height; i++) {
        objects[i] = 
        rotate([0,0,p*i], 
        translate([0,0,0.99*i], 
        polyCircle(p)));
    }
    return difference(union(objects),cylinder({h:height+2, r: p-1, fn: 16}));

}

function poly(p) {
    return difference(
        cylinder({h:1, r: 3, fn: p}), 
        cylinder({h:1, r: 2, fn: p}));
}

function polyCircle(n) {
    var objects = new Array();
    for(var i = 0; i < n; i++) {
        objects[i] = 
        rotate([0,0,(360/n)*i], 
        translate([n-2,0,0], 
        poly(n)));
    }
    return union(objects);
}