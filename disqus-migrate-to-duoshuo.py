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

    thread_id = post_element.find('{http://disqus.com}thread').get('{http://disqus.com/disqus-internals}id')

    if thread_id in threads_map:
        post = {}
        thread = threads_map[thread_id]
        post['thread_key'] = thread['thread_key']
        post_key = post_element.get('{http://disqus.com/disqus-internals}id')
        post['post_key'] = post_key
        email = post_element.find('{http://disqus.com}author/{http://disqus.com}email').text
        post['author_email'] = email
        author_name = post_element.find('{http://disqus.com}author/{http://disqus.com}name').text
        post['author_name'] = author_name
        ip = post_element.find('{http://disqus.com}ipAddress').text
        post['ip'] = ip

        created_at = post_element.find('{http://disqus.com}createdAt').text
        created_at = created_at.replace('T', ' ')
        created_at = created_at.replace('Z', ' ')
        post['created_at'] = created_at

        message = post_element.find('{http://disqus.com}message').text
        post['message'] = message
        parent_element = post_element.find('{http://disqus.com}parent')
        if parent_element is not None:
            parent_key = parent_element.get('{http://disqus.com/disqus-internals}id')
            post['parent_key'] = parent_key
        posts.append(post)

j = json.dumps({'threads':threads,'posts':posts})
print(j)
