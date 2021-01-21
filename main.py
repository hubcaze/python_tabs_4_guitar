import tkinter as tk
import partition
from tkinter import filedialog, messagebox

class App:

	CURRENT_POS = [30,20]

	DICO = {} # will contain all positions and values of notes

	def __init__(self):
		self.root = tk.Tk()

		self.scene()

		self.canv.create_oval(28,18,33,23,fill='red',outline='red', tag="visu")

		self.root.mainloop()

	def openPartition(self):
		pass

	def scene(self):
		cframe = tk.Frame(self.root)
		cframe.rowconfigure(0, weight=1)
		cframe.columnconfigure(0, weight=1)
		cframe.pack(expand=1, fill="both", padx=5, pady=5)

		self.canv = tk.Canvas(
			cframe,
			width=1000,
			height=200,
			bg="white")

		self.Partition = partition.Partition(self.canv)

		hbar = tk.Scrollbar(cframe, orient="horizontal")

		self.canv.configure(
			xscrollcommand=hbar.set,
			scrollregion=(0, 0, 20000, 600),
		)

		hbar.configure(command=self.canv.xview)
		hbar.pack(side="bottom")

		self.canv.bind("<Motion>", self.visualisation)
		self.canv.bind("<Button-1>", self.addNote)
		self.root.protocol("WM_DELETE_WINDOW", self.quit)

		self.canv.pack()

	def visualisation(self,event):
		coords = self.Partition.convertCanv([event.x,event.y])
		new_coords = self.Partition.convertPartition(coords)
		delta_x = new_coords[0] - self.CURRENT_POS[0]
		delta_y = new_coords[1] - self.CURRENT_POS[1]
		self.CURRENT_POS = new_coords
		self.canv.move("visu", delta_x, delta_y)

	def addNote(self, event):
		coords = self.CURRENT_POS
		self.canv.create_rectangle(coords[0]-5, coords[1]-5, coords[0]+5, coords[1]+5,fill='white', outline='white')
		if(self.DICO.get((coords[0],coords[1])) is not None):
			if(self.DICO[(coords[0],coords[1])] == 21):
				self.canv.create_text(coords[0],coords[1], text="1")
				self.DICO[(coords[0],coords[1])] = 1
			else:
				self.canv.create_text(coords[0],coords[1], text=str(self.DICO[(coords[0],coords[1])]+1))
				self.DICO[(coords[0],coords[1])] += 1
		else:
			self.canv.create_text(coords[0],coords[1], text="1")
			self.DICO[(coords[0],coords[1])] = 1


	def quit(self):
		if messagebox.askyesno('Quit', 'Êtes-vous sûr de vouloir quitter ?'):
			self.root.quit()

if __name__=='__main__':
	App()
	exit(0)
