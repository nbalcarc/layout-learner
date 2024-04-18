import sqlite3
import html2text
import preprocessor
from functools import reduce

h = html2text.HTML2Text()

con = sqlite3.connect("../data/wikibooks.sqlite")
cur = con.cursor()
cur.execute("SELECT * FROM en")

#line = str(data.fetchone())
#x = h.handle(line)
#validized = preprocessor.validize(x)
#chunked = preprocessor.chunkify(validized, 60)
#print(chunked)
data = cur.fetchall()
#print(data[0])
x = list(map(lambda x: preprocessor.chunkify(preprocessor.validize(reduce(lambda a, y: a + y, x)), 60), data))
data = None
print(len(x))
#print(len(data))

#data = str(cur.execute("SELECT COUNT(*) FROM en").fetchall())
#print(len(data))





