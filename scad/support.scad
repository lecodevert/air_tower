include <config.scad>;

$fn = 20;

difference() {
    union() {
        // main body
        translate([0, 0, (pms_height - 1)/2])
            cube([5, 5, pms_height - 1], center=true);
        translate([5, 0, 0.5])
            cube([5, 5, 5,], center=true);
        translate([0, -3, 6])
            cube([5, 5, 5,], center=true);
        translate([0, -3, 17.5])
            cube([5, 5, 5,], center=true);
    }
    // hole for screw
    translate([0, 0, -0.5])
        cylinder(d=3 + clearance, h=pms_height);
    //  notch for switch
    translate([0, -2.8, 11.75])
        cube([5, 2.5, 6.5], center=true);
}
