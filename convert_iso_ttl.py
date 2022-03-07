import re

f = open("iso_combined.ttl", "r", encoding="utf-8")
isottl=f.read()
f.close()

isottl = re.sub(
           r"<(http.+?)[A-z]+\.([A-z]+)>", 
           r"<\1\2>", 
           isottl
       )
#isottl.gsub(,"\1\2")

f=open("iso_changed.ttl","w", encoding='utf-8')
f.write(isottl)
f.close()