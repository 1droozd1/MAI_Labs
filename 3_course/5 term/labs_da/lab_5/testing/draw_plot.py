import matplotlib.pyplot as plt

# Data
text_lengths = [10**i for i in range(1, 8)]
find_times = [0.000002, 0.000001, 0.000003, 0.000012, 0.000070, 0.000940, 0.011512]
kmp_times = [0.000005, 0.000014, 0.000074, 0.001381, 0.007307, 0.098278, 1.040296]
suffix_tree_times = [4.125e-06, 1.8708e-05, 2.3167e-05, 0.000489667, 0.00111033, 0.017905, 0.189559]

# Plot
plt.figure(figsize=(10,6))
plt.loglog(text_lengths, find_times, 'o-', label='Find Time', markersize=8)
plt.loglog(text_lengths, kmp_times, 's-', label='KMP Time', markersize=8)
plt.loglog(text_lengths, suffix_tree_times, '^-', label='Suffix Tree', markersize=8)
plt.xlabel('Text Length', fontsize=14)
plt.ylabel('Time (seconds)', fontsize=14)
plt.title('Time vs Text Length', fontsize=16)
plt.legend()
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.tight_layout()

plt.show()