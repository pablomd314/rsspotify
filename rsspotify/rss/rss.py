import element
import email.utils

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

class EnclosureElement(element.Element):
    """docstring for EnclosureElement"""
    def __init__(self, url="https://example.com/audio.mp3", 
        length="1234567890",
        type_="audio/mpeg"):
        attributes = {"url": url, "length": length, "type": type_}
        super(TextInputElement, self).__init__(tag="cloud", 
            attributes=attr)

    def clearAttributes(self):
        raise Exception("URL needs to have url, length, and type")

    def addChild(self, child):
        raise Exception("Can't add child")
        

class TextInputElement(element.Element):
    """docstring for TextInputElement"""
    def __init__(self, title="Example Domain", 
        description="A phrase or sentence describing the channels.",
        name="Name",
        link="http://example.com"):
        title = TextElement(tag="title", text=title)
        desc  = TextElement(tag="description", text=description)
        name  = TextElement(tag="name", text=name)
        link  = TextElement(tag="link", text=link)
        super(TextInputElement, self).__init__(tag="cloud", 
            attributes=attr, children=[title,desc,name,link])

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

    def setName(self, name):
        try:
            self.getChildByTag("name").setText(name)
        except Exception as e:
            raise e

class CloudElement(element.Element):
    """docstring for CloudElement"""
    def __init__(self, domain="radio.xmlstoragesystem.com",
     port="80",
     path="/RPC2",
     registerProcedure="xmlStorageSystem.rssPleaseNotify",
     protocol="xml-rpc"):
        attr = {"domain": domain, 
            "port": port,
            "path": path,
            "registerProcedure": registerProcedure,
            "protocol": protocol} 
        super(CloudElement, self).__init__(tag="cloud", 
            attributes=attr)

    def addChild(self, child):
        raise Exception("Can't add child") 

    def clearAttributes(self, child):
        raise Exception("CloudElement has required attributes.")

    def setDomain(self, domain):
        setAttribute("domain", domain)

    def setPort(self, port):
        setAttribute("port", port)

    def setRegisterProcedure(self, registerProcedure):
        setAttribute("registerProcedure", registerProcedure)

    def setProtocol(self, protocol):
        setAttribute("protocol", protocol)


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

    def setWidth(self, width):
        if int(width) > 144:
            raise Exception("Width too large.")
        self.setOrAddTextElement("width", width)
    
    def setHeight(self, height):
        if int(height) > 400:
            raise Exception("Height too large.")
        self.setOrAddTextElement("height", height)

class ItemElement(element.Element):
    def __init__(self, attributes={}, title=None, description=None):
        if title is None and description is None:
            raise Exception("Either title or description must be defined")
        children = []
        if title is not None:
            title = TextElement(tag="title", text=title)
            children.append(title)
        if description is not None:
            desc  = TextElement(tag="description", text=description)
            children.append(desc)
        super(ItemElement, self).__init__(tag="item", 
            attributes=attributes,
            children=children)

    def clearChildren(self):
        raise Exception("ChannelElement must have a title, link, and description.")

    def setAuthor(self, author):
        # todo: validate author (http://backend.userland.com/stories/storyReader$16)
        self.setOrAddTextElement("author", author)
    
    def setCategory(self, domain, category):
        el = TextElement(tag="category", text=category)
        el.addAttribute("domain", domain)
        self.addChild(el)

    def setComments(self, url):
        self.setOrAddTextElement("comments", url)

    def setEnclosure(self, enclosure):
        assert(isinstance(enclosure, EnclosureElement))
        self.addChild(enclosure)

    def setGuid(self, isPermalink, guid):
        el = TextElement(tag="guid", text=guid)
        el.addAttribute("isPermalink", isPermalink)
        self.addChild(el)

    def setPubDate(self, pubDate):
        self.setOrAddTextElement("comments", email.utils.format_datetime(pubDate))

    def setGuid(self, url, source):
        el = TextElement(tag="source", text=source)
        el.addAttribute("url", url)
        self.addChild(el)


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

    def clearChildren(self):
        raise Exception("ChannelElement must have a title, link, and description.")

    def clearItems(self):
        self.children = filter(self.getChildren(), 
            lambda x: not isinstance(x,ItemElement))

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
    
    def setCategory(self, domain, category):
        el = TextElement(tag="category", text=category)
        el.addAttribute("domain", domain)
        self.addChild(el)

    def setGenerator(self, generator):
        self.setOrAddTextElement("generator", generator)

    def setDocs(self, docs):
        self.setOrAddTextElement("docs", docs)

    def setCloud(self, cloud):
        self.addChild(cloud)

    def setTtl(self, ttl):
        assert(isinstance(float) or isinstance(int))
        self.setOrAddTextElement("ttl", ttl)

    def setImage(self, image):
        self.addChild(image)

    def setTextInput(self, textInput):
        ## this be different ##
        self.setOrAddTextElement("textInput", textInput)

    def setSkipHours(self, ttl):
        ## this be different ##
        self.setOrAddTextElement("ttl", ttl)

    def setSkipDays(self, ttl):
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

    def getChannel(self):
        return self.channel

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
        a = isinstance(self.getChildren()[0], ChannelElement)
        b = (b == "2.0")
        if not (a or b):
            return False
        return super(RSSElement, self).valid()
