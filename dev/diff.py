import sys
from pathlib import Path
from PIL import Image, ImageChops
a, b = Path(sys.argv[1]), Path(sys.argv[2])
bad = 0
for pa in sorted(a.glob("*.png")):
    pb = b / pa.name
    if not pb.exists(): print("MISSING", pa.name); bad += 1; continue
    ia, ib = Image.open(pa).convert("RGB"), Image.open(pb).convert("RGB")
    if ia.size != ib.size: print("SIZE", pa.name, ia.size, ib.size); bad += 1; continue
    d = ImageChops.difference(ia, ib); bbox = d.getbbox()
    if bbox:
        n = sum(1 for px in d.getdata() if px != (0,0,0))
        print("DIFF", pa.name, bbox, n, "px"); bad += 1
        d.point(lambda v: 255 if v else 0).save(b / ("diff-" + pa.name))
    else: print("same", pa.name)
print("TOTAL differing:", bad)
