import crawler_utilities
import codecs
import time

def getContentUrlOfWenku8(indexNum1, indexNum2, \
                            prefix = "http://www.wenku8.com/novel",
                            suffix = "index.htm"):
    urlStr = prefix + "/" + str(indexNum1) + "/" + str(indexNum2) + "/" + suffix
    return urlStr

def getContentTitleOfHtml(htmlStr, keyWord = "<div id=\"title\">"):

    targetIndex = htmlStr.find(keyWord)

    if targetIndex == -1:
        print "Error: getEncodingFromHTML: no keyword <" + keyWord + "> found in html page"
        return None

    startIndex = targetIndex + len(keyWord)
    endIndex = htmlStr.find("<", startIndex)

    return htmlStr[startIndex: endIndex]   

def getTitleFromWenku8(urlStr):

    isSuccess, statusCode,response = crawler_utilities.urlGet(urlStr)

    if not isSuccess:
        return None

    encodingStr = crawler_utilities.getEncodingFromHTML(response)
    htmlContent = response.decode(encodingStr)

    return getContentTitleOfHtml(htmlContent)

# skipMode:
# If consecutive 100 url is 404, then skip the next 500 url and start at a new point
# url format 
# http://www.wenku8.com/ + minorIndex + / + index + "/" + index.htm
# e.g. http://www.wenku8.com/novel/0/1/index.htm
# @startIndex, endIndex: the bound of index
# @minorStartIndex, minorEndIndex: the bound of minorIndex
# @skipMode: whether to enable skip mode: 0 - disabled; 1 - enabled; Skip mode will skip a bunch of url if 
# consecutive of skipThreshold url is 404 and the skip gap is skipInterval
# @sleepInterval: the frequency of sending http request; /secs
# @filename: the output file name
def crawler_main(startIndex, endIndex = 1000000, \
                minorStartIndex = 0, minorEndIndex = 3, \
                skipMode = 0, skipThreshold = 100, skipInterval = 500,\
                sleepInterval = 1, fileName = "title-url.txt"):

    file = codecs.open(fileName, "a", "utf-8")

    invalidUrlCount = 0

    i = startIndex
    while i < endIndex:
        for j in xrange(minorStartIndex, minorEndIndex):
            urlStr = getContentUrlOfWenku8(j, i)

            title = getTitleFromWenku8(urlStr)

            if title != None:
                print title, urlStr
                file.write(title + "\t" + urlStr + "\n")
            else:
                invalidUrlCount += 1

            time.sleep(sleepInterval)



        if (invalidUrlCount * (minorEndIndex - minorStartIndex) ) >= skipThreshold and \
            skipMode == 1:

            msg = "Skip index: [" + str(i+1) + " to " + str(i+skipInterval) + ")\n"
            file.write(msg)
            print msg

            i += skipInterval
            invalidUrlCount = 0
            
        else:
            i+=1

        # reset the count
        if (i - startIndex) % invalidUrlCount == 0 and i != startIndex:
            invalidUrlCount = 0

    file.close()


if __name__ == "__main__":


    # Should start from 20985
    crawler_main(0, endIndex = 2500, \
                minorStartIndex = 0, minorEndIndex = 5)


    # urlStr = "http://www.wenku8.com/novel/0/1/index.htm"

    # print getTitleFromWenku8(urlStr)

    # isSuccess, statusCode,response = crawler_utilities.urlGet(urlStr)

    # if isSuccess:
    #     encodingStr = crawler_utilities.getEncodingFromHTML(response)
    #     htmlContent = response.decode(encodingStr)

    #     print getContentTitleOfHtml(htmlContent)