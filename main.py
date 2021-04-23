from db import Db
from crawler import Crawler

crawler = Crawler()
db = Db()
#db.create()

search = input("Search: ") or "surface"

pages = crawler.getPages(search)
for page in pages:
    pageData = crawler.getPaper(page)
    db.savePage(pageData, search)