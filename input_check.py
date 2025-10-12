from Protein_Database import AMINO_ACID_PROPERTIES


def input_check(sequence, check_type="GC"):
    """
    Calculate the average properties (hydrophobicity, molecular weight, and isoelectric point)
    with position-specific validation rules for either AC or GC type sequences.

    """
    hydrophobicity = 0
    molecular_weight = 0
    isoelectric_point = 0
    invalid_count = 0

    # Check sequence length
    if len(sequence) != 14:
        raise ValueError("Sequence length must be 14 amino acids")

    # Define position-specific rules for each type
    validation_rules = {
        "AC": {
            0: ('K', 'S'),  # 1st position
            2: ('D', 'E'),  # 3rd position
            11: ('K', 'R'),  # 12th position
            13: ('D', 'E')  # 14th position
        },
        "GC": {
            0: ('K', 'S'),  # 1st position
            2: ('S', 'C', 'G'),  # 3rd position
            11: ('K', 'R'),  # 12th position
            13: ('D', 'E')  # 14th position
        }
    }

    # Get the appropriate rules
    rules = validation_rules.get(check_type)
    if not rules:
        raise ValueError("Invalid check_type. Must be 'AC' or 'GC'")

    # Process each amino acid
    for idx, aa in enumerate(sequence):
        # Check if this position has validation rules
        if idx in rules and aa not in rules[idx]:
            invalid_count += 1
            continue

        # If amino acid is valid, add its properties
        if aa in AMINO_ACID_PROPERTIES:
            hydrophobicity += AMINO_ACID_PROPERTIES[aa]['hydrophobicity']
            molecular_weight += AMINO_ACID_PROPERTIES[aa]['molecular_weight']
            isoelectric_point += AMINO_ACID_PROPERTIES[aa]['isoelectric_point']
        else:
            invalid_count += 1

    # Calculate averages
    valid_count = len(sequence) - invalid_count
    if valid_count <= 0:
        raise ValueError("Not enough valid amino acids in sequence to calculate averages")

    return {
        'average_hydrophobicity': hydrophobicity / valid_count,
        'average_molecular_weight': molecular_weight / valid_count,
        'average_isoelectric_point': isoelectric_point / valid_count
    }