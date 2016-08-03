from xml.etree.ElementTree import parse
from urllib.parse import urlparse
from optparse import OptionParser
import json

def main():
    usage = "usage:python3 %prog [options] file"
    parser = OptionParser(usage)
    parser.add_option("-s", "--title-suffix", dest="titleSuffix", help="Thread标题的固定后缀，方便在转换的时候进行删除")
    parser.add_option("-u", "--site-url", dest="siteURL", help="站点网址，以便排除别人拷贝你的站点导致的无用Thread数据")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    file_name = args[0]

    title_suffix = options.titleSuffix
    site_url = options.siteURL
    xmlFile = open(file_name)
    dom = parse(xmlFile)
    thread_elements = dom.getroot().findall('{http://disqus.com}thread')
    #threads
    threads = []
    threads_map = {} #便于关联构建输出时进行索引
    for thread_element in thread_elements:
        thread = {}
        title = thread_element.find('{http://disqus.com}title').text
        link = thread_element.find('{http://disqus.com}link').text
        if site_url is not None and not link.startswith(site_url):
            continue
        if title is not None:
            thread_key = urlparse(link).path
            thread['thread_key'] = thread_key
            if title_suffix is not None:
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

    json_string = json.dumps({'threads':threads,'posts':posts})
    json_file = open("duoshuo-import.json", "w")
    json_file.write(json_string)
    json_file.close()

if __name__ == "__main__":
    main()
