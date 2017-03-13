import urllib2
import urlparse
import codecs

def testGetURL(urlStr):
    response = urllib2.urlopen(urlStr)
    print response.getcode()
    return response.read()

def testURLParse(urlStr):
    result = urlparse.urlparse(urlStr)
    print result

# Send GET to urlStr
# Return (Boolean: isSuccess, int: StatusCode, String: response)
def urlGet(urlStr):
    try:
        response = urllib2.urlopen(urlStr)

    except urllib2.HTTPError as error:
        print "Error: " + urlGet.__name__ + \
                " raise an Exception: HTTPError"+ \
                " for url <" + urlStr + ">, " + \
                " code: " + str(error.code) + \
                " reason: ", error.reason
        return False, error.code, None

    except urllib2.URLError as error:
        print "Error: " + urlGet.__name__ + \
                " raise an Exception: URLError"+ \
                " for url <" + urlStr + ">, " + \
                "reason: ", error.reason
        return False, -1, None

    else:
        return True, response.getcode(), response.read()

# Get the encoding str from the html
# return the encoding string if succeed
# return None on error cases
def getEncodingFromHTML(htmlPageStr, keyWord = "charset"):
    
    targetIndex = htmlPageStr.find(keyWord)

    if targetIndex == -1:
        print "Error: getEncodingFromHTML: no keyword <" + keyWord + "> found in html page"
        return None

    targetIndex += len(keyWord)

    startIndex = htmlPageStr.find("=", targetIndex)
    endIndex = htmlPageStr.find("\"", targetIndex)

    if startIndex == -1 or endIndex == -1:
        print "Error: getEncodingFromHTML: html parse error after keyword"

        return None

    return htmlPageStr[startIndex+1:endIndex].strip()




if __name__ == "__main__":

    #urlStr = "https://www.google.com"
    urlStr = "http://www.wenku8.com/book/381.htm"

    #testGetURL(urlStr)

    isSuccess, statusCode,response = urlGet(urlStr)

    encodingStr = getEncodingFromHTML(response)

    if encodingStr != None and isSuccess:
        print "<" + encodingStr + ">"
        
        file = codecs.open("output.txt", "w", "utf-8")
        file.write(response.decode(encodingStr))
        file.close()

        #print response.decode("encodingStr")

    # print isSuccess
    # print statusCode
    # print response

    
    