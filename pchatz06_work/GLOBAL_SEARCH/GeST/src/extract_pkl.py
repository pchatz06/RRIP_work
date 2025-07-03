import os

import pickle



# === Import GeST classes ===

from Individual import Individual

from Population import Population

from Algorithm import Algorithm




# === Directory containing the .pkl files ===

PKL_DIR = "/home/pchatz06/RRIP_work/pchatz06_work/GLOBAL_SEARCH/Results/25-04-18-17-34"  # Change to your actual folder



# === Function to load a pickle file safely ===

def load_pickle(filepath):

    try:

        with open(filepath, 'rb') as f:

            obj = pickle.load(f)

            print(f"✅ Loaded {filepath}")

            return obj

    except Exception as e:

        print(f"❌ Failed to load {filepath}: {e}")

        return None



# === Load and process all .pkl files ===

def load_all_pickles(directory):

    loaded_objects = []



    for file in os.listdir(directory):

        if file.endswith(".pkl"):

            path = os.path.join(directory, file)

            obj = load_pickle(path)



            # Optional: check type

            if isinstance(obj, Individual):

                print(f"→ Individual with chromosome: {obj.chromosome}")

            elif isinstance(obj, Population):

                print(f"→ Population with {len(obj.individuals)} individuals.")

            elif isinstance(obj, Algorithm):

                print(f"→ Algorithm instance loaded.")

            else:

                print("→ Unknown or custom object type.")



            loaded_objects.append(obj)



    return loaded_objects



# === Run ===

if __name__ == "__main__":

    objects = load_all_pickles(PKL_DIR)

    print(f"\nTotal loaded objects: {len(objects)}")


