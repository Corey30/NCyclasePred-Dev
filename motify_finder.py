import re
from input_check import input_check
from calculate_properties import calculate_weighted_properties


def match_gc_motif(window):
    """
    Check if sequence matches GC motif pattern
    GC motif: [RK]X[SCG]X(10)[KR]X(0,2)[DE]
    """
    gc_pattern =  r'[KS][CGS].{8,12}[KR].{0,3}[DE]'

    return bool(re.match(gc_pattern, window))


def match_ac_motif(window):
    """
    Check if sequence matches AC motif pattern
    AC motif: [KSR]X[DE]X(8,12)[KR]X(0,3)[DE]
    """
    ac_pattern = r'[KS][DE].{8,12}[KR].{0,3}[DE]'
    return bool(re.match(ac_pattern, window))


def find_gc_hits(sequences):
    window_size = 14  # 固定窗口大小为14，与原始代码保持一致
    result = {}  # Final dictionary to store results

    for seq_name, sequence in sequences.items():
        sequence_hits = {}  # Temporary dictionary for this sequence's hits

        # If the sequence length is smaller than the sliding window size, skip processing
        if len(sequence) < window_size:
            continue

        # Sliding window approach
        for i in range(len(sequence) - window_size + 1):
            window = sequence[i:i + window_size]
            if match_gc_motif(window):
                try:
                    properties = input_check(window,check_type="GC")
                    start = i + 1  # 1-based position for display
                    end = i + window_size
                    location = f"{start}-{end}"  # Use location as the key

                    weighted_props = calculate_weighted_properties(window)

                    sequence_hits[location] = {
                        "amino_acid_sequence": window,
                        "properties": properties,
                        "weighted_properties": weighted_props
                    }
                except ValueError as e:
                    continue  # Skip invalid sequences

        # Only add to the result if there are hits for this sequence
        if sequence_hits:
            result[seq_name] = sequence_hits

    return result

def find_ac_hits(sequences):
    """
    Find AC motif positions in sequences using sliding window approach

    """
    window_size = 14  # 固定窗口大小为14，与原始代码保持一致
    result = {}  # Final dictionary to store results

    for seq_name, sequence in sequences.items():
        sequence_hits = {}  # Temporary dictionary for this sequence's hits

        # If the sequence length is smaller than the sliding window size, skip processing
        if len(sequence) < window_size:
            continue

        # Sliding window approach
        for i in range(len(sequence) - window_size + 1):
            window = sequence[i:i + window_size]
            if match_ac_motif(window):
                try:
                    properties = input_check(window,check_type="AC")
                    start = i + 1  # 1-based position for display
                    end = i + window_size
                    location = f"{start}-{end}"  # Use location as the key

                    weighted_props = calculate_weighted_properties(window)

                    sequence_hits[location] = {
                        "amino_acid_sequence": window,
                        "properties": properties,
                        "weighted_properties": weighted_props
                    }
                except ValueError as e:
                    continue  # Skip invalid sequences

        # Only add to the result if there are hits for this sequence
        if sequence_hits:
            result[seq_name] = sequence_hits

    return result


def generate_hit_markers(sequence, hits):
    """
    Generate hit markers for sequence visualization
    """
    sequence_len = len(sequence)
    hit_markers = [0] * sequence_len  # Initialize hit markers to track hits at each position

    for hit_key in hits:
        try:
            parts = list(map(int, hit_key.split('-')))
            if len(parts) != 2:
                continue  # If the hit_key is not in the format "start-end", skip it

            start, end = sorted(parts)  # Sort to ensure start < end
            start = max(1, start)  # Convert to 1-based index
            end = min(sequence_len, end)  # Ensure end is within the sequence length

            if start > end:
                continue  # Skip invalid ranges (start > end)

            # Mark the hit region (converted to 0-based index)
            for i in range(start - 1, end):
                hit_markers[i] += 1  # Increment the hit marker for this position

        except (ValueError, AttributeError):
            continue  # Skip if there is an error in parsing the hit_key

    return hit_markers