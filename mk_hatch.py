# Writes a minimal DXF: one SOLID hatch (a 400-vertex ring with a square hole) on layer HATCH, plus a frame line.
import math,sys
def loop(pts,flag):
    s=f"92\n{flag}\n72\n0\n73\n1\n93\n{len(pts)}\n"
    for x,y in pts: s+=f"10\n{x:.6f}\n20\n{y:.6f}\n"
    return s+"97\n0\n"
N=400
outer=[(50+40*math.cos(2*math.pi*i/N)*(1+0.1*math.sin(7*2*math.pi*i/N)),50+40*math.sin(2*math.pi*i/N)*(1+0.1*math.sin(7*2*math.pi*i/N))) for i in range(N)]
hole=[(40,40),(60,40),(60,60),(40,60)]
h="0\nHATCH\n8\nHATCH\n62\n5\n10\n0\n20\n0\n30\n0\n210\n0\n220\n0\n230\n1\n2\nSOLID\n70\n1\n71\n0\n91\n2\n"+loop(outer,3)+loop(hole,2)+"75\n0\n76\n1\n98\n0\n"
d="0\nSECTION\n2\nENTITIES\n"+h+"0\nLINE\n8\n0\n10\n0\n20\n0\n11\n100\n21\n100\n0\nENDSEC\n0\nEOF\n"
open(sys.argv[1],"w").write(d)
