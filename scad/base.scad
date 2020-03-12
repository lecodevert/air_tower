include <config.scad>;

module screw_hole(angle, offset) {
        rotate([0, 0, angle])
            translate([offset, 0, 0]) {
                    cylinder(h=5, d=3 + clearance);
                    translate([0, 0, -1])
                        cylinder(h=4, d=5.5 + clearance);
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
        // logo
        translate([2.5, 0, -0.1])
            linear_extrude(height=2.5)
                rotate([0, 0, -90])
                    scale([0.08, 0.08, 1])
                        import("lecodevert.svg", center=true);
        // Holes for rubber feets
        a = 45;
        for(i=[0, 90, 180, 270])
            rotate([0, 0, i + a])
                translate([25, 0, -1])
                    cylinder(d=10 + clearance, h=3);
        // holes for cover screws
        for(i=screw_angles)
            screw_hole(i, inner_diameter/2 -3);
        // holes for display stand screws
        screw_hole(display_angle/2, inner_diameter/2 - 2.5);
        screw_hole(-display_angle/2, inner_diameter/2 - 2.5);
        // holes for usb connector breakout board
        for(i=[-1, 1]) {
            translate([-25, i * 4, 0])
                screw_hole(0, 0);
                // clearance for cable connections
                translate([-21, i  * 5, 2])
                    cylinder(h=5, d=2 + clearance);
        }
        // hole for sensor/holder mount
        screw_hole(180, -21.5);
    }
    // front sensor mount
    rotate([0, 0, 90]) {
        difference() {
            union() {
                translate([0, -21.5, pms_height/2 + base_height])
                     cube([5, 5, pms_height], center=true);
                // Barrier to prevent airflow between the inlet and the outlet
                translate([-2.5, -inner_diameter/2 + clearance, base_height])
                    cube([2, 12.5 - clearance, pms_height]);
            }
            translate([0, -21.5, base_height - 1]) {
                cylinder(d=3 + clearance, h=pms_height + 2, $fn=20);
            }
        }
    }
    // a thin layer to act as support for holes
    translate([0, 0, 3])
        cylinder(d=inner_diameter, h=thin_wall);
}

base();
