import validators
import datetime

def allowsNone(f):
	def wrapper(element):
		if element is None:
			return True
		return f(element)
	return wrapper

def requires_keys(*keys):
	def decorator(f):
		def wrapper(element):
			if not isinstance(element, dict):
				return False
			for key in keys:
				if key not in element:
					return False
			return f(element)
		return wrapper
	return decorator

@allowsNone
def validDefault(element) -> bool:
	return True

def validRequired(element) -> bool:
	return element is not None and element != ""

@allowsNone
def validUrl(element) -> bool:
	return validators.url(element)

@allowsNone
def validEmail(element) -> bool:
	return validators.email(element)

@allowsNone
@requires_keys('url', 'length', 'type')
def validEnclosure(element) -> bool:
	url = element['url']
	length = element['length']
	return validators.url(url) and validInt(length)

@allowsNone
def validDate(element) -> bool:
	return isinstance(element, datetime.datetime)

@allowsNone
@requires_keys('url', 'text')
def validSource(element) -> bool:
	url = element['url']
	return validators.url(url)

@allowsNone
def validLanguage(element) -> bool:
	return True

@allowsNone
def validCategory(element) -> bool:
	if isinstance(element, dict):
		return "text" in element
	return allowsNone(element)

@allowsNone
def validCategories(element) -> bool:
	return all(validCategory(cat) for cat in element)

@allowsNone
@requires_keys('domain', 'port', 'path', 'registerProcedure', 'protocol')
def validCloud(element) -> bool:
	port = element['port']
	return validInt(port)

@allowsNone
@requires_keys('url', 'title', 'link')
def validImage(element) -> bool:
	url = element['url']
	width,height = element.get('width'),element.get('height')
	wf, hf = True, True
	if width is not None:
		wf = validInt(width) and (int(width) <= 144)
	if height is not None:
		hf = validInt(height) and (int(height) <= 400)
	return validators.url(url) and wf and hf

@allowsNone
@requires_keys('title', 'description', 'name', 'link')
def validInput(element) -> bool:
	return True

@allowsNone
def validInt(element) -> bool:
	return isinstance(element, int) or element.isdigit()

@allowsNone
def validGuid(element) -> bool:
	if isinstance(element, dict):
		return "text" in element
	return True

@allowsNone
def validSkipHours(element) -> bool:
	return True

@allowsNone
def validSkipHours(element) -> bool:
	return True

@allowsNone
def validSkipDays(element) -> bool:
	return True