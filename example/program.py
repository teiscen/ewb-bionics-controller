# main.py
from cli_controller import SimulinkMessage
from control_hub import ControlHub
from interface import MockInterface, UDPInterface


# ----- EXAMPLE
# 
# REMEMBER TO CREATE A SCRIPT TO FETCH THE REQUIRED FILES 
def main():
    # Define the control_hub with whatever interface you wrote.
    # Here, I've included the MockInterface (MAKE LINK) which prints out whatever it receives    
    hub = ControlHub({
        'mock': MockInterface(),
        # 'twin': UDPInterface('localhost', 50007),
    })
    # After you create control_hub you must enable it (name has to match).
    hub.enable('mock')
    # hub.enable('twin')

    # Connect all of the ENABLED interfaces. 
    hub.connect_all()

# ----- CODE BELOW THIS LINE DEPENDS ON YOUR CLASS  
    # For the CLI program I've written, I give it control_hub object
    # so that it may communicate with the interfaces we enabled above.
    # You're program will probably follow a similar use case.
    shell = SimulinkMessage(hub)

    # I begin the CLI loop
    shell.cmdloop()

# ----- NOTE: Remember to disconnect all the interfaces.
    hub.disconnect_all()

if __name__ == '__main__':
    main()


