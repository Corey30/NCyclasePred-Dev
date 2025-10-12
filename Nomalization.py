def normalize_acc_values(amino_sequence, amino_acid_properties):
    """
    Normalize the amino acid sequence
    """
    if not amino_sequence or len(amino_sequence) != 14:
        print(f"Warning: The length of sequence should be 14, current is {len(amino_sequence) if amino_sequence else 0}")
        return {'GH': 0.8, 'GW': 0.75, 'GP': 0.82, 'G': 0.79}  # default value

    # Get property values for all amino acids
    hydrophobicity_values = []
    mw_values = []
    ip_values = []

    # Collect property values for the sequence
    for aa in amino_sequence:
        if aa in amino_acid_properties:
            hydrophobicity_values.append(amino_acid_properties[aa]['hydrophobicity'])
            mw_values.append(amino_acid_properties[aa]['molecular_weight'])
            ip_values.append(amino_acid_properties[aa]['isoelectric_point'])
        else:
            print(f"Warning: Unknown amino acid '{aa}'")
            # Use average values as default
            hydrophobicity_values.append(0)
            mw_values.append(100)
            ip_values.append(6)

    # Calculate reference values (max and min of all possible amino acids)
    all_hydro = [props['hydrophobicity'] for props in amino_acid_properties.values()]
    all_mw = [props['molecular_weight'] for props in amino_acid_properties.values()]
    all_ip = [props['isoelectric_point'] for props in amino_acid_properties.values()]

    max_hydro_diff = max(all_hydro) - min(all_hydro)
    max_mw_diff = max(all_mw) - min(all_mw)
    max_ip_diff = max(all_ip) - min(all_ip)

    # Calculate averages
    avg_hydro = sum(all_hydro) / len(all_hydro)
    avg_mw = sum(all_mw) / len(all_mw)
    avg_ip = sum(all_ip) / len(all_ip)

    # Calculate normalized values according to paper's formula
    # GH = (sum(1 - |Pc - μc|/max(|Pi - μi|)) + sum(1)) / 14
    GH_values = []
    for value in hydrophobicity_values:
        if max_hydro_diff > 0:
            # Calculate deviation from mean and normalize
            normalized = 1 - (abs(value - avg_hydro) / max_hydro_diff)
            GH_values.append(normalized)
        else:
            GH_values.append(1)

    # Calculate GW (molecular weight)
    # GW = (sum(1 - |Wc - μw|/max(|Wi - μw|)) + sum(1)) / 14
    GW_values = []
    for value in mw_values:
        if max_mw_diff > 0:
            normalized = 1 - (abs(value - avg_mw) / max_mw_diff)
            GW_values.append(normalized)
        else:
            GW_values.append(1)

    # Calculate GP (isoelectric point)
    # GP = (sum(1 - |Ic - μi|/max(|Ii - μi|)) + sum(1)) / 14
    GP_values = []
    for value in ip_values:
        if max_ip_diff > 0:
            normalized = 1 - (abs(value - avg_ip) / max_ip_diff)
            GP_values.append(normalized)
        else:
            GP_values.append(1)

    # Calculate final normalized values
    GH = sum(GH_values) / len(GH_values) if GH_values else 0
    GW = sum(GW_values) / len(GW_values) if GW_values else 0
    GP = sum(GP_values) / len(GP_values) if GP_values else 0

    # Calculate overall value
    G = (GH + GW + GP) / 3

    # Ensure all values are within 0-1 range
    GH = max(0, min(1, GH))
    GW = max(0, min(1, GW))
    GP = max(0, min(1, GP))
    G = max(0, min(1, G))

    return {
        'GH': GH,
        'GW': GW,
        'GP': GP,
        'G': G
    }