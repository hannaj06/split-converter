from split_converter.converterError import converterError
from split_converter.single_val_converter import single_val_converter
from split_converter.multiple_val_converter import multiple_val_converter
import tkinter
from tkinter import ttk


class ComboBoxDemo:

	def __init__(self, parent):
		self.parent = parent
		self.display_combo()  # work delegated

	def display_combo(self):
		# A Combobox with values 'First value', 'Second value', 'Third value' is on console
		self.box = ttk.Combobox()
		# Combobox inherits from Sequence--on which indexing is allowed
		self.box['values'] = ('s/500m', 'kmh', 'mph', 'min/mile')
		self.box.grid(column=0, row=0)  # position of display *
		self.box.current(0)  # index of value showing (as default) in the single line window


		def echo_to_console(an_event):
			if self.box.get() == 's/500m' or self.box.get() == 'min/mile':
				print('multiple val input')
			else:
				print(self.box.get())
				print('single val input')


		self.box.bind('<<ComboboxSelected>>', echo_to_console)

if __name__ == '__main__':
	root = tkinter.Tk()
	app = ComboBoxDemo(root)
	root.mainloop()
	app.destroy()

