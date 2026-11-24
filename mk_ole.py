# Writes a minimal DXF with one OLE2FRAME holding a Paint ("PBrush") picture: a 24-bit BMP in the
# \x01Ole10Native stream of a compound file. Everything here is synthetic (a red rounded-less box).
import struct,sys
W,H=200,60
row=(W*3+3)//4*4
px=bytearray()
for y in range(H):
    r=bytearray()
    for x in range(W):
        edge = x<4 or x>=W-4 or y<4 or y>=H-4
        stripe = (x//20)%2==0
        r+= bytes((0,0,200)) if edge else (bytes((230,230,255)) if stripe else bytes((255,255,255)))
    r+=bytes(row-len(r)); px+=r
bmp=b"BM"+struct.pack("<IHHI",14+40+len(px),0,0,54)+struct.pack("<IiiHHIIiiII",40,W,H,1,24,0,len(px),2835,2835,0,0)+bytes(px)
native=struct.pack("<I",len(bmp))+bmp
END=0xFFFFFFFE;FATS=0xFFFFFFFD;NO=0xFFFFFFFF
nsec=(len(native)+511)//512
def ent(name,typ,left,right,child,start,size,clsid=bytes(16)):
    n=name.encode("utf-16-le")
    return n.ljust(64,b"\0")+struct.pack("<HBBIII",len(n)+2,typ,1,left,right,child)+clsid+bytes(4)+bytes(16)+struct.pack("<IQ",start,size)
import uuid
clsid=uuid.UUID("0003000A-0000-0000-C000-000000000046").bytes_le
d=ent("Root Entry",5,NO,NO,1,END,0,clsid)+ent("\x01Ole10Native",2,NO,NO,NO,2,len(native))+bytes(256)
fat=[FATS,END]+[i+1 for i in range(3,2+nsec)]+[END]
fat+= [NO]*(128-len(fat))
hdr=bytes.fromhex("D0CF11E0A1B11AE1")+bytes(16)+struct.pack("<HHHHH",0x3E,3,0xFFFE,9,6)+bytes(6)+struct.pack("<IIIIIIIII",0,1,1,0,4096,END,0,END,0)+struct.pack("<I",0)+struct.pack("<I",NO)*108
assert len(hdr)==512,len(hdr)
cfb=hdr+struct.pack("<128I",*fat)+d+native.ljust(nsec*512,b"\0")
# envelope: 2-byte marker, then four frame corners (3 little-endian doubles each), as cadcraft reads it
UL=(10.0,50.0);LR=(40.0,30.0)
env=b"\x01\x00"
for x,y in [UL,(LR[0],UL[1]),LR,(UL[0],LR[1])]: env+=struct.pack("<ddd",x,y,0.0)
blob=env+cfb
hexs=blob.hex().upper()
chunks="".join(f"310\n{hexs[i:i+254]}\n" for i in range(0,len(hexs),254))
dxf=("0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1015\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n"
 f"0\nOLE2FRAME\n5\n2B\n100\nAcDbEntity\n8\n0\n100\nAcDbOle2Frame\n70\n2\n3\nOLE Object\n10\n{UL[0]}\n20\n{UL[1]}\n30\n0\n11\n{LR[0]}\n21\n{LR[1]}\n31\n0\n71\n2\n72\n0\n90\n{len(blob)}\n{chunks}1\nOLE\n"
 "0\nLINE\n8\n0\n10\n0\n20\n0\n11\n50\n21\n60\n0\nENDSEC\n0\nEOF\n")
open(sys.argv[1],"w").write(dxf)
open(sys.argv[1]+".bmp","wb").write(bmp)
open(sys.argv[1]+".cfb","wb").write(cfb)
