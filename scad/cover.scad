/* $fn = 50; */

lozenge_size = 5;
lozenge_radius = 1;
lozenge_spacing = 2;
number_of_lozenges = 20;
stack_number = 10;

function lozenge_total_size() = lozenge_size * sqrt(2) + lozenge_radius*2;

echo(lozenge_total_size=lozenge_total_size());

function stack_total_height() = (lozenge_total_size() + lozenge_spacing) * stack_number;

echo(stack_total_height=stack_total_height());

function cylinder_radius() = (lozenge_total_size() + lozenge_spacing)/ (2 * tan( 180 / number_of_lozenges));

total_radius = cylinder_radius();
echo(radius=total_radius);

module lozenge(size, radius, height) {
    rotate([0, 90, 0])
    linear_extrude(height=height) offset(r=radius) rotate([0, 0, 45]) square(size, center=true);
}


module lozenge_stack(inner_diameter) {
    difference() {
        angle = 360 / number_of_lozenges;
        for (j=[0: 1: stack_number]) {
            step =  j % 2 == 0 ? angle : angle / 2;
            rotate([0, 0, step])
                translate([0, 0, j * (lozenge_total_size()/2 + lozenge_spacing)])
                    for(i=[0: angle: 360 - angle]) {
                        rotate([0, 0, i]) lozenge(lozenge_size, lozenge_radius, total_radius);
                    }
        }
        translate([0, 0, - lozenge_total_size() / 2 - lozenge_spacing]) cylinder(h=stack_total_height(), d=inner_diameter);
    }
}

/* difference() { */
/*     cylinder(r=total_radius, h=150); */
/*     lozenge_stack(65); */
/* } */
lozenge_stack(65);
