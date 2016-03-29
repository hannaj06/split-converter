from converterError import converterError
from single_val_converter import single_val_converter

class multiple_val_convter(object):
	def __init__(self, mins, sec):

		if type(sec) is str:
			raise converterError('seconds must be a positive integer or float!')
		elif type(mins) is not int:
			raise converterError('value must be integer')
		elif sec < 0 or mins < 0:
			raise converterError('value must be greater than 0!')


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

	def split_to_mpslit(self):
		mph = self.split_to_mph()
		a = single_val_converter(float(mph))
		return a.mph_to_msplit()

	def msplit_to_mph(self):
		total_s = self.mins * 60 + self.sec
		m_s = 1609.34/total_s				#m/s
		print(m_s)
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


a = multiple_val_convter(4, 5)
print(a.split_to_mph())
print(a.split_to_mpslit())
print(a.msplit_to_mph())
print(a.msplit_to_kmh())
print(a.msplit_to_split())