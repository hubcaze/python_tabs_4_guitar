class Partition:

    def __init__(self, pcanvas):
        self.draw_partition(pcanvas)

    def draw_partition(self, pcanvas):
        """Dessine la partition"""
        pcanvas.create_line(
            30,20,20000,20,
            fill="black")
        pcanvas.create_line(
            30,50,20000,50,
            fill="black")
        pcanvas.create_line(
            30,80,20000,80,
            fill="black")
        pcanvas.create_line(
            30,110,20000,110,
            fill="black")
        pcanvas.create_line(
            30,140,20000,140,
            fill="black")
        pcanvas.create_line(
            30,170,20000,170,
            fill="black")

        pcanvas.create_text(
            10, 20, text="e", font="Times 16 italic bold")

        pcanvas.create_text(
            10, 50, text="B", font="Times 16 italic bold")

        pcanvas.create_text(
            10, 80, text="G", font="Times 16 italic bold")

        pcanvas.create_text(
            10, 110, text="D", font="Times 16 italic bold")

        pcanvas.create_text(
            10, 140, text="A", font="Times 16 italic bold")

        pcanvas.create_text(
            10, 170, text="E", font="Times 16 italic bold")

        for i in range(30,20000,30):
            pcanvas.create_line(
                i,20,i,170,
                fill='grey')

    def convertCanv(self, pcoords):
        # Returns the partition coords with pcoords as canvas coords (from event)
        x = (pcoords[0]//30)-1
        y = (pcoords[1]-20)//30
        if(x < 0):
            x = 0
        if (y < 0):
            y = 0
        elif(y > 5):
            y = 5
        return([x,y])

    def convertPartition(self, pcoords):
        # Returns the canvas coords with pcoords as partition coords (from convertCanv())
        return([(pcoords[0]+1)*30,(pcoords[1]*30+20)])

    def isIn(self, p_converted_coords):
        if (p_converted_coords[0] < 650 and
            p_converted_coords[1] < 5 and
            p_converted_coords[0] > 0 and
            p_converted_coords[1] > 0):
            return True
        return False
