#! /usr/bin/env python3
# -*- Coding: UTF-8 -*-

r"""
Convert Amber/GAFF/GAFF2 Force Field from Amber format to Gaussian format.
"Amber=SoftOnly should appear in your Gaussian input file."
The atom type as well as the charge should be in the coordinates section like
"C-ca--0.0628604164    x-coordinate    y-coordinate    z-coordinate"
"""

# prepare files name
import sys
fl_name = sys.argv[1] if len(sys.argv) > 1 else "gaff"
ifl_name = fl_name + ".dat"
ofl_name = fl_name + ".prm"

# open files
ifl = open(ifl_name, "r")
print("Will read from \"{ifl_name:s}\".".format(ifl_name = ifl_name))
ofl = open(ofl_name, "w")
print("Will write to \"{ofl_name:s}\".".format(ofl_name = ofl_name))

# make an alias to a easier way of printing
def printo(*pargs, **kwargs):
    global ofl
    print(*pargs, **kwargs, file = ofl)
    return

# title section
buf = ifl.readline()
printo("! Generated by FF_Amber2Gaussian.py")

# non-bonded interaction section
printo("!")
printo("! Non-bonded interaction")
printo("!")
printo("NonBon {VType:1d} {CType:1d} {VCutoff:d} {CCutoff:d}".format(\
    VType = 3, CType = 1, VCutoff = -10, CCutoff = 0), \
    "{VScale1:.3f} {VScale2:.3f} {VScale3:.3f}".format(\
    VScale1 = 0.0,  VScale2 = 0.0,  VScale3 = 0.5), \
    "{CScale1:.3f} {CScale2:.3f} {CScale3:.3f}".format(\
    CScale1 = 0.0, CScale2 = 0.0, CScale3 = -1.2))
"""
VType = 3        vdW type             Arithmetic (as for Amber)
CType = 1        Coulomb type         1/R
VCutoff          vdW cut-off          in unit Anstrom, + for hard cut-off, - for soft cut-off, 0 for no cut-off
CCutoff          Coulomb cut-off      same as above
VScale1-3        vdW scale for 1-2, 1-3, and 1-4 interaction, + for value, - for 1/abs(value)
CScale1-3        Coulomb scale for 1-2, 1-3, and 1-4 interaction, others same sa above
"""

# atom symbols and mass section
while True:
    buf = ifl.readline()
    if buf.strip() == "": break
"""
seems this section is not needed
"""

# bond length section
buf = ifl.readline() # atom types
printo("!")
printo("! Stretches")
printo("!")
while True:
    buf = ifl.readline()
    if buf.strip() == "": break
    bt = buf[:5].replace("-", " ")
    tmp = buf[5:].lstrip().split()
    rk = float(tmp[0])
    req = float(tmp[1])
    printo("HrmStr1", bt, "{rk:6.1f} {req:7.4f}".format(rk = rk, req = req))
"""
bt             rk                req
xx-xx    kcal/mol/(A**2)      Angstrom
"""

# bond angle section
printo("!")
printo("! Angles")
printo("!")
while True:
    buf = ifl.readline()
    if buf.strip() == "": break
    tt = buf[:8].replace("-", " ")
    tmp = buf[8:].lstrip().split()
    tk = float(tmp[0])
    teq = float(tmp[1])
    printo("HrmBnd1", tt, "  {tk:5.1f}   {teq:6.2f}".format(tk = tk, teq = teq))
"""
tt                tk                teq
xx-xx-xx    kcal/mol/(rad**2)      degree
"""

# dihedral section
printo("!")
printo("! Torsions")
printo("!")
inew = True
while True:
    buf = ifl.readline()
    if buf.strip() == "": break
    if inew:
        pk = [0.0, 0.0, 0.0, 0.0]
        phase = [0, 0, 0, 0]
        pt = buf[:11].replace("X", "*").replace("-", " ")
        idivf = int(buf[11:15])
    tmp = buf[15:].lstrip().split()
    pn = int(float(tmp[2]))
    if pn < 0:
        pn = - pn
        inew = False
    else:
        inew = True
    """
    pn < 0 means to continue for this type of dihedral
    """
    pk[pn - 1] = float(tmp[0])
    phase[pn - 1] = int(float(tmp[1]))
    if inew:
        printo("AmbTrs", pt, "{:3d} {:3d} {:3d} {:3d}".format(* phase), end = "")
        printo("{:7.3f}{:7.3f}{:7.3f}{:7.3f}".format(* pk), "{idivf:4.1f}".format(idivf = float(idivf)))
"""
pt               idvif       pk        phase     pn
xx-xx-xx-xx        int    height/2    degree   float, the (pn - 1) term, negativa for continue
"""

# improper dihedral
printo("!")
printo("! Improper torsions")
printo("!")
while True:
    buf = ifl.readline()
    if buf.strip() == "": break
    impt = buf[:11].replace("X", "*").replace("-", " ")
    tmp = buf[11:].lstrip().split()
    impk = float(tmp[0])
    imphase = float(tmp[1])
    impn = float(tmp[2])
    printo("ImpTrs", impt, "{impk:5.1f}  {imphase:5.1f} {impn:3.1f}".format(\
        impk = impk, imphase = imphase, impn = impn))
"""
impt              impk      imphase      impn
xx-xx-xx-xx     height/2     degree    float, the (pn - 1) term, negativa for continue
"""

# van der Waals
while True:
    buf = ifl.readline()
    if "RE" in buf: break
printo("!")
printo("! Vanderwaals parameters")
printo("!")
while True:
    buf = ifl.readline()
    if buf.strip() == "": break
    atomname = buf[2:4]
    tmp = buf[4:].lstrip().split()
    r_m_div_2 = float(tmp[0])
    epsilon = float(tmp[1])
    epsilon_print = ("{:6.4f}" if (epsilon >= 1e-4) or (epsilon < 1e-8) else "{:.3e}").format(epsilon)
    printo("VDW", atomname, "{r_m_div_2:6.4f}  {epsilon_print:6s}".format(\
        r_m_div_2 = r_m_div_2, epsilon_print = epsilon_print))

# end
buf = ifl.readline()
if not ("END" in buf):
    raise ValueError("File not ended")

# close files
ifl.close()
ofl.close()
