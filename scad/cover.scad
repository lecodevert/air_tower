/* $fn = 100; */

cover_height=30;

lozenge_size = 5;
lozenge_radius = 1;
lozenge_spacing = 2;
number_of_lozenges = 20;
stack_number = 3;

function lozenge_total_size() = lozenge_size * sqrt(2) + lozenge_radius*2;

echo(lozenge_total_size=lozenge_total_size());

function stack_total_height() = (lozenge_total_size() + lozenge_spacing) * stack_number;

echo(stack_total_height=stack_total_height());

function cylinder_radius() = (lozenge_total_size() + lozenge_spacing)/ (2 * tan( 180 / number_of_lozenges));

total_radius = cylinder_radius();
echo(radius=total_radius);

module lozenge(size, radius, height) {
    translate([height, 0, 0]) rotate([0, 90, 180])
    linear_extrude(height=height, scale=[0, 0]) offset(r=radius, $fn=10) rotate([0, 0, 45]) square(size, center=true);
}


module lozenge_stack(inner_diameter, outer_diameter) {
    angle = 360 / number_of_lozenges;
    difference() {
       translate([0, 0, lozenge_total_size() / 2 + lozenge_spacing]) {
            for (j=[0: 1: stack_number]) {
                step =  j % 2 == 0 ? angle : angle / 2;
                rotate([0, 0, step])
                    translate([0, 0, j * (lozenge_total_size()/2 + lozenge_spacing)])
                        for(i=[0: angle: 360 - angle]) {
                            rotate([0, 0, i]) lozenge(lozenge_size, lozenge_radius, total_radius);
                        }
            }
        }
        cylinder(h=stack_total_height(), d=inner_diameter);
        difference() {
            cylinder(d=1000, h=stack_total_height());
            cylinder(d=outer_diameter, h=stack_total_height());
        }
    }
}

difference() {
    cylinder(d=64, h=cover_height, $fn=100);
    cylinder(d=58, h=cover_height+1, $fn=100);
    lozenge_stack(57, 61.3);
    rotate([0, 0, 360 / number_of_lozenges / 2]) lozenge_stack(61, 64.5);
}

