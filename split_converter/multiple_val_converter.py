from split_converter.converterError import converterError
from split_converter.single_val_converter import single_val_converter



#accepts two values (mins and sec) as a string
#defines functions to convert to 500m split times, mph or kmh
class multiple_val_converter(object):
	def __init__(self, mins, sec):
		try:
			self.sec = float(sec)
		except ValueError:
			raise converterError('seconds must be a positive integer or float!')

		try:
			self.mins = int(mins)
		except ValueError:
			raise converterError('minutes must be positive integer')

		if self.sec < 0 or self.mins < 0:
			raise converterError('value must be greater than 0!')

	def split_to_mph(self):
		total_s = self.mins * 60 + self.sec
		m_s = 500.0/total_s					#m/s
		mph = round(m_s * 2.237, 2)
		return str(mph)

	def split_to_kmh(self):
		mph = self.split_to_mph()
		a = single_val_converter(float(mph))
		return a.mph_to_kmh()

	def split_to_msplit(self):
		mph = self.split_to_mph()
		a = single_val_converter(float(mph))
		return a.mph_to_msplit()

	def msplit_to_mph(self):
		total_s = self.mins * 60 + self.sec
		m_s = 1609.34/total_s				#m/s
		mph = round(m_s * 2.237, 2)
		return str(mph)

	def msplit_to_kmh(self):
		mph = self.msplit_to_mph()
		a = single_val_converter(float(mph))
		return a.mph_to_kmh()

	def msplit_to_split(self):
		mph = self.msplit_to_mph()
		a = single_val_converter(float(mph))
		return a.mph_to_split()