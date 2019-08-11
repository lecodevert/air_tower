clearance = 0.1;

module holder(inner_diameter) {
    $fn = 100;
    difference() {
        cylinder(d=inner_diameter - clearance * 2, h=2);
        translate([-inner_diameter/2, 25, 0])
            cube([inner_diameter, inner_diameter, 3]);
    }
    translate([-3, -inner_diameter/2 + clearance, 2])
        difference() {
            cube([6, 11 - clearance, 20 - clearance]);
            for( i = [0, 1]) {
                translate([i * 4, 0, 2]) cube([2, 11 - clearance, 20 - clearance]);
                translate([i * 6, 11, 2]) rotate([90, 0, 0]) cylinder(d=4, h=11);
            }
        }
}

holder(63);
