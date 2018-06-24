class Element(object):
    """docstring for Element"""
    def __init__(self, tag="element", attributes={}, children=[]):
        # super(Element, self).__init__()
        self._tag = tag
        self._attributes = attributes
        self._children = children
        
    def getTag(self):
        return self._tag

    def getAttributes(self):
        return self._attributes

    def setAttribute(self, attr_name, attr_value):
        if not isinstance(attr_name, basestring):
            raise Exception("attr_name must be string")
        if not isinstance(attr_value, basestring):
            raise Exception("attr_value must be string")            
        if len(attr_name) == "":
            raise Exception("attr_name cannot be empty string")
        # if len(attr_value) == "":
        #   raise Exception("attr_value cannot be empty string")
        self._attributes[attr_name] = attr_value

    def setAttributes(self, attributes):
        for (attr_name, attr_value) in attributes.items():
            self.setAttribute(attr_name, attr_value)

    def clearAttributes(self):
        self._attributes = {}

    def getChildren(self):
        return self._children

    def getChildrenByTag(self, tag):
        return filter(lambda x: x.getTag() == tag, self.getChildren())

    def getChildByTag(self, tag):
        try:
            return self.getChildrenByTag(tag)[0]
        except Exception as e:
            return None

    def setOrAddTextElement(self, tag, text):
        try:
            self.getChildByTag(tag).setText(language)
        except Exception as e:
            el = TextElement(tag=tag, text=text)
            self.addChild(el)

    def addChild(self, child):
        if not isinstance(child, Element):
            raise Exception("child must be an element")
        self._children.append(child)

    def addChildren(self, children):
        for child in children:
            self.addChild(child)

    def clearChildren(self):
        self._children = []

    def valid(self):
        return all([child.valid for child in self.getChildren()])

    def rss(self):
        return self._rss(0)

    def _rss(self, level):
        pre = "  "*level
        attr_string = ''.join([' {0}="{1}"'.format(attr_name,attr_value) 
            for (attr_name,attr_value) in 
            self.getAttributes().items()])
        children_string = ''.join([child._rss(level+1) + "\n"
            for child in
            self.getChildren()])
        ret = "{3}<{0}{1}>\n{2}{3}</{0}>".format(
            self.getTag(),
            attr_string,
            children_string,
            pre)
        return ret

class TextElement(Element):
    """docstring for TextElement"""
    def __init__(self, tag="text", attributes={}, text="Title"):
        super(TextElement, self).__init__(tag=tag,
            children=[text])

    def setText(self,text):
        self.getChildren()[0] = text        

    # rss element can only have 1 child, a channel
    def addChild(self, child):
        raise Exception("TextElement must have exactly 1 child.")

    def addChildren(self, children):
        if children != []:
            raise Exception("TextElement must have exactly 1 child.")
        return

    def getChildrenByTag(self, tag):
        return []

    def getChildByTag(self, tag):
        return None

    def clearChildren(self):
        raise Exception("TextElement must have exactly 1 child.")

    def valid(self):
        a = len(self.getChildren())
        if a != 1:
            return False
        a = isinstance(self.getChildren()[0], basestring)
        if not a:
            return False
        return super(TextElement, self).valid()

    def _rss(self, level):
        pre = "  "*level
        attr_string = ''.join([' {0}="{1}"'.format(attr_name,attr_value) 
            for (attr_name,attr_value) in 
            self.getAttributes().items()])
        children_string = self.getChildren()[0]
        ret = "{3}<{0}{1}>{2}</{0}>".format(
            self.getTag(),
            attr_string,
            children_string,
            pre)
        return ret