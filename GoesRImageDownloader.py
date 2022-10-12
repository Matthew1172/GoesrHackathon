import xarray as xr
import boto3
import fsspec
import matplotlib.pyplot as plt
from botocore import UNSIGNED
from botocore.client import Config
import os

class GoesRImageDownloader():
    def __init__(self, fp, products, sat='G16', yrs=None, modes=None, startDay=1, endDay=366):
        self.fp = fp if fp else None
        self.products = products if products else None
        self.sat = sat
        self.yrs = yrs if yrs else ['2022']
        self.modes = modes if modes else ['6']
        self.startDay = startDay
        self.endDay = endDay

        self.numberOfBandsStart=1
        self.numberOfBandsEnd=17

    def get_urls_for_prefix(self, prefix):
        s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        paginator = s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket='noaa-goes16', Prefix=prefix)
        files_mapper = ["s3://noaa-goes16/" + file['Key'] for page in page_iterator for file in page['Contents']]
        return files_mapper

    def handleSaveImage(self, url, path):
        timeSliceUrls = self.get_urls_for_prefix(url)
        for timeSlice in timeSliceUrls:
            try:
                with xr.open_dataset(fsspec.open(timeSlice, anon=True).open()) as bds:
                    if 'CMI' in bds:
                        darray = bds['CMI']
                    elif 'Rad' in bds:
                        darray = bds['Rad']
                    else:
                        darray = bds['DQF']

                    fn = bds.dataset_name
                    img_path = os.path.join(path, fn)[:-2]
                    img_path += "png"
                    if os.path.exists(img_path): continue

                    plt.figure(figsize=(10, 10), dpi=200)
                    plt.imshow(darray)
                    plt.axis('off')

                    plt.savefig(img_path, bbox_inches='tight')
                    plt.close()

            except(KeyError):
                print("Couldn't save {}! there was a Key Error.".format(img_path))
                continue
            except (RuntimeError, FileNotFoundError, FileExistsError):
                print("RuntimeError or FileNotFoundError or FileExistsError: " + img_path)
                continue
            except:
                print("Couldn't save {}!".format(img_path))
                continue

    def handleSuviUrl(self, product, y, d, h, hp):
        url = "{}/{}/{}/{}".format(product, y, d, h)
        self.handleSaveImage(url, hp)

    def handleNormalUrl(self, product, y, d, h, hp):
        for i in range(self.numberOfBandsStart, self.numberOfBandsEnd):
            if i < 10: band = "0"+str(i)
            else: band = str(i)
            bp = os.path.join(hp, band)
            try:
                os.mkdir(bp)
            except (FileExistsError, FileNotFoundError):
                print("Couldnt create band directory: " + band)
            for mode in self.modes:
                mp = os.path.join(bp, mode)
                try:
                    os.mkdir(mp)
                except (FileExistsError, FileNotFoundError):
                    print("Couldnt create mode directory: " + mode)

                data = "OR_{}-M{}C{}_{}".format(product, mode, band, self.sat)
                url = "{}/{}/{}/{}/{}".format(product, y, d, h, data)
                self.handleSaveImage(url, mp)

    def downloadAndCreateDirectories(self):
        for product, desc in self.products.items():
            pp = os.path.join(self.fp, product)
            try:
                os.mkdir(pp)
            except (FileExistsError, FileNotFoundError):
                print("Couldnt create product directory: " + product)
            for y in self.yrs:
                yp = os.path.join(pp, y)
                try:
                    os.mkdir(yp)
                except (FileExistsError, FileNotFoundError):
                    print("Couldnt create year directory: " + y)
                for d in range(self.startDay, self.endDay):
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
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L1b-RadC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L1b-RadM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ACHAC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ACHAF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ACHAM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ACHTF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ACHTM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ACMC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ACMF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ACMM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ACTPC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ACTPF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ACTPM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ADPC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ADPF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-ADPM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-AODC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-AODF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-CMIPC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-CMIPF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-CMIPM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-CODC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-CODF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-CPSC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-CPSF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-CPSM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-CTPC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-CTPF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-DMWC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-DMWF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-DMWM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-DSIC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-DSIF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-DSIM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-DSRC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-DSRF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-DSRM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-FDCC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-FDCF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-LSTC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-LSTF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-LSTM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-LVMPC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-LVMPF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-LVMPM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-LVTPC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-LVTPF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-LVTPM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-MCMIPC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-MCMIPF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-MCMIPM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-RRQPEF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-RSRC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-RSRF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-SSTF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-TPWC':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-TPWF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-TPWM':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'ABI-L2-VAAF':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'GLM-L2-LCFA':
                                self.handleNormalUrl(product, y, day, hour, hp)
                            case 'SUVI-L1b-Fe093':
                                self.handleSuviUrl(product, y, day, hour, hp)
                            case 'SUVI-L1b-Fe131':
                                self.handleSuviUrl(product, y, day, hour, hp)
                            case 'SUVI-L1b-Fe171':
                                self.handleSuviUrl(product, y, day, hour, hp)
                            case 'SUVI-L1b-Fe195':
                                self.handleSuviUrl(product, y, day, hour, hp)
                            case 'SUVI-L1b-Fe284':
                                self.handleSuviUrl(product, y, day, hour, hp)
                            case 'SUVI-L1b-He303':
                                self.handleSuviUrl(product, y, day, hour, hp)

