import csv, re, urllib2, argparse
from datetime import datetime


def downloadData(url):
    response = urllib2.urlopen(url)
    return response.read()


def processData(csvData):
    logData = []
    data = csvData.split('\n')

    for i in data[:-1]:
        val = []
        comma=[]
        for ind, ch in enumerate(i):
            if ch==',':
                comma.append(ind)

        if len(comma) == 4:
            logData.append(i.split(','))
        else:
            val.append(i[0:comma[0]])
            val.append(i[comma[0]+1:comma[1]])
            val.append(i[comma[1]+1:comma[3]])
            val.append(i[comma[3]+1:comma[4]])
            logData.append(val)

    return logData


def total_image_hits(data):
    count=0
    for i in data:
        path = i[0].lower()
        if re.findall("[\w]+.png$", path) or re.findall("[\w]+.jpg$", path) or re.findall("[\w]+.gif$", path):
            count += 1
        
    #print(count, len(data))
    print("Image requests account for %.1f%s of all requests"%((count*100)/float(len(data)), "%"))


def find_browser(data):
    browser = ""
    br_count = {"Internet Explorer": 0,
                "Firefox": 0,
                "Chrome": 0,
                "Safari": 0}
    
    for d in data:
        ua = d[2]
        opt = re.findall('[A-Z]+ [\d.]+', ua) + re.findall('[A-Z]+[a-z]+/[\d.]+', ua)
        for i in opt:
            if "MSIE" in i:
                browser = "Internet Explorer"
                br_count[browser] += 1
                break
            
            elif "Firefox" in i:
                browser = "Firefox"
                br_count[browser] += 1
                break
            
            elif "Chrome" in i:
                browser = "Chrome"
                br_count[browser] += 1
                break
            
            elif "Safari" in i:
                browser = "Safari"
                br_count[browser] += 1
                break

    mc = max(br_count.values())
    for key in br_count.keys():
        if br_count[key] == mc:
            break
            return key
    print("Most popular browser is " + key)


def hourly_hits(data):
    hours = [0]*24
    for d in data:
        hours[int(datetime.strptime(d[1], "%Y-%m-%d %H:%M:%S").hour)] += 1
    #print(hours)

    for i in range(24):
        print("Hour {:02d} has {:d} hits".format(i, hours[i]))



parser = argparse.ArgumentParser()
parser.add_argument("--url", help="URL for downloading birthday data")
args = parser.parse_args()
try:
    if args.url:
        csvData = downloadData(args.url)
    else:
        raise NameError("URL not specified.")

    logData = processData(csvData)

    total_image_hits(logData)
    find_browser(logData)
    hourly_hits(logData)

except Exception as e:
    print(e)

'''
data = reading_data()
find_browser(data)
'''
