from selenium import webdriver
from bs4 import BeautifulSoup as bs
from sys import argv

script, start, end = argv	#start as a argument for Starting Roll No and 'end' as a argument for ending Roll no
start = int(start)
end = int(end)

baseurl = 'http://gseb.org/1510anitnegra/sem2/'		#baseurl. Given url may not be working. Open Frame in new tab and String before /B00/00/B000000.html

f = open('results.txt', 'w')				#Opening Output file.
f.write('SeatNo Name Group Total MM Percentile SciencePercentile Grade Percentage\n') 	#Headers for Outputs.

# end = 979738
# start = 851001

firstChar = 'B'					#Change this to "A" for SSC Results
errorNo = 0
errNoList = []
driver = webdriver.Firefox()			#Open Firefox. Will be required to install Mozilla Firefox

for num in xrange(start, end+1):
    try:
        seatNo = firstChar + str(num)
        resUrl = baseurl + seatNo[0:3] + '/' + seatNo[3:5] + '/' + seatNo + '.html'
        print resUrl
        driver.get(resUrl)
        the_page = driver.page_source
        while "try again" in the_page:
            driver.navigate.refresh
        soup = bs(the_page)
        listB = soup.find_all('b')
        for i in range(0, 5):
            listB[i] = listB[i].next_sibling.string
        seatNo = listB[0]
        name = listB[1]
        name = name.replace(' ','_')
        Group = listB[2]
        if listB[3] == "--":
            SciPercentile = 0.0
            percentile = 0.0
        elif Group == "AB":
            sci = listB[3].split(' ')
            sci1 = float(sci[0].split('-')[1])
            sci2 = float(sci[1].split('-')[1])
            norm = listB[4].split(' ')
            norm1 = float(norm[0].split('-')[1])
            norm2 = float(norm[1].split('-')[1])
            SciPercentile = (sci1+sci2)/2
            percentile = (norm1+norm2)/2
        else:
            SciPercentile = float(listB[3])
            percentile = float(listB[4])
        for i in range(1, 4):
            listB[-i] = listB[-i].string
        MM = int(listB[-3])
        Total = int(listB[-2])
        grade = listB[-1]
        percent = Total*100.0/MM
        string = seatNo+" "+ name+" "+ Group+" "+ str(Total)+" "+ str(MM)+" "+ str(percentile)+" "+ str(SciPercentile)+" "+ grade+" "+str(percent)+"\n"
        print string
        f.write(string)
    except:
        errorNo += 1
        print "Error No: ", errorNo
        errNoList += [num]
print errNoList
f.write(str(errNoList))
f.close() 
driver.close()
