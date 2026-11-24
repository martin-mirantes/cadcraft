# DXF with four text styles named after common Windows fonts (arial.ttf, verdana.ttf, georgia.ttf, GOTHIC.TTF).
import sys
st=[("S_ARIAL","arial.ttf"),("S_VERDANA","verdana.ttf"),("S_GEORGIA","georgia.ttf"),("S_CENTURY","GOTHIC.TTF")]
t="0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1015\n0\nENDSEC\n0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nSTYLE\n70\n%d\n"%len(st)
for n,f in st: t+=f"0\nSTYLE\n2\n{n}\n70\n0\n40\n0\n41\n1\n50\n0\n71\n0\n42\n2.5\n3\n{f}\n4\n\n"
t+="0\nENDTAB\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n"
for i,(n,f) in enumerate(st): t+=f"0\nTEXT\n8\n0\n10\n0\n20\n{i*10}\n30\n0\n40\n4\n1\nIluminacao {f} 0123456789\n7\n{n}\n"
t+="0\nENDSEC\n0\nEOF\n"
open(sys.argv[1],"w").write(t)
