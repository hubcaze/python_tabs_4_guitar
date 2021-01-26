import tkinter as tk
import partition
from tkinter import filedialog, messagebox

class App:

	CURRENT_POS = [30,20]

	DICO = {} # will contain all positions and values of notes
	POS_LIST = [] # will contain all positions of notes

	def __init__(self):
		self.root = tk.Tk()

		self.scene()

		self.root.mainloop()

	def cancel(self,event=None):
		if(len(self.POS_LIST) != 0):
			coords = self.POS_LIST.pop()
			if(self.DICO[(coords[0],coords[1])] == 0):
				self.canv.delete("nb_"+str(coords[0])+str(coords[1]))
				self.canv.delete("rect_"+str(coords[0])+str(coords[1]))
				self.DICO.pop((coords[0],coords[1]))
			else:
				self.canv.delete("nb_"+str(coords[0])+str(coords[1]))
				self.canv.delete("rect_"+str(coords[0])+str(coords[1]))
				self.DICO[(coords[0],coords[1])] -= 1
				self.canv.create_rectangle(coords[0]-5, 
					coords[1]-5, coords[0]+5, coords[1]+5,
					fill='white', outline='white',tag="rect_"+str(coords[0])+str(coords[1]))
				self.canv.create_text(coords[0],coords[1], text=str(self.DICO[(coords[0],coords[1])]),
					tag="nb_"+str(coords[0])+str(coords[1]))

	def newPartition(self):
		self.canv.delete("all")
		self.Partition = partition.Partition(self.canv)
		self.DICO.clear()
		self.POS_LIST = []
		self.canv.create_oval(28,18,33,23,fill='red',outline='red', tag="visu")

	def openPartition(self):
		file = filedialog.askopenfile(
			mode="r", defaultextension=".tab",
			filetypes=(("tab Files", ".tab"),("All files", ".*")))
		if file:
			self.newPartition()
			for lines in file.readlines():
				parse = lines.rstrip().split(',')
				coords = list(map(int,parse[0].split(" ")))
				for i in range(int(parse[1])+1):
					self.placeNote(coords)
		file.close()

	def savePartition(self):
		file = filedialog.asksaveasfilename(
			defaultextension=".tab",
			filetypes=(("Tab Files", ".tab"),("All files", ".*"))
		)
		if not file:
			return
		try:
			f = open(file, "w", encoding = "utf-8")
		except FileNotFoundError:
			messagebox.showerror(
				title="Error",
				message="Erreur fichier non trouvé"
			)
		except IOError:
			messagebox.showerror(
				title="Error",
				message="Le fichier n'existe pas"
			)
		else:
			for key in self.DICO:
				f.write(str(key[0])+" "+str(key[1])+","+str(self.DICO[key])+"\n")
			f.close()

	def scene(self):
		self.menu_frame = tk.Frame(self.root)
		self.menu_frame.pack(side=tk.TOP, expand=True, fill=tk.X, anchor="n")
		self.menu_fichier = tk.Menubutton(
			self.menu_frame,
			text="File",
			underline=0,
			relief="raised")

		self.deroul_fichier = tk.Menu(self.menu_fichier, tearoff=False)
		self.deroul_fichier.add_command(label="New (Ctrl + N)",
										command=self.newPartition)
		self.deroul_fichier.add_command(label="Open (Ctrl + O)",
										command=self.openPartition)
		self.deroul_fichier.add_command(label="Save (Ctrl + S)",
										command=self.savePartition)
		self.deroul_fichier.add_separator()
		self.deroul_fichier.add_command(label="Quit (Alt + F4)",
										command=self.quit)
		cframe = tk.Frame(self.root)
		cframe.rowconfigure(0, weight=1)
		cframe.columnconfigure(0, weight=1)
		cframe.pack(expand=1, fill="both", padx=5, pady=5)

		self.canv = tk.Canvas(
			cframe,
			width=1000,
			height=200,
			bg="white")

		self.canv.create_oval(28,18,33,23,fill='red',
			outline='red', tag="visu")

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
		self.root.bind("<Control-n>", self.newPartition)
		self.root.bind("<Control-o>", self.openPartition)
		self.root.bind("<Control-s>", self.savePartition)
		self.root.bind("<Control-z>", self.cancel)

		self.menu_fichier.config(menu=self.deroul_fichier)
		self.menu_fichier.pack(side=tk.LEFT)

		self.canv.pack()

	def visualisation(self,event):
		coords = self.Partition.convertCanv([event.x,event.y])
		new_coords = self.Partition.convertPartition(coords)
		delta_x = new_coords[0] - self.CURRENT_POS[0]
		delta_y = new_coords[1] - self.CURRENT_POS[1]
		self.CURRENT_POS = new_coords
		self.canv.move("visu", delta_x, delta_y)

	def addNote(self, event):
		self.placeNote(self.CURRENT_POS)

	def placeNote(self, coords):
		self.canv.create_rectangle(coords[0]-5, 
			coords[1]-5, coords[0]+5, coords[1]+5,
			fill='white', outline='white',tag="rect_"+str(coords[0])+str(coords[1]))
		if(self.DICO.get((coords[0],coords[1])) is not None):
			if(self.DICO[(coords[0],coords[1])] == 21):
				self.canv.create_text(coords[0],coords[1], text="0",
					tag="nb_"+str(coords[0])+str(coords[1]))
				self.DICO[(coords[0],coords[1])] = 0
			else:
				self.canv.create_text(coords[0],coords[1],
					text=str(self.DICO[(coords[0],coords[1])]+1),
					tag="nb_"+str(coords[0])+str(coords[1]))
				self.DICO[(coords[0],coords[1])] += 1
		else:
			self.canv.create_text(coords[0],coords[1], text="0",
				tag="nb_"+str(coords[0])+str(coords[1]))
			self.DICO[(coords[0],coords[1])] = 0
		self.POS_LIST.append(coords)


	def quit(self):
		if messagebox.askyesno('Quit', 'Êtes-vous sûr de vouloir quitter ?'):
			self.root.quit()

if __name__=='__main__':
	App()
	exit(0)
