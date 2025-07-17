import matplotlib.pyplot as plt
Markos_LRU = {
    "x264": 1.372, "cactuBSSN": 0.761, "Fotonik3d": 0.621, "Gcc": 0.353, 
    "Cam4": 0.725, "Xz": 0.894, "Omnetpp": 0.246, "Roms": 1.079, 
    "Blender": 0.661, "Mcf": 0.400, "Wrf": 0.823, "Lbm": 0.652, 
    "Parest": 0.935, "Xalancbmk": 0.395
}
Markos_SRRIP = {
    "Blender": 0.670, "Bwaves": 1.016, "Cam4": 0.731, "cactuBSSN": 0.755,
    "Exchange": 1.127, "Gcc": 0.353, "Lbm": 0.698, "Mcf": 0.402,
    "Parest": 1.025, "Povray": 0.356, "Wrf": 0.826, "Xalancbmk": 0.433,
    "Fotonik3d": 0.620, "Imagick": 2.191, "Leela": 0.548, "Omnetpp": 0.248,
    "Perlbench": 0.448, "Roms": 1.048, "x264": 1.365, "Xz": 0.900 
}
MINE_LRU = {
    "x264": 1.372, "cactuBSSN": 0.761, "Fotonik3d": 0.621, "Gcc": 0.353,
    "Cam4": 0.725, "Xz": 0.894, "Omnetpp": 0.246, "Roms": 1.079,
    "Blender": 0.661, "Mcf": 0.400, "Wrf": 0.823, "Lbm": 0.652,
    "Parest": 0.935, "Xalancbmk": 0.395, "Perlbench": 0.448, "Exchange": 1.127,
    "Leela": 0.548, "Povray": 0.356, "Imagick": 2.193, "Bwaves": 1.016
}
MINE_SRRIP = {
    "x264": 1.365, "cactuBSSN": 0.755, "Fotonik3d": 0.620, "Gcc": 0.353,
    "Cam4": 0.731, "Xz": 0.900, "Omnetpp": 0.248, "Roms": 1.047,
    "Blender": 0.670, "Mcf": 0.402, "Wrf": 0.826, "Lbm": 0.698,
    "Parest": 1.025, "Xalancbmk": 0.433, "Perlbench": 0.448, "Exchange": 1.127,
    "Leela": 0.548, "Povray": 0.356, "Imagick": 2.192, "Bwaves": 1.016
}

# Ensure consistent ordering
common_keys = sorted(set(MINE_LRU.keys()) & set(Markos_LRU.keys()))
common_keys_srrip = sorted(set(MINE_SRRIP.keys()) & set(Markos_SRRIP.keys()))

# Extract values
mine_lru_vals = [MINE_LRU[k] for k in common_keys]
markos_lru_vals = [Markos_LRU[k] for k in common_keys]

mine_srrip_vals = [MINE_SRRIP[k] for k in common_keys_srrip]
markos_srrip_vals = [Markos_SRRIP[k] for k in common_keys_srrip]

x_lru = range(len(common_keys))
x_srrip = range(len(common_keys_srrip))

# Plotting
fig, axs = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

# LRU plot
axs[0].bar(x_lru, mine_lru_vals, width=0.4, label='MINE', align='center')
axs[0].bar([x + 0.4 for x in x_lru], markos_lru_vals, width=0.4, label='Markos', align='center')
axs[0].set_title('LRU Comparison')
axs[0].set_xticks([x + 0.2 for x in x_lru])
axs[0].set_xticklabels(common_keys, rotation=90)
axs[0].legend()

# SRRIP plot
axs[1].bar(x_srrip, mine_srrip_vals, width=0.4, label='MINE', align='center')
axs[1].bar([x + 0.4 for x in x_srrip], markos_srrip_vals, width=0.4, label='Markos', align='center')
axs[1].set_title('SRRIP Comparison')
axs[1].set_xticks([x + 0.2 for x in x_srrip])
axs[1].set_xticklabels(common_keys_srrip, rotation=90)
axs[1].legend()

plt.tight_layout()
plt.savefig("comparison.png")

