import sys,os
import xml.sax

reload(sys)
sys.setdefaultencoding('utf-8')

class ConvertXML(xml.sax.ContentHandler):
    'Convert the XML file'
    def __init__(self, showlog):
        self.currentData = ""
        self.attr_name = ""
        self.SHOW_LOG = showlog

        self.Component = ""
        self.DE_manager = ""
        self.Found = ""
        self.Headline = ""
        self.Identifier = ""
        self.Original_found = ""
        self.Product = ""
        self.Project = ""
        self.Severity_desc = ""
        self.Status = ""
        self.Status_desc = ""
        self.Submitted_on = ""
        self.Tickets_count = ""

    def startElement(self, tag, attributes):
        self.currentData = tag
        if tag == "Defect":
            self.Identifier = attributes["id"]
            #print self.Identifier
        if tag == "Field":
            self.attr_name = attributes["name"]
            #print self.attr_name
    def endElement(self, tag):
        if self.currentData == "Field":
            print 'ConvertXML::endElement'
        self.currentData = ""
    def characters(self, content):
        if self.currentData == "Field":
            if self.attr_name == "Component":
                self.Component = content
                print self.Component
            elif self.attr_name == "DE-manager":
                self.DE_manager = content
                print self.DE_manager
            elif self.attr_name == "Found":
                self.Found = content
                print self.Found
            elif self.attr_name == "Headline":
                self.Headline = content
                print self.Headline
            elif self.attr_name == "Original_found":
                self.Original_found = content
                print self.Original_found
            elif self.attr_name == "Product":
                self.Product = content
                print self.Product
            elif self.attr_name == "Project":
                self.Project = content
                print self.Project
            elif self.attr_name == "Severity_desc":
                self.Severity_desc = content
                print self.Severity_desc
            elif self.attr_name == "Status":
                self.Status = content
                print self.Status
            elif self.attr_name == "Status_desc":
                self.Status_desc = content
                print self.Status_desc
            elif self.attr_name == "Submitted_on":
                self.Submitted_on = content
                print self.Submitted_on
            elif self.attr_name == "Tickets_count":
                self.Tickets_count = content
                print self.Tickets_count
            elif self.attr_name == "":
                if self.SHOW_LOG:
                    print '>>>>ConvertXML::characters:NON-support tag name'
if __name__ == '__main__':
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    handler = ConvertXML(0)#1: show log
    parser.setContentHandler(handler)

    parser.parse('./xmlFile/WSAPI_buffer.xml')

