import datetime


class converter(object):
	def __init__(self, value):
		if type(value) is str:
			raise converterError('value must be a positive real number!')
		if value <= 0:
			raise converterError('value must be greater than 0!')

		self.value = value
	
	#precondition: miles per hour as a positive real number
	#postcondition: returns min/500 split time as string
	def mph_to_split(self):
		mph = self.value
		m_s = mph  * 0.44704 			#m/s
		total_s = 500 / m_s 			#s/500 m
		mn = int(total_s / 60) 			#minutes
		s = round(total_s % 60, 1) 		#seconds
		output = str(mn) + ':' + str(s) #min:sec.ms
		return output

	#precondition: miles per hour positive real number
	#postcondition: returns km/h as string
	def mph_to_kmh(self):
		mph = self.value
		kmh = str(round(mph * 1.6034, 1))
		return kmh

class converterError(Exception):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message


a = converter(11)
print(a.mph_to_kmh())



