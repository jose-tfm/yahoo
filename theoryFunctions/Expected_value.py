import numpy as np
import matplotlib.pyplot as plt

numbers = np.array([1, 2, 3, 4, 5, 6])
probabilities = np.full(6, 1/6)

Expected_value = 0
for i in range(len(numbers)): 
    Expected_value += numbers[i] * probabilities[i]
#Expected_value = np.sum(numbers * probabilities)
print(f'Expected value is ', Expected_value)

np.random.seed(42)  # for reproducibility
# Take from numbers, 1000 random choices, p = probability associated with each value number
samples = np.random.choice(numbers, size=1000, p = probabilities)


average = np.mean(samples)
print(f'Average', average)

# Compute running average
running_avg = np.cumsum(samples) / np.arange(1, len(samples) + 1)

variance = np.sum((numbers - Expected_value) ** 2 * probabilities)
print(f'Variance is ', variance)

# The idea is to plot the evolution of the sample average as we take more samples
plt.figure(figsize=(10, 5))
plt.plot(running_avg, label='Sample Running Average', color='orange')
plt.axhline(Expected_value, color='blue', linestyle='--', label='Expected Value')
plt.ylabel('Value')
plt.xlabel('Sample Size')
plt.title('Evolution of Sample Average vs Expected Value')
plt.legend()
plt.show()

