from ProductScanner import *

def getProducts(productsPath):
    with open(productsPath, 'r') as f:
        ps = f.readlines()
    return {k[0]: k[1][:-1] for k in [i.split(' - ') for i in ps]}

fp = "GoesRImages"
fp = os.path.join(os.getcwd(), fp)
try:
    os.mkdir(fp)
except (FileExistsError, FileNotFoundError):
    print("Couldn't create GoesRImages directory: " + fp)

#aws s3 cp s3://noaa-goes16/<Product>/<Year>/<Day of Year>/<Hour>/<Filename> . --no-sign-request
products = getProducts(os.path.join(os.getcwd(), "products.txt"))
#GoesRImages//<Product>//<Year>//<Day of Year>//<Hour>//<Band>//<Mode>//<Filename>
#or if no band and channel (SUVI)
#GoesRImages//<Product>//<Year>//<Day of Year>//<Hour>//<Filename>
downloadAndCreateDirectories(fp, products)