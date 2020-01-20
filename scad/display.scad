include <config.scad>;

$fn=100;

difference() {
    union() {
        translate([0, 0, -20])
        rotate_extrude(angle=150, convexity=10) {
            translate([inner_diameter/2 - 1, 0, 0])
                difference() {
                    square([2, 40], center=true);
                    translate([(2 - 0.3)/2, 0, 0]) square([0.3, 37], center=true);
                }
        }

        translate([inner_diameter/2 - 2.5, 0, -40]) cylinder(d=5, h=52);
        rotate([0, 0, 150]) translate([inner_diameter/2 - 2.5, 0, -40]) cylinder(d=5, h=52);
    }
    translate([inner_diameter/2 - 2.5, 0, -40]) cylinder(d=3, h=52);
    rotate([0, 0, 150]) translate([inner_diameter/2 - 2.5, 0, -40]) cylinder(d=3, h=52);
    // flatten this edge for clearance for the ribbon
    translate([inner_diameter/2 - 0.15, 0, -20]) cube([0.3, 3, 37], center=true);
    // notch for the display ribbon
    translate([inner_diameter/2 - 2.5, -3, -20]) cube([5, 5, 20], center=true);
}
