import os


ignore = ["git","idea","LICENSE","README.md"]
result = []
files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser("./")) for f in fn]
temp = []
for elem in files:
    if elem.find(ignore[0]) == -1 and elem.find(ignore[1]) == -1 and elem.find(ignore[2]) == -1 and elem.find(ignore[3]) == -1:
            result.append(elem)

for elem in result:
    print("ampy -p /dev/ttyUSB0 put %s %s" % (elem,elem[1:]))

