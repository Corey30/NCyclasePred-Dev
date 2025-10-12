import pandas as pd
import base64
from visualization import generate_color_scale


def generate_downloadable_csv(df):
    """
    Convert DataFrame to downloadable CSV format
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return b64


def create_results_table(results):
    """
    Create results table from motif hits

    """
    all_hits = []
    for seq_name, hits in results.items():
        for position, hit_data in hits.items():
            properties = hit_data["properties"]
            weighted_props = hit_data["weighted_properties"]

            gh_color = generate_color_scale(weighted_props['GH'])
            gw_color = generate_color_scale(weighted_props['GW'])
            gp_color = generate_color_scale(weighted_props['GP'])
            g_color = generate_color_scale(weighted_props['G'])

            all_hits.append({
                "Protein  Name": seq_name,
                "Position": position,
                "Matched Sequence": hit_data["amino_acid_sequence"],
                "Avg Hydrophobicity": f"{properties['average_hydrophobicity']:.2f}",
                "Avg MW": f"{properties['average_molecular_weight']:.2f}",
                "Avg pI": f"{properties['average_isoelectric_point']:.2f}",
                "GH Score": f"<span style='color:{gh_color};'>{weighted_props['GH']:.3f}</span>",
                "GW Score": f"<span style='color:{gw_color};'>{weighted_props['GW']:.3f}</span>",
                "GP Score": f"<span style='color:{gp_color};'>{weighted_props['GP']:.3f}</span>",
                "G Overall": f"<span style='color:{g_color};'>{weighted_props['G']:.3f}</span>"
            })
    return pd.DataFrame(all_hits)


