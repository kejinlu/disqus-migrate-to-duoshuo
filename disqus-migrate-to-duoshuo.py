from xml.etree.ElementTree import parse

xmlFile = open('./data.xml')
dom = parse(xmlFile)
dom.getroot().getchildren()


