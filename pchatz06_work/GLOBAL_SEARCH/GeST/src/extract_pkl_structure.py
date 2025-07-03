#!/usr/bin/env python3

"""

extract_pkl_structure.py



Loads a GeST Population pickle and prints out, for each individual:

 - its fitness (safely formatted even if stored as string)

 - each instruction name

 - the operand value(s) currently assigned to that instruction

"""



import os

import sys

import pickle

from Population import Population

from Individual import Individual

from Instruction import Instruction

from Operand import Operand



def detect_slots(pop: Population):

    """

    Inspect the first individual and find any

    attribute names that hold Operand slots.

    Assumes that instructions have attributes

    like .operands (a dict or list).

    """

    sample = pop.individuals[0]

    slots = []

    # look for any attribute on Instruction holding Operand or list thereof:

    inst = sample.sequence[0]

    for attr in dir(inst):

        val = getattr(inst, attr)

        if isinstance(val, Operand):

            slots.append(attr)

        elif isinstance(val, list) and val and isinstance(val[0], Operand):

            slots.append(attr)

    return slots



def get_instruction_values(inst: Instruction, slots):

    """

    Given an instruction and the list of operand‐slots,

    extract the currentValue of each.

    """

    out = []

    for slot in slots:

        val = getattr(inst, slot)

        if isinstance(val, Operand):

            out.append(val.getValue())

        elif isinstance(val, list):

            # e.g. list of Operands

            for op in val:

                out.append(op.getValue())

    return out



def print_individual_features(pop: Population):

    """

    Print all individuals in pop, with fitness and full

    instruction→operand‐value listing.

    """

    slots = detect_slots(pop)

    print(f"🔍 Loading population from: {pop._file_path}")

    print(f"→ Population size: {len(pop.individuals)} individuals")

    print(f"→ detected instruction‐value slots: {slots}\n")



    for idx, indiv in enumerate(pop.individuals, start=1):

        # safe formatting of fitness

        raw_fit = indiv.getFitness()

        try:

            fit_val = float(raw_fit)

            fit_str = f"{fit_val:.6f}"

        except Exception:

            fit_str = str(raw_fit)



        print(f"Individual {idx}: (fitness={fit_str})")

        for step, inst in enumerate(indiv.sequence, start=1):

            name = getattr(inst, 'name', f"<inst@{step}>")

            vals = get_instruction_values(inst, slots)

            # if there's exactly one operand, don't wrap in list

            if len(vals) == 1:

                vals = vals[0]

            print(f"  [{step:2d}] {name:20s} → {vals}")

        print()



def main():

    if len(sys.argv) != 2:

        print("Usage: python extract_pkl_structure.py /path/to/results_dir/")

        sys.exit(1)



    path = sys.argv[1]

    if not os.path.isdir(path):

        print(f"Error: '{path}' is not a directory.")

        sys.exit(1)



    # find all .pkl population files (ignore rand or seed files)

    files = []

    for root, dirs, filenames in os.walk(path):

        for f in filenames:

            if f.endswith(".pkl") and "rand" not in f:

                files.append(os.path.join(root, f))

    if not files:

        print("No .pkl files found under", path)

        sys.exit(1)



    # sort by the numeric prefix, e.g. "2.pkl", "3.pkl", ...

    files.sort(key=lambda x: int(os.path.basename(x).split(".")[0]))



    # Just load the last one (or you can loop over them)

    pkl_file = files[-1]

    with open(pkl_file, "rb") as inp:

        pop = pickle.load(inp)

    # stash file path for printing

    pop._file_path = pkl_file



    print_individual_features(pop)





if __name__ == "__main__":

    main()


