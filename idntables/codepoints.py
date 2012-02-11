import string
import etree


class InvalidCodepoint(ValueError): pass



class CodePoint(object):
	
	def __init__(self, codepoint=None, variants=[]):
		
		self.codepoint = codepoint
		self.variants = variants
		
	def __str__(self):
		
		if self.codepoint:
			return int_to_cp(self.codepoint)
		return False
		
	def xml_element(self):
		
		element = etree.Element('char', cp=int_to_cp(self.codepoint, prefix=None))
		for (variant_cp, category, condition) in self.variants:
			attribs = {
				'cp': int_to_cp(variant_cp, prefix=None),
			}
			if condition:
				attribs['when'] = condition
			if category:
				attribs['type'] = category
			variant_fragment = etree.Element('var', attrib=attribs)
			element.append(variant_fragment)

		return element



class CodePointRange(object):

	def __init__(self, start=None, end=None):
		
		self.start = start
		self.end = end

	def __str__(self):
		
		if self.start and self.end:
			return "%s-%s" % (int_to_cp(self.start), int_to_cp(self.end))
		return False
		
	def xml_element(self):
		
		element = etree.Element('range', attrib={
			'first-cp': int_to_cp(self.start, prefix=None),
			'last-cp': int_to_cp(self.end, prefix=None),
		})
		return element



def cp_to_int(s, raw=False):
	
	if raw == True:
		codepoints = []
		for cp in s:
			codepoints.append(cp)
	else:
		codepoints = s
	
	output = []

	if isinstance(codepoints, basestring):
		codepoints = codepoints.split(' ')
	
	for cp in codepoints:
		if len(cp) == 1:
			output.append(ord(cp))
		else:
			if cp[0:2] == 'U+' or cp[0:2] == '\u':
				cp = cp[2:]
			try:
				output.append(int(cp, 16))
			except ValueError:
				raise InvalidCodepoint, "Could not parse codepoint \"%s\" from \"%s\"" % (cp, s)
	
	if len(output) == 1:
		return output[0]
	else:
		return output


def int_to_cp(input, prefix="U+"):

	if not prefix:
		prefix = ""
		
	if isinstance(input, (list, tuple)):
		return " ".join("%s%04X" % (prefix, i) for i in input)
	else:
		return "%s%04X" % (prefix, input)


def find_range(input):
	
	if isinstance(input, basestring):
		if (0 < input.find('-') < len(input)):
			(start, end) = string.split(input, '-', 2)
			return (start, end)
		elif (0 < input.find('..') < len(input)):
			(start, end) = string.split(input, '..', 2)
			return (start, end)
	return False


def cp_range(start, end):
		
	start_cp = cp_to_int(start)
	end_cp = cp_to_int(end)

	for cp in range(min(start_cp,end_cp), max(start_cp,end_cp)+1):
		yield cp

