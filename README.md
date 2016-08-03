# disqus-migrate-to-duoshuo
最近发现Disqus访问又不好使了，无奈切换到多说。
好在多说评论系统支持json数据导入。所以写了此脚本将Disqus导出的xml文件进行转换，然后再导入到多说系统中去。

社会化评论系统一般包括两大实体：
- Thread 文章
- Post 评论

所以转换就是将这组内容进转换。 本脚本是建立在多说以url 的path部分作为thread_key的前提下进行的。

```bash

```