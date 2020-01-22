include <config.scad>;

$fn = 20;

difference() {
    cylinder(d=5, h=pms_height - 1);
    translate([0, 0, -0.5]) cylinder(d=3 + clearance, h=pms_height);
}
