module fractSpheres(position=[0,0,0], size=100, iteration=3, direction=-1) {
	currentSize=size/2;
	distance=(currentSize+size)/2;
	translate(position) {
        sphere(size*2/3, $fn=8);
    };
    union() {
        if(iteration > 0) {
            if(direction != 0) {
                fractSpheres(position-[distance,0,0],currentSize,iteration-1,1);
            }
            if(direction != 1) {
                fractSpheres(position+[distance,0,0],currentSize,iteration-1,0);
            }
            if(direction != 2) {
                fractSpheres(position-[0,distance,0],currentSize,iteration-1,3);
            }
            if(direction != 3) {
                fractSpheres(position+[0,distance,0],currentSize,iteration-1,2);
            }
            if(direction != 4) {
                fractSpheres(position-[0,0,distance],currentSize,iteration-1,5);
            }
            if(direction != 5) {
                fractSpheres(position+[0,0,distance],currentSize,iteration-1,4);
            }
        }
    }
}

fractSpheres();