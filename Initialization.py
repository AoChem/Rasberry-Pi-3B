def initialization(parent):
	import tkinter as tk
	from tkinter import simpledialog
	global NameOfSts
	global NumOfSts

	p = parent
	NameOfSts = []
	NumOfSts = tk.simpledialog.askinteger("Initializing", "Input the number of states",
										parent=p,
										minvalue=1, maxvalue=3)
	if NumOfSts>=1:
		NameOfSts1 = tk.simpledialog.askstring("Initializing",
												"State1 Name:",
												parent=p)
		NameOfSts.append(NameOfSts1)
		if NumOfSts>=2:
			NameOfSts2 = tk.simpledialog.askstring("Initializing",
													"State2 Name:",
													parent=p)
			NameOfSts.append(NameOfSts2)
			if NumOfSts==3:
				NameOfSts3 = tk.simpledialog.askstring("Initializing",
														"State3 Name:",
														parent=p)
				NameOfSts.append(NameOfSts3)