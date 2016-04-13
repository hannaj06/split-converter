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
		Button(self.root, text='Enter', command=self.calculate).pack(side='bottom')
		self.drop_down()




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
			history = {'timestamp': datetime.datetime.now().strftime("%d-%m-%y - %H:%M.%S"), 'results': results}
			self.history.append(history)

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

	#postcondition: saves all nonduplicate entries into history table of db
	def save_history(self):
		db = db_controller()
		db.insert_record(self.history)
		db.close()
		print('history saved to db')

	#postcondition: split_converter.txt is exported with all records in the history table of db
	def export_history(self):
		db = db_controller()
		history = db.fetch()
		db.close()
		export_file = open('split_converter.txt', 'w')
		export_file.write('split converter historcal data\n\n')
		export_file.write('mm-dd-yy - hh:mm.ss | [min/500m, kmh, mph, min/mile]\n')
		export_file.write('------------------------------------------------------------\n')
		for record in history:
			export_file.write(str(record[0]) + '  |  ' + str(record[1]) + '\n')
		print('history exported to split_converter.txt')

	#precondition: history table exists in split_converter db
	#postcondition: table is dropped and recreated thus clearing all previous entries
	def clear_history(self):
		db = db_controller()
		db.clear_db()
		db.close()

	def drop_down(self):
		menu_bar = Menu(self.root)
		self.root.config(menu = menu_bar)
		tools_menu = Menu(menu_bar) 
		menu_bar.add_cascade(label='tools', menu = tools_menu)

		tools_menu.add_command(label = 'save', command = self.save_history)
		tools_menu.add_command(label = 'export_history', command = self.export_history)
		tools_menu.add_command(label = 'clear histry', command = self.clear_history)

if __name__ == '__main__':
	root = Tk()
	app = split_converter(root)
	root.mainloop()