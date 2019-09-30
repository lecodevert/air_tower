include <config.scad>;

// Holder used to keep the particulate sensor on top of the tower
module holder(inner_diameter) {
    $fn = 100;
    difference() {
        cylinder(d=inner_diameter - clearance * 2, h=2);
        // Clearance for cable ribbon
        translate([-70, 25, 0])
            cube([inner_diameter, inner_diameter, 3]);

        // clearance for cover insertion
        translate([26, -25, 0]) cube([100, 100, 10]);
        translate([-126, -25, 0]) cube([100, 100, 10]);
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
    // sensor side holder
    for(i = [-1, 1])
        translate([i * (25 + clearance + 0.5), 0, 4])
            cube([1, 30, 5], center=true);
    // sensor back holder
    translate([0, 18, 4])
        cube([20, 1, 5], center=true);
}

holder(inner_diameter);
