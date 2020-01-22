module cover_cylinder(inner_diameter, thickness, number_of_holes,
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
        } else if (style == "slits") {
            for(i=[1:1:number_of_holes]) {
                rotate([0, 0, 360 / number_of_holes * i])
                    translate([inner_diameter / 2 - 0.5, 0, height * 0.05])
                        cube([(outer_diameter - inner_diameter)/2 + 1, polygon_side/2, ,height * 0.9]);
            }
        }
    }
}

