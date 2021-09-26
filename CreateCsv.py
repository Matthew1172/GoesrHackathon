import os
import csv

cn = "CMI.csv"

ys = ['2020']

hrs = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18','19', '20', '21', '22', '23']

julianDay = 10
jds = []
for i in range(1, julianDay):
    if i < 10:
        jd = '00' + str(i)
    elif i < 100:
        jd = '0' + str(i)
    else:
        jd = str(i)
    jds.append(jd)

# print(jds)

csvrs = []
for y in ys:
    for d in jds:
        for h in hrs:
            pic = y+'-'+d+'-'+h+'.png'
            p = os.path.join(y,d)
            p = os.path.join(p,pic)
            csvrs.append([p,d])

print(csvrs)

with open(cn, 'w') as f:
    writer = csv.writer(f)
    for r in csvrs:
        writer.writerow(r)
