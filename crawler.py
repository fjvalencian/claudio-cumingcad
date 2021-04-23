from selenium import webdriver
import math
import os
import shutil
import time
import config
import pprint
import requests


class Crawler:
    def getPages(self, search):
        path = config.SAVE_DIR + search
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.mkdir(path)

        # Disable firefox pdf viewer
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", path)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        fp.set_preference("pdfjs.enabledCache.state", False)
        self.browser = webdriver.Firefox(
            executable_path='geckopath',
            firefox_profile=fp
        )

        # Get number of result pages
        self.browser.get("http://papers.cumincad.org/cgi-bin/works/Search?search=" + search + "&x=0&y=0&first=0")
        results = self.browser.find_element_by_class_name("SEARCHTITLES")
        result = results.text.split()
        hits = int(result[5])

        pages = int(math.ceil(hits / 20))

        returnValue = []
        for i in range(pages):
            firstPage = i * 20
            href = ("http://papers.cumincad.org/cgi-bin/works/Search?search=" + search + "&x=0&y=0&first=" + str(firstPage))
            returnValue.append(href)
        return returnValue

    def getPaper(self, href):
        returnValue = []
        self.browser.get(href)
        # time.sleep(3)
        linksNum = len(self.browser.find_elements_by_xpath('//a[@href]//b'))
        for i in range(linksNum):
            self.browser.get(href)
            # time.sleep(3)
            links = self.browser.find_elements_by_xpath('//a[@href]//b')
            print(links[i].text)
            links[i].click()
            # time.sleep(10)
            # Download paper file
            data = self.browser.find_elements_by_class_name("DATA")      
            # Get paper data
            # Create data dictionary
            data_dict = {
                'authors': "",
                'year': "",
                'title': "",
                'source': "",
                'summary': "",
                'keywords': "",
                'series': "",
                'content': "",
                'url': "",
                'email': "",
            }

            print('*'*20)
            print(data)
            for row in data:
                key = row.text.split(' ', 1)[0]
                value = row.text.split(' ', 1)[1]
                data_dict[key] = value

            try: # Diego spell
                file = self.browser.find_element_by_link_text('file.pdf')
                url = file.get_attribute("href")
                print(url)
                filename = url.rsplit('/', 1)[-1]
                print(filename)
                # file.click()
                # time.sleep(3)
                r = requests.get(url, allow_redirects=True)
                #open('pdfs/'+filename, 'wb').write(r.content)
            except Exception as e:
                print("no pdf")
                print(e)
                print("-"*20)
                filename = ""
                url = ""

            data_dict['content'] = filename
            data_dict['url'] = url
            pprint.pprint(data_dict)
            print("---")
            returnValue.append(data_dict)

        return returnValue
