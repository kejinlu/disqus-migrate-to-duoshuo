from xml.etree.ElementTree import parse
import json
from urllib.parse import urlparse

title_suffix = ' | 卢克'
xmlFile = open('./data.xml')
dom = parse(xmlFile)
thread_elements = dom.getroot().findall('{http://disqus.com}thread')
#threads
threads = []
threads_map = {} #便于关联构建输出时进行索引
for thread_element in thread_elements:
    thread = {}
    title = thread_element.find('{http://disqus.com}title').text
    link = thread_element.find('{http://disqus.com}link').text
    if link.startswith('http://geeklu.com') and title:
        thread_key = urlparse(link).path
        thread['thread_key'] = thread_key
        if title.endswith(title_suffix):
            title = title[:-len(title_suffix)]
        thread['title'] = title
        thread['url'] = link
        threads.append(thread)

        thread_id = thread_element.get('{http://disqus.com/disqus-internals}id')
        threads_map[thread_id] = thread

#posts
post_elements = dom.getroot().findall('{http://disqus.com}post')
posts = []
for post_element in post_elements:
    post = {}
    email = post_element.find('{http://disqus.com}author/{http://disqus.com}email').text
    print(email)


#print(threads)
