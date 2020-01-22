include <config.scad>;

module pi_mount(dia=2.5, height=7) {
    for(i = [-1,1]) {
        difference() {
            // Monting pegs
                translate([0, i*11.5, height/2])
                    cube([3, 6, height], center=true);
            // Screw holes through mounting pegs
            translate([0, i*11.5, height - dia/2 - 1])
              rotate([0, 90, 0])
                  cylinder(d=dia + clearance, h=25, center=true);
        }
    }
}

// Holder used to keep the particulate sensor on top of the tower
module holder(inner_diameter) {
    $fn = 100;
    difference() {
        cylinder(d=inner_diameter - clearance * 2, h=1);
        // Clearance for cable ribbon
        translate([-30, 22, 0])
            cube([20, 25, 3], center=true);
        // clearance for cover insertion
        translate([0, 75, 0])
            cube([100, 100, 3], center=true);
        translate([0, -75, 0])
            cube([100, 100, 3], center=true);
        // screw holes
        translate([21.5, 0, 0])
                cylinder(d=3 + clearance, h=11, $fn=20);
        for(i=[-4, 4])
            translate([-25, i, 0])
                    cylinder(d=3 + clearance, h=11, $fn=20);
        // slot for microsd card
        rotate([0, 0, boards_angle])
            translate([0, 0, 0.5])
                cube([25, 15, 2], center=true);
    }

    rotate([0, 0, boards_angle]) {
        // Mounting pegs for Raspberry Pi + enviroplus hat
        for(i=[-7.6, -3 + clearance  *2])
            translate([i, 0, 1]) pi_mount(height=9);
        // Monting pegs for e-paper hat
        translate([0, 18, 1])
            rotate([0, 0, 90])
                pi_mount(dia=3);
    }
}


use <base.scad>;
translate([0, 0, -20 - base_height]) % base();

holder(inner_diameter);
