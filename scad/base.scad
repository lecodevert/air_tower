include <config.scad>;

module pi_mount() {
    for(i = [-1,1]) {
        difference() {
            // Monting pegs
            for(j=[-7.6, 7.6, -3 + clearance  *2, 3 - clearance * 2])
                translate([j, i*11.5, 3.5])
                    cube([3, 6, 7], center=true);
            // Screw holes through mounting pegs
            translate([0, i*11.5, 4.5])
              rotate([0, 90, 0])
                  cylinder(d=2.5 + clearance, h=25, center=true);
        }
    }
}

module base() {
    $fn = 100;
    difference() {
        union() {
            difference() {
                // Main port of the base
                cylinder(h=base_height + 2, d=outer_diameter);
                // Cut out for the cover
                translate([-outer_diameter/2, -19, 2])
                    cube([outer_diameter, outer_diameter, cover_height]);
                // Hole for wires
                translate([-10, -40, 4])
                    cube([20, 20, 50]);
                // Hole for connectors
                translate([-7, -22, 8])
                    cube([10, 10, 28]);
            }
            // Mounting plate for the Raspberry Pi
            cylinder(h=4, d=inner_diameter);
            // Mounting peg for the sensor divider
            translate([-5, -29, base_height + 2])
                cube([10, 10, 10]);
        }
        // Holes for rubber feets
        for(i = [-1, 1])
            for(j = [-1, 1])
                 translate([i * 15, j * 15, -1])
                    cylinder(d=10 + clearance, h=3);
        // holes for cover screws
        for(i = [0, 90, 180])
            rotate([0, 0, i])
                translate([inner_diameter/2 -3, 0, 0]) {
                        cylinder(h=5, d=3 + clearance);
                        cylinder(h=3, d=5.5 + clearance);
                }
        // hole for the insert for the sensor plate
        translate([0, -25, base_height + 2])
            cylinder(d=insert_dia, h=11, $fn=20);
    }
    // Mounting pegs for Raspberry Pi
    translate([0, 0, 4]) pi_mount();
}

base();
