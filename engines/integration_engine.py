def installation_steps():
    """
    Returns a simple, easy-to-read list of steps for setting up 
    the solar water heating system on-site.
    """
    return [
        {
            "step": "Site Inspection & Foundation Check",
            "description": (
                "Walk around the roof or ground area where the solar panels will go. "
                "Make sure the ground can hold the weight of the metal frames and water-filled panels. "
                "Check for any nearby trees or buildings that might block the sunlight during the day."
            )
        },
        {
            "step": "Assembling the Metal Support Frames",
            "description": (
                "Fix the metal stand legs firmly to the floor using strong anchor bolts. "
                "Set the tilt angle of the stands exactly as shown in your layout map. "
                "Double-check that all bolts are tight so the frames can withstand strong winds."
            )
        },
        {
            "step": "Mounting the Solar Panels",
            "description": (
                "Lift the solar panels carefully onto the metal stands. "
                "Clamps them down securely to make sure they do not move or slide. "
                "Leave a small gap between the panel rows so they do not shade one another."
            )
        },
        {
            "step": "Laying and Joining the Water Pipes",
            "description": (
                "Connect the water input and output pipes to the panel array. "
                "Use standard rubber washers or glue to stop any water leaks. "
                "Wrap all outside hot-water pipes with thick foam insulation to keep the water from losing its heat."
            )
        },
        {
            "step": "Connecting the Water Pump & Heat Exchanger",
            "description": (
                "Mount the main water pump and connect it to the electrical box. "
                "Pipe the hot water coming from the solar panels into the heat exchanger unit. "
                "Make sure the regular factory water pipes are connected properly to the other side of the exchanger."
            )
        },
        {
            "step": "Setting up the Automatic Safety Valves",
            "description": (
                "Install the 3-way automatic valves to control how the water flows. "
                "Put in the air release valves at the highest points of the pipeline to stop air bubbles. "
                "Attach the pressure release valves to safely vent out extra steam if the system gets too hot."
            )
        },
        {
            "step": "Wiring the Temperature Sensors & Controller",
            "description": (
                "Place the temperature probes inside the solar panels and the water tank. "
                "Run the sensor wires back to the main control panel box. "
                "Turn on the controller screen and test if it reads the hot and cold temperatures correctly."
            )
        },
        {
            "step": "Testing for Leaks and Starting Up",
            "description": (
                "Fill the entire system with water and run the pump for an hour. "
                "Check every joint and valve closely to make sure there are zero water drips. "
                "Once everything is dry and working, open the valves to let the hot solar water mix with your boiler tank."
            )
        }
    ]
