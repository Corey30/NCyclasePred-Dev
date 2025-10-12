import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from Protein_Database import AMINO_ACID_PROPERTIES
from Nomalization import normalize_acc_values


def generate_color_scale(value, threshold_low=0.3, threshold_high=0.7):
    """
    Generate color based on value thresholds
    """
    if value < threshold_low:
        return "red"
    elif value > threshold_high:
        return "green"
    else:
        return "orange"


amino_acid_properties=AMINO_ACID_PROPERTIES



def plot_weighted_properties(hit_data, seq_name, position):
    """
    for score distribution
    """
    # get hit sequences
    if "amino_acid_sequence" in hit_data:
        amino_sequence = hit_data["amino_acid_sequence"]
    else:
        print("sorry,can't find amino_acid_sequence")
        amino_sequence = "AAAAAAAAAAAAA"  # 默认序列用于测试

   #Normalization
    weighted_props = normalize_acc_values(amino_sequence, AMINO_ACID_PROPERTIES)
    hit_data["weighted_properties"] = weighted_props


    df = pd.DataFrame({
        'Property': ['GH (Hydrophobicity)', 'GW (Molecular Weight)', 'GP (Isoelectric)', 'G (Overall)'],
        'Value': [weighted_props['GH'], weighted_props['GW'], weighted_props['GP'], weighted_props['G']]
    })


    fig, ax = plt.subplots(figsize=(16, 10), dpi=150)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')


    colors = [generate_color_scale(v, 0.5, 0.7) for v in df['Value']]


    bars = ax.bar(
        df['Property'],
        df['Value'],
        color=colors,
        width=0.65,
        edgecolor='none'
    )


    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height + 0.03,
            f'{height:.3f}',
            ha='center',
            va='bottom',
            fontweight='bold',
            fontsize=16
        )


    ax.axhline(y=0.5, color='orange', linestyle='--', alpha=0.3)
    ax.axhline(y=0.7, color='g', linestyle='--', alpha=0.3)
    ax.axhline(y=0.3, color='r', linestyle='--', alpha=0.3)


    full_title = f'Score distribution of Weighted Properties for {seq_name} at {position}'
    ax.set_title(full_title, fontsize=16, fontweight='bold', pad=10)


    ax.set_ylim(0, 1.1)
    ax.set_xlabel('Properties', fontsize=16)
    ax.set_ylabel('Score (0-1)', fontsize=16)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)


    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


    ax.grid(axis='y', alpha=0.2, linestyle='-', color='gray')


    plt.tight_layout()

    return fig


def generate_sequence_panel_html(sequence, hit_markers, line_width=100):
    """
    Generate HTML for colored sequence panel with hit highlighting
    """
    sequence_len = len(sequence)
    html_lines = []

    for line_num in range(0, sequence_len, line_width):
        line_start = line_num
        line_end = min(line_num + line_width, sequence_len)
        line_segment = sequence[line_start:line_end]  # Extract the current line segment

        colored_line = []  # List to store colored characters
        for idx, char in enumerate(line_segment):
            pos = line_start + idx  # 0-based position in the full sequence
            marker = hit_markers[pos]  # Get the hit marker for this position

            # Apply color based on the marker value
            if marker > 1:
                colored_line.append(
                    f'<span style="background-color:yellow; font-weight:bold;">{char}</span>')  # Yellow for overlapping hits
            elif marker == 1:
                colored_line.append(
                    f'<span style="background-color:#ffcccc; font-weight:bold;">{char}</span>')  # Light red for single hits
            else:
                colored_line.append(char)  # No hit, no color change

        position = line_start + 1  # Convert to 1-based numbering for display
        html_lines.append(f"<strong>{position:8}</strong>: {''.join(colored_line)}")

    return "<br>".join(html_lines)


def plot_hit_distribution(sequence, hit_markers):
    """
    Create a plot showing the distribution of hits along the sequence
    """
    fig, ax = plt.subplots(figsize=(12, 3))

    x = np.arange(1, len(sequence) + 1)  # 1-based positions

    # Plot hit markers as a heatmap-like plot
    scatter = ax.scatter(x, [1] * len(x), c=hit_markers, cmap='YlOrRd',
                         marker='s', s=50, alpha=0.8, vmin=0, vmax=max(max(hit_markers), 1))

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Hit Count')

    # Customize plot
    ax.set_xlim(0, len(sequence) + 1)
    ax.set_ylim(0, 2)
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_xlabel('Sequence Position')
    ax.set_title('Motif Match Distribution')

    # Add grid lines for better position reference
    ax.grid(alpha=0.3)

    return fig


def plot_property_profile(sequence, properties_list, window_size=5):
    """
    Plot amino acid property profile with sliding window averaging
    """
    # Extract properties for each amino acid in the sequence
    hydrophobicity = []
    molecular_weight = []
    isoelectric_point = []

    for aa in sequence:
        if aa in AMINO_ACID_PROPERTIES:
            props = AMINO_ACID_PROPERTIES[aa]
            hydrophobicity.append(props['hydrophobicity'])
            molecular_weight.append(props['molecular_weight'] / 100)  # Scale down for plotting
            isoelectric_point.append(props['isoelectric_point'])
        else:
            # Use defaults for unknown amino acids
            hydrophobicity.append(0)
            molecular_weight.append(1)
            isoelectric_point.append(7)

    # Calculate running averages
    def running_average(data, window):
        return np.convolve(data, np.ones(window) / window, mode='valid')

    x_positions = np.arange(1, len(sequence) + 1)
    x_avg = np.arange(1 + window_size // 2, len(sequence) + 1 - window_size // 2)

    hydro_avg = running_average(hydrophobicity, window_size)
    mw_avg = running_average(molecular_weight, window_size)
    pi_avg = running_average(isoelectric_point, window_size)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x_avg, hydro_avg, 'b-', label='Hydrophobicity')
    ax.plot(x_avg, mw_avg, 'r-', label='MW (scaled)')
    ax.plot(x_avg, pi_avg, 'g-', label='pI')

    # Add annotations for motif regions
    for i, props in enumerate(properties_list):
        pos = i + 1  # 1-based position
        ax.axvline(x=pos, color='gray', linestyle='--', alpha=0.3)

    ax.set_xlabel('Position in Sequence')
    ax.set_ylabel('Property Value')
    ax.set_title('Amino Acid Property Profile')
    ax.legend()
    ax.grid(True, alpha=0.3)

    return fig