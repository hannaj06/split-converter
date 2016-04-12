from split_converter.converterError import converterError
from split_converter.single_val_converter import single_val_converter
from split_converter.multiple_val_converter import multiple_val_converter
from split_converter.db_controller import db_controller
import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class split_converter:

	def __init__(self, root):
		self.root = root
		self.root.title('velocity converter')
		self.history = []
		Frame(self.root, width=260, height=10).pack()
		Label(self.root, text='select velocity unit to convert:').pack()
		self.combo()
		Button(self.root, text='Quit', command=self.root.quit).pack(side='bottom')
		Button(self.root, text='Save', command=self.save_history).pack(side='bottom')
		Button(self.root, text='Enter', command=self.calculate).pack(side='bottom')


	#returns 500/m split time, kmh, mph, and min/mile equivalent times
	#handles string input, float, and <0 errors
	def calculate(self):
		try:
			if self.box.get() == 'kmh':
				converter = single_val_converter(self.e1.get())

				results = [converter.kmh_to_split(),
				self.e1.get(),
				converter.kmh_to_mph(),
				converter.kmh_to_msplit()]


			elif self.box.get() == 'mph':
				converter = single_val_converter(self.e1.get())

				results = [converter.mph_to_split(),
				converter.mph_to_kmh(),
				self.e1.get(),
				converter.mph_to_msplit()
				] 

			elif self.box.get() == 'sec/500m':
				converter = multiple_val_converter(self.e1.get(), self.e2.get())

				results = [self.e1.get() + ':' + self.e2.get(),
				converter.split_to_kmh(),
				converter.split_to_mph(),
				converter.split_to_msplit()
				]

			elif self.box.get() == 'min/mile':
				converter = multiple_val_converter(self.e1.get(), self.e2.get())

				results = [converter.msplit_to_split(),
				converter.msplit_to_kmh(),
				converter.msplit_to_mph(),
				self.e1.get() + ':' + self.e2.get()
				]


			units = [' sec/500m', ' kmh ', ' mph', ' min/mile']
			i = 0
			for result in results:
				Label(self.root, text = result + units[i]).pack()
				i += 1

			Label(self.root, text = '-----------------------').pack()
			history = {'timestamp': datetime.datetime.now(), 'results': results}
			self.history.append(history)
			print(self.history)
		except converterError as e:
			messagebox.showwarning("Error", str(e))


	def combo(self):
		self.box = ttk.Combobox()
		self.box['values'] = ('sec/500m', 'kmh', 'mph', 'min/mile')
		self.box.pack()
		
		def input_box(event):
			if self.box.get() == 'kmh' or self.box.get() == 'mph':
				Label(self.root, text=self.box.get() + ':').pack()
				self.e1 = Entry(self.root)
				self.e1.pack()
			else:
				Label(self.root, text=self.box.get() + ':').pack()
				self.e1 = Entry(self.root)
				self.e2 = Entry(self.root)
				Label(self.root, text='minute(s):').pack()
				self.e1.pack()
				Label(self.root, text='second(s):').pack()
				self.e2.pack()

		self.box.bind('<<ComboboxSelected>>', input_box)

	def save_history(self):
		db = db_controller()
		db.insert_record(self.history)

	def export_history(self):
		pass

if __name__ == '__main__':
	root = Tk()
	app = split_converter(root)
	root.mainloop()