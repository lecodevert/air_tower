include <config.scad>;

/* This is probably too many polygons for poor OpenScad to preview with
   default settings.

   If rendering turns off, you'll need to open Preferences -> Advanced;

   And set 'Turn off rendering' to at least 10000 elements.
*/

use <styled_cylinder.scad>;

// Rounded edges cap
module cap(height) {
    rotate([0, 180, 0])
        difference() {
            rotate_extrude($fn=200)
                translate([(inner_diameter + outer_diameter - height)/4,0,0])
                    circle(height, $fn=50);
            translate([0, 0, - height])
                cylinder(d=outer_diameter + 1, h=height);
        }
    translate([0, 0, -height])
        cylinder(d=(inner_diameter + outer_diameter)/2, h=height);
}

// Mounting ring for base
module mount(size) {
    rotate_extrude(angle=14, $fn=500)
        translate([inner_diameter/2 - size, 0, 0])
            polygon(points= [[size, 0], [0, size], [0, size + 2],
                             [size, size + 2], [size, size]]);
}

module cover() {
    ring_width = inner_diameter - cover_ring_dia;
    window_offset = cover_height - cover_window_height - display_height + 9;
    difference() {
        union() {
            cover_cylinder(inner_diameter = inner_diameter,
                           thickness = (outer_diameter - inner_diameter) / 2,
                           number_of_holes = cover_holes,
                           height = cover_height,
                           layers = cover_layers,
                           holes_spacing = 1.7,
                           style=cover_style,
                           clearance = clearance);
        // mounting pegs
        for(i=screw_angles)
            rotate([0, 0, -i - 7])
                translate([0, 0, cover_height - ring_width - 4 - clearance])
                    mount(ring_width);
        // window "frame"
        rotate([0, 0, -cover_window_angle/2 - 2])
            translate([0, 0, window_offset]) {
                rotate_extrude(angle=cover_window_angle + 4,
                               convexity=10, $fn=100) {
                    translate([outer_diameter/2 - 1.5, 0, 0])
                        difference() {
                            square([(outer_diameter - inner_diameter)/2,
                                    cover_window_height+2], center=true);
                        }
                }
            }
        }
        // holes for inserts
        for(i = screw_angles)
            rotate([0, 0, -i])
                translate([inner_diameter/2 - 3, 0,
                           cover_height - 2 - ring_width]) {
                        cylinder(h=10, d=insert_dia + clearance, $fn=20);
                }
        // display window
        rotate([0, 0, -cover_window_angle/2])
            translate([0, 0, window_offset]) {
                rotate_extrude(angle=cover_window_angle, convexity=10) {
                    translate([outer_diameter/2 - 1.5, 0, 0])
                        difference() {
                            square([5, cover_window_height], center=true);
                        }
                }
            }
        // holes for usb connector
        rotate([0, 0, 180])
            translate([inner_diameter/2, 0, cover_height]) {
                translate([0, 0, -3.5])
                    cube([10, 10, 7], center=true);
                translate([0, 0, -2.5])
                    cube([10, 14, 5], center=true);
            }
    }

    // Built in support for window
    rotate([0, 0, -cover_window_angle/2])
        translate([0, 0, window_offset]) {
            rotate_extrude(angle=cover_window_angle, convexity=10) {
                translate([inner_diameter/2, 0, 0])
                    square([thin_wall, cover_window_height], center=true);
                translate([outer_diameter/2, 0, 0])
                    square([thin_wall, cover_window_height], center=true);
            }
        }
    cap(cover_cap_height);
}

cover();

use <base.scad>;
translate([0, 0, cover_height + 2])
    rotate([180, 0, 0])
        % base();
