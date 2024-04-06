import numpy as np
import matplotlib.pyplot as plt


def plot_array(arr, id):
    # Generate random data (replace this with your actual data)
    data = arr

    # Specify the percentile you want to display
    percentiles = [25, 50, 75]

    # Calculate the percentile values
    percentile_values = np.percentile(data, percentiles)

    # Plot the histogram (normalized)
    plt.hist(data, bins=30, density=True, alpha=0.7, color='blue', edgecolor='black')

    for percentile, percentile_value in zip(percentiles, percentile_values):
        plt.axvline(percentile_value, color='red', linestyle='dashed', linewidth=1)
        plt.text(percentile_value + 0.1, plt.ylim()[1] * 0.9 - percentile * 0.01,
                 f'{percentile}th percentile: {percentile_value:.2f}', color='red')

    # Add labels and title
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.title('Normalized Histogram with Percentiles')

    plt.savefig('hst_id_{}.png'.format(id))
    plt.close()
    # plt.show()
