from converterError import converterError
from single_val_converter import single_val_converter

class multiple_val_convter(object):
	def __init__(self, mins, sec):

		# if (type(mins), type(sec)) is str:
		# 	raise converterError('value must be a positive integer!')
		# elif (sec or mins) < 0:
		# 	raise converterError('value must be greater than 0!')
		# elif type(mins) is not int:
		# 	raise converterError('value must be integer')

		self.mins = mins
		self.sec = sec

	def split_to_mph(self):
		total_s = self.mins * 60 + self.sec
		m_s = 500.0/total_s					#m/s
		mph = round(m_s * 2.237, 2)
		return str(mph)

	def split_to_kmh(self):
		mph = self.split_to_mph()
		a = single_val_converter(float(mph))
		return a.mph_to_kmh()


a = multiple_val_convter(1, 45)

