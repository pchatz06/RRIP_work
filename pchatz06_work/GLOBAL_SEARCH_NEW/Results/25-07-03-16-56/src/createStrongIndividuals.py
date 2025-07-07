#!/usr/bin/env python3

import os, re, random, pickle

from Population import Population

from Individual import Individual

from Instruction import Instruction

from Operand import Operand



# -------------------------------------------------------------------------

# CONFIGURATION

# -------------------------------------------------------------------------

OUT_DIR    = "/home/pchatz06/Individuals"

OUT_FILE   = os.path.join(OUT_DIR, "1.pkl")

BENCHMARKS = [

    "Blender", "Cam4", "CactuBSSN", "Parest", "Wrf", "Lbm", "Fotonik3d",

    "Xalancbmk", "Omnetpp", "Gcc",     "Roms", "Xz",  "X264", "Mcf"

]

PREFIX2TYPE = {

    'L': "LOAD",

    'R': "RFO",

    'P': "PREFETCH",

    'W': "WRITEBACK"

}

LINE_RE = re.compile(r'^\s*([LRPW]_[A-Za-z0-9_]+)\s+%?(\d+)\s*$')



os.makedirs(OUT_DIR, exist_ok=True)



# -------------------------------------------------------------------------

# Helpers

# -------------------------------------------------------------------------

def find_crossover_folder(b):

    """Try 3 locations in turn."""

    paths = [

        f"/home/pchatz06/Thesis_{b}/Fittest_Results_MiddleCrossover",

        f"/home/pchatz06/{b}/Fittest_Results_MiddleCrossover",

        "/home/pchatz06/Thesis/Fittest_Results_MiddleCrossover"

    ]

    for p in paths:
        if(b=="Mcf"):
            return "/home/pchatz06/Thesis/Fittest_Results_MiddleCrossover"
	
        if os.path.isdir(p):

            return p
	

    return None



def parse_txt_to_sequence(txt_path):

    seq = []

    with open(txt_path) as f:

        for line in f:

            m = LINE_RE.match(line)

            if not m:

                continue

            name, opnum = m.groups()

            itype = PREFIX2TYPE[name[0]]

            inst = Instruction(name=name, ins_type=itype, numOfOperands=1)

            val = int(opnum)

            op = Operand(

                id="op",

                type="constant",

                values=[val],

                min=val, max=val, stride=1

            )

            op.currentValue = val

            inst.operands = [op]

            seq.append(inst)

    if len(seq) != 20:

        raise RuntimeError(f"{txt_path!r}: expected 20, got {len(seq)}")

    return seq



# -------------------------------------------------------------------------

# Build population

# -------------------------------------------------------------------------

all_txts = []

for b in BENCHMARKS:

    folder = find_crossover_folder(b)

    if not folder:

        print(f"skipping {b}: no folder")

        continue

    cands = [f for f in os.listdir(folder)

             if f.endswith(".txt") and f[0].isdigit()]

    if not cands:

        print(f"{folder} has no suitable .txt")

        continue

    chosen = random.sample(cands, min(3, len(cands)))

    for fn in chosen:

        all_txts.append(os.path.join(folder, fn))



if not all_txts:

    print("❌ no individuals found, nothing to do.")

    exit(1)



individuals = []

for idx, txt in enumerate(all_txts, start=1):

    try:

        seq = parse_txt_to_sequence(txt)

        ind = Individual(sequence=seq, generation=1)

        # optional: set your own ID field if needed, e.g. ind.myId = idx

        individuals.append(ind)

        print(f"✅ parsed {txt}")

    except Exception as e:

        print(f"❌ failed {txt}: {e}")



# -------------------------------------------------------------------------

# Dump the single‐generation population

# -------------------------------------------------------------------------

pop = Population(individuals)

with open(OUT_FILE, "wb") as f:

    pickle.dump(pop, f)



print(f"\n Wrote generation (size={len(individuals)}) to {OUT_FILE}")


