def generate_pid():

    pid = """

digraph G {

rankdir=LR;

Collector [shape=box];
Pump [shape=circle];
HX [shape=diamond];
Tank [shape=cylinder];
Boiler [shape=box];

Collector -> Pump;
Pump -> HX;
HX -> Tank;
Boiler -> HX;

}

"""

    return pid