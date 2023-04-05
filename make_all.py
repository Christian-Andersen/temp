import csv
import datetime
import shutil
import urllib.request
from pathlib import Path


size1 = Path('IDCKWCDEA0.tgz').stat().st_size
size2 = int(urllib.request.urlopen('ftp://ftp.bom.gov.au/anon/gen/clim_data/IDCKWCDEA0.tgz').info()['Content-length'])
if size1 != size2:
    print('Downloading New File')
    urllib.request.urlretrieve('ftp://ftp.bom.gov.au/anon/gen/clim_data/IDCKWCDEA0.tgz', 'IDCKWCDEA0.tgz')
    print('Unpacking File')
    shutil.unpack_archive('IDCKWCDEA0.tgz')
    print('File Unpacked')

rows = []

print('Start Reading Files')
total_files = sum(1 for _ in Path("tables").rglob("*"))
for idx, p in enumerate(Path("tables").rglob("*")):
    if idx%100 == 0:
        print(f'{idx/total_files:.2%}', end='\r')
    if p.suffix != '.csv':
        continue
    with open(p, 'r', encoding='unicode_escape') as f:
        r = csv.reader(f)
        for row in r:
            if not row:
                continue
            try:
                date = datetime.datetime.strptime(row[1], "%d/%m/%Y").date()
            except ValueError:
                continue
            new_row = [date, row[0], row[5], row[6], row[7], row[8]]
            rows.append(['' if x==' ' else x for x in new_row])

print('Creating CSV')
with open('temp_all.csv', 'w', encoding='utf-8', newline='') as out_file:
    w = csv.writer(out_file)
    w.writerow(['date', 'location', 'max_temp', 'min_temp', 'max_humidity', 'min_humidity'])
    w.writerows(rows)
print('Done')
