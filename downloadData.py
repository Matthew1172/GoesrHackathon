import xarray as xr
import boto3
import fsspec
import matplotlib.pyplot as plt
from botocore import UNSIGNED
from botocore.client import Config
import os

def get_urls_for_prefix(prefix):
    s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket='noaa-goes16', Prefix=prefix)
    files_mapper = ["s3://noaa-goes16/" + file['Key'] for page in page_iterator for file in page['Contents']]
    return files_mapper

fp = "FullDiskPngs"
fp = os.path.join(os.getcwd(), fp)
try:
    os.mkdir(fp)
except (FileExistsError, FileNotFoundError):
    print("Couldn't create directory: " + fp)

fp = os.path.join(fp, "CloudMoistureImagery")
try:
    os.mkdir(fp)
except (FileExistsError, FileNotFoundError):
    print("Couldn't create directory: " + fp)

p = 'ABI-L2-CMIPF'
#ys = ['2020', '2021']
ys = ['2020']
hrs = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
ch = 'OR_' + p + '-M6C13'
k = 'CMI'
jds = []

#julianDay = 366
julianDay = 10
for i in range(1, julianDay):
    if i < 10:
        jd = '00' + str(i)
    elif i < 100:
        jd = '0' + str(i)
    else:
        jd = str(i)
    jds.append(jd)

# print(jds)

urls = []
for y in ys:
    yp = os.path.join(fp, y)
    try:
        os.mkdir(yp)
    except (FileExistsError, FileNotFoundError):
        print("Couldnt create year directory: " + y)

    for d in jds:
        path = os.path.join(yp, d)
        try:
            os.mkdir(path)
        except (FileExistsError, FileNotFoundError):
            print("Couldn't create day directory: " + d)

        for h in hrs:
            url = p + '/' + y + '/' + d + '/' + h + '/' + ch
            urls.append(url)

# print(urls)

mburls = []
for u in urls:
    try:
        mburls.append(get_urls_for_prefix(u))
    except (RuntimeError, KeyError):
        print(str(KeyError) + ": " + u)

for mb in mburls:
    fn = mb[0][30:42].replace('/', '-').strip('-') + '.png'
    path = os.path.join(fp, fn[0:4])
    path = os.path.join(path, fn[5:8])
    path = os.path.join(path, fn)
    if os.path.exists(path): continue
    b = mb[2]
    with xr.open_dataset(fsspec.open(b, anon=True).open()) as bds:
        darray = bds[k]
        plt.figure(figsize=(10, 10), dpi=200)
        plt.imshow(darray)
        # plt.plot(darray)
        plt.axis('off')
        # 'ABI-L2-CMIPF/2021/226/00/OR_ABI-L2-CMIPF-M6C13'
        # print(mb[0][30:42].replace('/', '-').strip('-') + '.png')
        try:
            plt.savefig(path, bbox_inches='tight')
        except (RuntimeError, FileNotFoundError, FileExistsError):
            print("RuntimeError or FileNotFoundError or FileExistsError: " + path)
        plt.close()
