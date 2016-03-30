import datetime
from split_converter.converterError import converterError

#accepts single values (mph or kmh) as a string
#defines functions to convert to 500m split times, mph or kmh
class single_val_converter(object):
	def __init__(self, value):
		try:
			self.value = float(value)
		except ValueError:
			raise converterError('value must be a positive real number!')

		if self.value <= 0:
			raise converterError('value must be greater than 0!')


	#precondition: miles per hour as a positive real number
	#postcondition: returns min/500 m split time as string
	def mph_to_split(self):
		mph = self.value
		m_s = mph  * 0.44704 			#m/s
		total_s = 500.0 / m_s 			#s/500 m
		mn = int(total_s / 60.0) 			#minutes
		s = round(total_s % 60.0, 2) 		#seconds
		output = str(mn) + ':' + str(s) #min:sec.ms
		return output

	#precondition: miles per hour positive real number
	#postcondition: returns km/h as string
	def mph_to_kmh(self):
		mph = self.value
		kmh = str(round(mph * 1.6034, 2))
		return kmh

	#precondition: miles per hour positive real number
	#postcondition: returns min/mile as string
	def mph_to_msplit(self):
		mph = self.value
		total_s = 3600.0 / mph			#total seconds
		mn = int(total_s/60)			#minutes
		s = round(total_s % 60, 2)		#seconds
		output = str(mn) + ':' + str(s)	#min:sec.ms
		return output

	#precondition: km/h as positive real number
	#postcondition: returns miles per hour as string
	def kmh_to_mph(self):
		kmh = self.value
		mph = str(round(kmh/1.6034, 2))
		return mph

	#precondition: km/h as a positive real number
	#postcondition: returns min/500 m split time as string
	def kmh_to_split(self):
		mph = self.kmh_to_mph()
		a = single_val_converter(float(mph))
		return a.mph_to_split()

	def kmh_to_msplit(self):
		mph = self.kmh_to_mph()
		a = single_val_converter(float(mph))
		return a.mph_to_msplit()