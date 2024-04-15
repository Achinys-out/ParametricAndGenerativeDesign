size = 20;
iterations = 2;
clearExtra = 0.1;

difference() {
    cube(size = size, center = true);
    for (i = [0: iterations-1]) {
	    currentSize = size / pow(3, i);
        smallSize = (size / 3) / pow(3, i); 
        innerLoopSize = (pow(3, i) - 1) / 2; 
        for (xLoop = [-innerLoopSize:innerLoopSize]) {
            for (yLoop = [-innerLoopSize:innerLoopSize]) {
                for (zLoop = [-innerLoopSize:innerLoopSize]) {
                    for (x = [-smallSize - clearExtra, smallSize + clearExtra]) {
                        for (y = [-smallSize - clearExtra, smallSize + clearExtra]) {
                            for (z = [-smallSize - clearExtra, smallSize + clearExtra]) {
                                translate([
                                    x - xLoop * currentSize, 
                                    y - yLoop * currentSize, 
                                    z - zLoop * currentSize
                                ])
                                cube(size = smallSize + 2 * clearExtra, center = true);
                            }
                        }
                    }
                }
			}
        }
	}
}