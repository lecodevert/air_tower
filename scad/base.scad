include <config.scad>;

module pi_mount(dia=2.5) {
    for(i = [-1,1]) {
        difference() {
            // Monting pegs
                translate([0, i*11.5, 3.5])
                    cube([3, 6, 7], center=true);
            // Screw holes through mounting pegs
            translate([0, i*11.5, 4.5])
              rotate([0, 90, 0])
                  cylinder(d=dia + clearance, h=25, center=true);
        }
    }
}

module base() {
    $fn = 100;
    difference() {
        union() {
            difference() {
                // Main part of the base
                cylinder(h=base_height/2, d=outer_diameter);
                // Cut out for the cover
                translate([0, 0, 2])
                    cylinder(d=outer_diameter + 1, h=cover_height);
            }
            // Mounting plate for the Raspberry Pi
            cylinder(h=base_height, d=inner_diameter);
        }
        // Holes for rubber feets
        for(i = [-1, 1])
            for(j = [-1, 1])
                 translate([i * 15, j * 15, -1])
                    cylinder(d=10 + clearance, h=3);
        // holes for cover screws
        for(i = [55, 235])
            rotate([0, 0, i])
                translate([inner_diameter/2 -3, 0, 0]) {
                        cylinder(h=5, d=3 + clearance);
                        cylinder(h=3, d=5.5 + clearance);
                }
        // holes for display stand screws
        rotate([0, 0, 39])
            translate([inner_diameter/2 - 2.5, 0, 0]) {
                cylinder(h=5, d=3 + clearance);
                cylinder(h=3, d=5.5 + clearance);
            }
        rotate([0, 0, 39 - 150])
            translate([inner_diameter/2 - 2.5, 0, 0]) {
                cylinder(h=5, d=3 + clearance);
                cylinder(h=3, d=5.5 + clearance);
            }
        // slot for microsd card
        translate([-5, -8, 0])
            cube([5, 15, base_height + 1]);
        // holes for usb connector breakout board
        translate([-25, 0, 0]) {
            for(i=[-4, 4])
                // screws
                translate([0, i, 0])
                    cylinder(h=5, d=3 + clearance);
            for(i=[-5, 5])
                // clearance for cable connections
                translate([4, i, 2])
                    cylinder(h=5, d=2 + clearance);
        }
    }
    // Mounting pegs for Raspberry Pi + enviroplus hat
    /* for(i=[-7.6, 7.6, -3 + clearance  *2, 3 - clearance * 2]) */
    for(i=[-7.6, -3 + clearance  *2])
        translate([i, 0, base_height]) pi_mount();
    // Monting pegs for e-paper hat
    translate([0, 18, base_height])
        rotate([0, 0, 90])
            pi_mount(dia=3);
}

base();
