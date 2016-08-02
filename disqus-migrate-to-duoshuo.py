from xml.etree.ElementTree import parse
import json
from urllib.parse import urlparse

xmlFile = open('./data.xml')
dom = parse(xmlFile)
thread_elements = dom.getroot().findall('{http://disqus.com}thread')
#threads
threads = []
for thread_element in thread_elements:
    thread = {}
    title = thread_element.find('{http://disqus.com}title').text
    link = thread_element.find('{http://disqus.com}link').text
    if link.startswith('http://geeklu.com') and title:
        thread_key = urlparse(link).path
        thread['thread_key'] = thread_key
        if title.endswith(' | 卢克'):
            title = title[:-5]
        thread['title'] = title
        thread['url'] = link
        threads.append(thread)


#posts
print(threads)
