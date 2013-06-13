#!/usr/bin/env python
import time

class LedBorg:
    
    colours = {"maroon":"100",
               "red":"200",
               "pink":"211",
               "olive":"110",
               "yellow":"220",
               "lightyellow":"221",
               "green":"010",
               "limegreen":"020",
               "lightgreen":"121",
               "teal":"011",
               "cyan":"022",
               "lightcyan":"122",
               "navy":"001",
               "blue":"002",
               "lightblue":"112",
               "purple":"101",
               "magenta":"202",
               "fuchsiapink":"212",
               "black":"000",
               "grey":"111",
               "white":"222",
               "azure":"012",
               "violet":"102",
               "brightpink":"201",
               "chartreuse":"120",
               "guppiegreen":"021",
               "orange":"210"}
    def show(self,colour="red"):
        """Show the given colour"""
        # Open the LedBorg driver
        dev = open('/dev/ledborg', 'w')
        # Set LedBorg to the new colour
        dev.write(self.colours[colour])
        # Close
        dev.close()                    

if __name__ == "__main__":
    lb = LedBorg()
    while True:
        for colour in lb.colours:
            print colour
            lb.show(colour)
            time.sleep(2)

