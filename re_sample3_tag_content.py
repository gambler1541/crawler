import re

file_name = 're_tag_content_example.html'
with open(file_name, 'rt') as f:
    html = f.read()


p = re.compile(r'<[^/]*?>(.*?)</.*?>', re.DOTALL)
result = re.findall(p, html)
for item in result:
    print(item)



