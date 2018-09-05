import copy
from .validators import *
from .printers import *

class Element(object):
    """Base class for feedrss"""
    def __init__(self, config):
        self.rules = copy.deepcopy(self.__class__.elementRules)
        self.config = config
        for (key, value) in self.rules.items():
            el = self.config.get(key)
            if not value['validator'](el):
                raise Exception('Invalid value for key value ' + key)

    def set(self, name, value):
        if name in self.rules:
            validator = self.rules[name].get('validator', validDefault)
            if not validator(value):
                raise Exception('Invalid value for key value ' + key)
        self.config[name] = value

    def get(self, name):
        return self.config.get(name)

    def xml(self):
        els = []
        for (key, value) in self.config.items():
            rule = self.rules.get(key)
            if rule is not None:
                printer = rule.get('printer')
            printer = printer or defaultPrinter
            if isinstance(value, list):
                for v in value:
                    els.append(printer(key, v))
            else:
                els.append(printer(key, value))
                    
        return "\n".join(els)

class RSSElement(Element):
    elementRules = {} 
    def __init__(self, config):
        self.channel = ChannelElement(config.pop("channel", None))
        self.version = config.pop("version", None)
        if self.version is None:
            self.version = "2.0"
        super(RSSElement, self).__init__(config)

    def xml(self):
        ret = "<rss version=\"{0}\">\n{1}\n</rss>".format(self.version, self.channel.xml())
        return ret

class ChannelElement(Element):
    elementRules = {
        "title": {"validator": validRequired}, "description": {"validator": validRequired},
        "link": {"validator": lambda x: validRequired(x) and validUrl(x)},
        "language": {"validator": validLanguage}, "copyright": {"validator": validDefault}, 
        "managingEditor": {"validator": validEmail}, "webMaster": {"validator": validEmail},
        "pubDate": {"validator": validDate, "printer": datePrinter}, 
        "lastBuildDate": {"validator": validDate, "printer": datePrinter},
        "category": {"validator": validCategories}, "generator": {"validator": validDefault},
        "docs": {"validator": validUrl}, "cloud": {"validator": validCloud},
        "ttl": {"validator": validInt}, "image": {"validator": validImage, "printer": imagePrinter},
        "textInput": {"validator": validInput}, "skipHours": {"validator": validSkipHours},
        "skipDays": {"validator": validSkipDays}
    }

    def __init__(self, config):
        items = config.pop('items', None)
        self.items = []
        if items is not None:
            self.items = [ItemElement(item) for item in items]
        super(ChannelElement, self).__init__(config)

    def xml(self):
        stringItems = "\n".join(x.xml() for x in self.items)
        ret = "<channel>\n{0}\n{1}\n</channel>".format(super(ChannelElement, self).xml(),
            stringItems)
        return ret

class ItemElement(Element):
    elementRules = {
        "title": {"validator": validDefault}, "description": {"validator": validDefault}, "link": {"validator": validUrl},
        "author": {"validator": validEmail}, "category": {"validator": validCategory},
        "comments": {"validator": validUrl},
        "enclosure": {"validator": validEnclosure}, "guid": {"validator": validGuid},
        "pubDate": {"validator": validDate, "printer": datePrinter}, "source": {"validator": validSource}
    }

    def __init__(self, config):
        title = config.get('title')
        desc = config.get('description')
        if not (title is not None or description is not None):
            raise Exception('ItemElement requires either title or description')
        super(ItemElement, self).__init__(config)

    def xml(self):
        ret = "<item>\n{0}\n</item>".format(super(ItemElement, self).xml())
        return ret
