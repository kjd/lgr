import datetime
import re
import string
import StringIO

from idntables.codepoints import *
from idntables.idna import IDN
import idntables.etree as etree


xml_header = "<?xml version=\"1.0\"?>\n"
xml_namespace = "http://www.iana.org/idn-tables/0.1"

class InvalidDomain(Exception): pass
class InvalidIDNTable(Exception): pass


class IDNTable(object):

	
	def __init__(self, filename=None):
		
		self._codepoints = set()
		self._variants = {}
		self.meta = IDNTableMetadata()

		if filename:
			self.load(filename)


	def __contains__(self, item):

		return self.contains(item)


	def __add__(self, other):

		self.merge(other)


	def __and__(self, other):

		# diff = self.diff(other)
		# return diff.unchanged
		raise NotImplementedError


	def __sub__(self, other):
		
		# diff = self.diff(other)
		# return diff.deleted
		raise NotImplementedError


	def __or__(self, other):
		
		self.merge(other)


	def __len__(self):
		
		return len(self._codepoints)


	def __str__(self):
		
		return self.xml()


	def __iter__(self):
		
		for cp in self._codepoints:
			yield int_to_cp(cp)


	def add(self, *arguments):
		
		for argument in arguments:
		
			r = find_range(argument)
			if r:
				self.addrange(r[0], r[1])
			else:
				codepoint = cp_to_int(argument)
				if not codepoint in self._codepoints:
					self._codepoints.add(codepoint)


	def delete(self, *arguments):

		for argument in arguments:
		
			r = find_range(argument)
			if r:
				self.deleterange(r[0], r[1])
			else:
				codepoint = cp_to_int(argument)
				if codepoint in self._codepoints:
					self._codepoints.discard(codepoint)
				if codepoint in self._variants:
					del self._variants[codepoint]


	def addrange(self, start, end):
		
		for cp in cp_range(start, end):
			if not cp in self._codepoints:
				self._codepoints.add(cp)


	def deleterange(self, start, end):

		for cp in cp_range(start, end):
			if cp in self._codepoints:
				self._codepoints.discard(cp)


	def addvariant(self, codepoint, variant, category=None, condition=None):
		
		cp = cp_to_int(codepoint)
		if variant.find(' ') > 0:
			variant_cp = []
			for vcp in variant.split(' '):
				variant_cp.append(cp_to_int(vcp))
		else:
			variant_cp = cp_to_int(variant)
							
		if not cp in self._codepoints:
			self._codepoints.add(cp)
		if not cp in self._variants:
			self._variants[cp] = []
			
		self._variants[cp].append([variant_cp, category, condition])


	def entries(self):
		
		# Iterate through an ordered list of the codepoints, to identify
		# sets of adjacent codepoints that can be merged into a single
		# range. If a codepoint has a variant, it is removed from a range.
		
		codepoint_list = sorted(self._codepoints)
		last_write = 1
		
		for i in range(0, len(codepoint_list)):
			
			has_variant = codepoint_list[i] in self._variants
			
			if i+1 < len(codepoint_list):
				if codepoint_list[i] == codepoint_list[i+1]-1:
					if not has_variant:
						continue
						
			codepoint_range = codepoint_list[last_write+1:i+1]
			codepoint_single = None
			if has_variant:
				codepoint_single = codepoint_range[-1]
				codepoint_range = codepoint_range[0:-1]
				
			if len(codepoint_range) == 1:
				yield CodePoint(codepoint_range[0])
				
			elif len(codepoint_range) > 1:
				yield CodePointRange(codepoint_range[0], codepoint_range[-1])
				
			if codepoint_single:
				yield CodePoint(codepoint_single, variants=self._variants.get(codepoint_single))

			last_write = i


	def contains(self, item, exceptions=False):

		if len(item) == 1:
			return cp_to_int(item) in self._codepoints
		else:
			idn = IDN(item)
			position = 0
			for codepoint in idn.codepoints:
				position += 1
				if not codepoint in self._codepoints:
					if exceptions:
						raise InvalidDomain, "Codepoint U+%04X at position %d not allowed per table" % (codepoint, position)
					return False
			return True


	def variants(self, item, exceptions=False):

		idn = IDN(item)
		for codepoints in self._yield_variants(idn.codepoints, exceptions):
			result = IDN(codepoints)
			yield result


	def _yield_variants(self, codepoints, exceptions):
		
		codepoint = codepoints[0]
		variants = [codepoint]
		
		if not codepoint in self._codepoints:
			raise InvalidDomain, "Domain not allowed per table"
			
		if self._variants.has_key(codepoint):
			for (variant, category, condition) in self._variants[codepoint]:
				if isinstance(variant, int):
					variants.append(variant)
				else:
					variants.extend(variant)
		
		for variant in variants:
		
			if len(codepoints) > 1:
				for remainder in self._yield_variants(codepoints[1:], exceptions):
					yield [variant] + remainder
			else:
				yield [variant]


	def merge(self, table):
		
		raise NotImplementedError


	def diff(self, table):
		
		diff_table = IDNTableDiff(self, table)
		return diff_table


	def xml(self, xmlns=xml_namespace):

		if xmlns:
			xml = etree.Element('idntable', xmlns=xmlns)
		else:
			xml = etree.Element('idntable')
		meta = etree.Element('meta')
		data = etree.Element('data')
		
		for entry in self.entries():
			data.append(entry.xml_element())

		if self.meta.script:
			if isinstance(self.meta.script, basestring):
				self.meta.script = [self.meta.script]
			for script in self.meta.script:
				meta.append(_text_element('script', script))
	
		if self.meta.language:
			if isinstance(self.meta.language, basestring):
				self.meta.language = [self.meta.language]
			for language in self.meta.language:
				meta.append(_text_element('language', language))	

		if self.meta.domain:
			if isinstance(self.meta.domain, basestring):
				self.meta.domain = [self.meta.domain]
			for domain in self.meta.domain:
				meta.append(_text_element('domain', domain))	

		if self.meta.date:
			meta.append(_text_element('date', self.meta.get_date(iso_date=True)))	

		if self.meta.version:
			meta.append(_text_element('version', self.meta.version))

		if self.meta.description:
			attribs = {}
			if self.meta.description_type:
				attribs['type'] = self.meta.description_type
			description = etree.Element('description', attrib=attribs)
			description.text = self.meta.description
			meta.append(description)
			
		if len(meta) > 0:
			xml.append(meta)
		xml.append(data)
		_xml_indent(xml)
		
		return xml_header + etree.tostring(xml)


	def parse(self, data, xmlns=xml_namespace):

		xmlobj = etree.XML(data)
		
		for c in self._findall(xmlobj, 'data/char', xmlns):
			self.add(c.get('cp'))
			for v in self._findall(c, 'var', xmlns):
				self.addvariant(c.get('cp'), v.get('cp'), condition=v.get('when'), category=v.get('type'))
		for r in self._findall(xmlobj, 'data/range', xmlns):
			self.addrange(r.get('first-cp'), r.get('last-cp'))
			
		for e in self._findall(xmlobj, 'meta/data', xmlns):
			self.meta.date = e.text
		for e in self._findall(xmlobj, 'meta/version', xmlns):
			self.meta.version = e.text
		for e in self._findall(xmlobj, 'meta/domain', xmlns):
			self.meta.domain.append(e.text)
		for e in self._findall(xmlobj, 'meta/language', xmlns):
			self.meta.language.append(e.text)
		for e in self._findall(xmlobj, 'meta/script', xmlns):
			self.meta.script.append(e.text)
		for e in self._findall(xmlobj, 'meta/description', xmlns):
			self.meta.description_type = e.get('type')
			self.meta.description = e.text


	def _findall(self, obj, path, xmlns):
		
		elements = path.split('/')
		path = "/".join(["{%s}%s" % (xmlns, e) for e in elements])
		return obj.findall(path)


	def save(self, filename):
		
		xml = self.xml()
		
		f = open(filename, 'wb')
		f.write(xml)
		f.close()


	def load(self, filename):
		
		try:
			f = open(filename, 'rb')
			data = f.read()
			f.close()
		except IOError, e:
			raise InvalidIDNTable(e)
		
		try:
			self.parse(data)	
		except Exception, e:
			raise InvalidIDNTable(e)



class IDNTableMetadata(object):
	
	def __init__(self):
		
		self.version = None
		self._date = None
		self.script = []
		self.language = []
		self.domain = []
		self.description = None
		self.description_type = None


	def _convert_iso8601_to_date(self, value):
		
		r = re.match("^(\d\d\d\d)\-(\d\d)\-(\d\d)$", value)
		if r:
			year = int(r.group(1))
			month = int(r.group(2))
			day = int(r.group(3))
			return datetime.date(year, month, day)
		else:
			raise ValueError, "Not a valid date of the form YYYY-MM-DD"


	def set_date(self, value):
	
		if isinstance(value, datetime.date):
			self._date = value
		elif isinstance(value, basestring):
			self._date = self._convert_iso8601_to_date(value)
		elif value is None:
			self._date = None
		else:
			raise ValueError, "Date must be either ISO 8601 string or datetime object"


	def get_date(self, iso_date=False):

		if not self._date:
			return None
			
		if iso_date:
			return "%04d-%02d-%02d" % (self._date.year, self._date.month, self._date.day)
		else:
			return self._date


	def del_date(self):

		self._date = None


	date = property(get_date, set_date, del_date)


	def add_language(self, language):
		
		self.language.append(language)


	def delete_language(self, language):
		
		self.language.remove(language)


	def stubname(self):
		
		identifier = "unknown"
		if self.script:
			identifier = string.join(self.script, '+')
		elif self.language:
			identifier = string.join(self.language, '+')
		
		return "%s_%s_%s" % (self.domain or "unknown", identifier, self.version or '0')	



class IDNTableDiff(object):
	
	def __init__(self, first_table=None, second_table=None):
		
		self.first_table = first_table
		self.second_table = second_table
		
		self.changed = []
		self.unchanged = []
		self.added = []
		self.deleted = []
		
		if first_table and second_table:
			self.compare()


	def compare(self):
		
		raise NotImplementedError



def load(filename):

	return IDNTable(filename=filename)


def _xml_indent(elem, level=0):

	i = "\n" + level*"  "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		for e in elem:
			_xml_indent(e, level+1)
			if not e.tail or not e.tail.strip():
				e.tail = i + "  "
		if not e.tail or not e.tail.strip():
			e.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i


def _text_element(name, value, attribs=None):

	element = etree.Element(name)
	element.text = value
	return element

