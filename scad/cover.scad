include <config.scad>;

/* This is probably too many polygons for poor OpenScad to preview with
   default settings.

   If rendering turns off, you'll need to open Preferences -> Advanced

   And set 'Turn off rendering' to at least 10000 elements
*/

module latticed_cylinder(inner_diameter, thickness, number_of_holes,
                         holes_spacing, height, layers, clearance = 0.1,
                         style="lattice") {
    outer_diameter = inner_diameter + thickness * 2;
    layer_thickness = thickness / layers * 2;
    polygon_side = 2 * (inner_diameter/2 + thickness) *
        sin( 180 / number_of_holes);
    lozenge_radius = 1;
    lozenge_size = polygon_side - holes_spacing * 2 - lozenge_radius * 2;
    stack_number = round(height / (polygon_side - 1.5 * holes_spacing));

    // Base 2D shape
    module lozenge(size, radius, height) {
        translate([height, 0, 0]) rotate([0, 90, 180])
            linear_extrude(height=height, scale=[0, 0])
                offset(r=radius, $fn=10)
                    rotate([0, 0, 45])
                        square(size, center=true);
    }

    // Row of lozenge spikes around the center
    module lozenge_stack(inner_diameter, outer_diameter) {
        angle = 360 / number_of_holes;
        difference() {
            translate([0, 0, polygon_side / 2 + holes_spacing]) {
                for (j=[1: 1: stack_number]) {
                    step =  j % 2 == 0 ? angle : angle / 2;
                    rotate([0, 0, step])
                        translate([0, 0, (j - 1) *
                            (polygon_side/2 + holes_spacing)])
                            for(i=[0: angle: 360 - angle]) {
                                rotate([0, 0, i])
                                    lozenge(lozenge_size,
                                            lozenge_radius,
                                            outer_diameter/2);
                            }
                }
            }
            cylinder(h=height, d=inner_diameter);
        }
    }

    difference() {
        cylinder(d=outer_diameter, h=height, $fn=500);
        translate([0, 0, -0.5])
            cylinder(d=inner_diameter, h=height+1, $fn=500);
        if (style == "lattice") {
            for(i=[1:1:layers]) {
                inner_dia = inner_diameter + layer_thickness * (i - 1)
                    - clearance;
                outer_dia = inner_diameter + layer_thickness * i + clearance;
                rotate([0, 0, 360 / number_of_holes / layers * i])
                    lozenge_stack(inner_dia, outer_dia);
            }
        }
    }
}

// Rounded edges cap
module cap() {
    rotate([0, 180, 0]) rotate_extrude($fn=100) {
        difference() {
            translate([32.5,0,0]) circle(2, $fn=50);
            translate([0,-2,0]) square([70/2, 2]);
        }
        square([66/2, 2]);
    }
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
    window_offset = cover_height - cover_window_height - display_height - 2 + 10;
    difference() {
        union() {
            latticed_cylinder(inner_diameter = inner_diameter,
                              thickness = (outer_diameter - inner_diameter) / 2,
                              number_of_holes = cover_holes,
                              height = cover_height,
                              layers = cover_layers,
                              holes_spacing = 1.7,
                              style=cover_style,
                              clearance = clearance);
        // screws holes
        for(i=screw_angles)
            rotate([0, 0, -i - 7])
                translate([0, 0, cover_height - ring_width - 4 - clearance])
                    mount(ring_width);
        // window "frame"
        rotate([0, 0, -cover_window_angle/2 - 1])
            translate([0, 0, window_offset]) {
                rotate_extrude(angle=cover_window_angle + 2,
                               convexity=10, $fn=100) {
                    translate([outer_diameter/2 - 1.5, 0, 0])
                        difference() {
                            square([4, cover_window_height+2], center=true);
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
    cap();
}

cover();
use <base.scad>;
translate([0, 0, cover_height + 2])
    rotate([180, 0, 0])
        % base();
size = inner_diameter - cover_ring_dia;
polygon(points= [[size, 0], [0, size], [0, size + 2], [size, size + 2], [size, size]]);
