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

def handleSaveImage(url, path):
    timeSliceUrls = get_urls_for_prefix(url)
    for timeSlice in timeSliceUrls:
        with xr.open_dataset(fsspec.open(timeSlice, anon=True).open()) as bds:
            try:
                if 'CMI' in bds:
                    darray = bds['CMI']
                elif 'Rad' in bds:
                    darray = bds['Rad']
                else:
                    darray = bds['DQF']
            except(KeyError):
                continue

            fn = bds.dataset_name
            img_path = os.path.join(path, fn)[:-2]
            img_path += "png"
            if os.path.exists(img_path): continue

            plt.figure(figsize=(10, 10), dpi=200)
            plt.imshow(darray)
            plt.axis('off')

            try:
                plt.savefig(img_path, bbox_inches='tight')
            except (RuntimeError, FileNotFoundError, FileExistsError):
                print("RuntimeError or FileNotFoundError or FileExistsError: " + img_path)
            plt.close()

def handleSuviUrl(sat, product, y, d, h, hp):
    url = "{}/{}/{}/{}".format(product, y, d, h)
    handleSaveImage(url, hp)

def handleNormalUrl(sat, product, y, d, h, hp, numberOfBandsStart=1, numberOfBandsEnd=17, modes=None):
    if modes is None: modes = ['6']
    for i in range(numberOfBandsStart, numberOfBandsEnd):
        if i < 10: band = "0"+str(i)
        else: band = str(i)
        bp = os.path.join(hp, band)
        try:
            os.mkdir(bp)
        except (FileExistsError, FileNotFoundError):
            print("Couldnt create band directory: " + band)
        for mode in modes:
            mp = os.path.join(bp, mode)
            try:
                os.mkdir(mp)
            except (FileExistsError, FileNotFoundError):
                print("Couldnt create mode directory: " + mode)

            data = "OR_{}-M{}C{}_{}".format(product, mode, band, sat)
            url = "{}/{}/{}/{}/{}".format(product, y, d, h, data)
            handleSaveImage(url, mp)

def downloadAndCreateDirectories(fp, products, sat='G16', yrs=None, dayStart=1, dayEnd=2):
    if yrs is None: yrs = ['2020']
    for product, desc in products.items():
        pp = os.path.join(fp, product)
        try:
            os.mkdir(pp)
        except (FileExistsError, FileNotFoundError):
            print("Couldnt create product directory: " + product)
        for y in yrs:
            yp = os.path.join(pp, y)
            try:
                os.mkdir(yp)
            except (FileExistsError, FileNotFoundError):
                print("Couldnt create year directory: " + y)
            for d in range(dayStart, dayEnd):
                if d < 10: day = '00' + str(d)
                elif d < 100: day = '0' + str(d)
                else: day = str(d)
                dp = os.path.join(yp, day)
                try:
                    os.mkdir(dp)
                except (FileExistsError, FileNotFoundError):
                    print("Couldn't create day directory: " + day)
                for h in range(24):
                    if h < 10: hour = str(0)+str(h)
                    else: hour = str(h)
                    hp = os.path.join(dp, hour)
                    try:
                        os.mkdir(hp)
                    except (FileExistsError, FileNotFoundError):
                        print("Couldnt create hour directory: " + hour)

                    match product:
                        case 'ABI-L1b-RadF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L1b-RadC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L1b-RadM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ACHAC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ACHAF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ACHAM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ACHTF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ACHTM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ACMC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ACMF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ACMM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ACTPC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ACTPF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ACTPM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ADPC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ADPF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-ADPM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-AODC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-AODF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-CMIPC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-CMIPF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-CMIPM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-CODC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-CODF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-CPSC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-CPSF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-CPSM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-CTPC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-CTPF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-DMWC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-DMWF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-DMWM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-DSIC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-DSIF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-DSIM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-DSRC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-DSRF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-DSRM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-FDCC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-FDCF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-LSTC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-LSTF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-LSTM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-LVMPC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-LVMPF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-LVMPM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-LVTPC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-LVTPF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-LVTPM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-MCMIPC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-MCMIPF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-MCMIPM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-RRQPEF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-RSRC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-RSRF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-SSTF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-TPWC':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-TPWF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-TPWM':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'ABI-L2-VAAF':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'GLM-L2-LCFA':
                            handleNormalUrl(sat, product, y, day, hour, hp)
                        case 'SUVI-L1b-Fe093':
                            handleSuviUrl(sat, product, y, d, h, hp)
                        case 'SUVI-L1b-Fe131':
                            handleSuviUrl(sat, product, y, d, h, hp)
                        case 'SUVI-L1b-Fe171':
                            handleSuviUrl(sat, product, y, d, h, hp)
                        case 'SUVI-L1b-Fe195':
                            handleSuviUrl(sat, product, y, d, h, hp)
                        case 'SUVI-L1b-Fe284':
                            handleSuviUrl(sat, product, y, d, h, hp)
                        case 'SUVI-L1b-He303':
                            handleSuviUrl(sat, product, y, d, h, hp)

