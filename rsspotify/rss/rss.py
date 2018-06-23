import element

class TextElement(element.Element):
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
        a = instanceof(self.getChildren()[0], basestring)
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

class ImageElement(element.Element):
    def __init__(self, attributes={}, url="https://google.com/img.jpeg", title="Example Title",
        link="https://example.com/"):
        url  = TextElement(tag="url", text=url)
        title = TextElement(tag="title", text=title)
        link  = TextElement(tag="description", text=description)
        super(ImageElement, self).__init__(tag="image", 
            attributes=attributes,
            children=[url, title, link])

    def setUrl(self, url):
        try:
            self.getChildByTag("url").setText(url)
        except Exception as e:
            raise e

    def setTitle(self, title):
        try:
            self.getChildByTag("title").setText(title)
        except Exception as e:
            raise e


    def setLink(self, url):
        try:
            self.getChildByTag("link").setText(url)
        except Exception as e:
            raise e

    def setDescription(self, desc):
        self.setOrAddTextElement("description", desc)

    def setWidth(self, desc):
        # validate
        self.setOrAddTextElement("description", desc)
    
    def setHeight(self, desc):
        # validate
        self.setOrAddTextElement("description", desc)


class ChannelElement(element.Element):
    """docstring"""
    def __init__(self, attributes={}, title="Example Domain", link="http://example.com",
        description="A phrase or sentence describing the channels."):
        title = TextElement(tag="title", text=title)
        link  = TextElement(tag="link", text=link)
        desc  = TextElement(tag="description", text=description)
        super(ChannelElement, self).__init__(tag="channel", 
            attributes=attributes,
            children=[title, link, desc])

    def setTitle(self, title):
        try:
            self.getChildByTag("title").setText(title)
        except Exception as e:
            raise e

    def setLink(self, url):
        try:
            self.getChildByTag("link").setText(url)
        except Exception as e:
            raise e

    def setDescription(self, desc):
        try:
            self.getChildByTag("description").setText(desc)
        except Exception as e:
            raise e

    def setLanguage(self, language):
        # todo: validate language (http://backend.userland.com/stories/storyReader$16)
        self.setOrAddTextElement("language", language)

    def setCopyright(self, copyright):
        self.setOrAddTextElement("copyright", copyright)

    def setManagingEditor(self, managingEditor):
        self.setOrAddTextElement("managingEditor", managingEditor)

    def setLastBuildDate(self, lastBuildDate):
        self.setOrAddTextElement("lastBuildDate", lastBuildDate)
    
    def setCategory(self, category):
        ## this be different ##
        self.setOrAddTextElement("category", category)

    def setGenerator(self, generator):
        self.setOrAddTextElement("generator", generator)

    def setDocs(self, docs):
        self.setOrAddTextElement("docs", docs)

    def setCloud(self, cloud):
        ### this be different ###
        self.setOrAddTextElement("cloud", cloud)

    def setTtl(self, ttl):
        # validate int #
        self.setOrAddTextElement("ttl", ttl)

    def setImage(self, image):
        ## this be different ##
        self.setOrAddTextElement("image", image)

    def setTextInput(self, textInput):
        ## this be different ##
        self.setOrAddTextElement("textInput", textInput)

    def setSkipHours(self, ttl):
        ## this be different ##
        self.setOrAddTextElement("ttl", ttl)

    def setSkupDays(self, ttl):
        ## this be different ##
        self.setOrAddTextElement("ttl", ttl)



class RSSElement(element.Element):
    """docstring for RSSElement"""
    def __init__(self):
        channel = ChannelElement()
        super(RSSElement, self).__init__(tag="rss",
         attributes={"version": "2.0"},
         children = [channel])

    def clearAttributes(self):
        raise Exception("RSSElement needs to have version attribute.")

    # rss element can only have 1 child, a channel
    def addChild(self, child):
        raise Exception("RSSElement must have exactly 1 child.")

    def addChildren(self, children):
        if children != []:
            raise Exception("RSSElement must have exactly 1 child.")
        return

    def clearChildren(self):
        raise Exception("RSSElement must have exactly 1 child.")

    def valid(self):
        a = len(self.getChildren())
        b = self.getAttributes().get("version")
        if a != 1 or b is None:
            return False
        a = instanceof(self.getChildren()[0], ChannelElement)
        b = (b == "2.0")
        if not (a or b):
            return False
        return super(RSSElement, self).valid()
