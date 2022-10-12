from GoesRGifCreator import *

year = "2022"
product = "ABI-L1b-RadF"
startDay = 1
endDay = 3
mode = 6
for i in range(1, 17):
    if i < 10: b = '0'+str(i)
    else: b = str(i)
    cg = GoesRGifCreator(product=product, year=year, startDay=startDay, endDay=endDay, band=b, mode=mode)
    cg.createGif()