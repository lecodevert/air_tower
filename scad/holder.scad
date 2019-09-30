include <config.scad>;

module holder(inner_diameter) {
    $fn = 100;
    difference() {
        cylinder(d=inner_diameter - clearance * 2, h=2);
        // Clearance for cable ribbon
        translate([-70, 25, 0])
            cube([inner_diameter, inner_diameter, 3]);
        // screw hole
        translate([0, 25, 0])
            cylinder(d=3 + clearance, h=11, $fn=20);
    }
    // Barrier to prevent airflow mixing between the inlet and the outlet
    translate([-3, -inner_diameter/2 + clearance, 2])
        difference() {
            cube([6, 11 - clearance, 20 - clearance]);
            for( i = [0, 1]) {
                translate([i * 4, 0, 2])
                    cube([2, 11 - clearance, 20 - clearance]);
                translate([i * 6, 11, 2])
                    rotate([90, 0, 0])
                        cylinder(d=4, h=11);
            }
        }
}

// Holder used to keep the particulate sensor on top of the cover
holder(inner_diameter);
