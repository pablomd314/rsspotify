def defaultPrinter(tag, value):
	if isinstance(value, str):
		return "<{0}>{1}</{0}>".format(tag, value)
	elif isinstance(value, dict):
		attrs = ["{0}=\"{1}\"".format(k,v) for (k,v) in value.items() if k != "text"]
		if "text" in value:
			return "<{0} {2}>{1}</{0}>".format(tag, value['text'], " ".join(attrs))
		else:
			return "<{0} {1}/>".format(tag, " ".join(attrs))

def imagePrinter(tag, value):
	children = "\n".join("<{0}>{1}</{0}>".format(k,v) for (k,v) in value.items())
	ret = "<image>\n{0}\n</image>".format(children)
	return ret

def datePrinter(tag, value):
	return "<pubDate>{0}</pubDate>".format(
		value.strftime("%a, %d %b %Y %H:%M:%S GMT"))
	
# do this faggot