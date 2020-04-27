from selenium import webdriver
import json
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path= "C:\\Users\\Rishik\\Downloads\\chromedriver_win32\\chromedriver.exe",
                          options= options)
url = 'https://finance.yahoo.com/quote/AAPL/key-statistics?p=AAPL'


def findXpath(element, target, path):
    if target in element.get_attribute('textContent') and element.tag_name == 'script':
        return path
    newelements = element.find_elements_by_xpath('./*')
    for newelement in newelements:
        final = findXpath(newelement, target, path + '/' + newelement.tag_name)
        if final != '':
            return final
    return ''

def findJson(object, target, path, matchtype):
    if type(object) == matchtype:
        if target in object:
            return path
        for newkey in object:
            final = findJson(object[newkey], target, path+ ','+newkey, matchtype)
            if final != '':
                return final
    return ''

driver.get(url)
#print(driver.page_source)
# elements = driver.find_elements_by_xpath('html/body/script')
# counter = 1
# for element in elements:
#     if 'trailingPE' in element.get_attribute('textContent'):
#         print(counter)
#         break
#     counter += 1
#print(findXpath(element, 'trailingPE', 'html'))
#print(element.get_attribute('textContent'))
#elements = driver.find_elements_by_xpath('html/*')
# for elem in elements:
#     print(elem.tag_name)

element = driver.find_element_by_xpath('html/body/script[1]')
tempData = element.get_attribute("textContent").strip("(this));\n")
tempData = tempData.split("root.App.main = ")[1][:-3]
jsonData = json.loads(tempData)
matchtype = type(jsonData)
# print(findJson(jsonData, 'trailingPE', '', matchtype))

finalData = jsonData['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']
df = pd.DataFrame(finalData)
print(df)
driver.quit()


