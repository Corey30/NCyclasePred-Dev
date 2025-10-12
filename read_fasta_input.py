import os.path
import os
import re
import os

def read_fasta_input(input):
    sequences = {}  # Used to store sequence name and sequence content
    seq_name = ''
    sequence = ''
    seq_name_buffer = ''  # Stores the sequence name which might span across multiple lines

    if os.path.isfile(input):  # Check if the input is a file
        try:
            with open(input, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            raise ValueError(f"File {input} not found.")  # Raise an error if file is not found
    else:
        lines = input.strip().splitlines()  # If input is a string, split it into lines

    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespace

        if line.startswith('>'):  # If the line starts with '>', it's a sequence name line
            if seq_name and sequence:  # If there is already a sequence name and sequence
                sequences[seq_name] = sequence  # Save the previous sequence
                sequence = ''  # Reset the sequence

            # Handle cases where sequence name might span multiple lines
            if seq_name_buffer:  # If there was a previous sequence name in the buffer, concatenate the new part
                seq_name_buffer += ' ' + line[1:]  # Remove '>' and append the new part
            else:
                seq_name_buffer = line[1:]  # If no buffered name, start a new sequence name

            seq_name = seq_name_buffer
            seq_name_buffer = ''  # Reset the name buffer for the next sequence name

        elif line:  # If it's a non-empty line and not a sequence name, it must be sequence content
            sequence += line  # Append the sequence data

        if not line.startswith('>') and not line:  # If an empty line is encountered, handle end of multi-line name
            seq_name_buffer = ''  # Clear the name buffer

    # Save the last sequence into the dictionary
    if seq_name and sequence:
        sequences[seq_name] = sequence

    #If no sequences are found and there is a single sequence, not assign it a default name
    # if not sequences and sequence:
    #    sequences["Single_Sequence"] = sequence

    return sequences


def format_sequence_with_position(sequence, line_length=100):
    # Format sequence into lines of length `line_length`, displaying the global position at the start of each line
    formatted_sequence = ""
    for i in range(0, len(sequence), line_length):
        position = i + 1  # Calculate the starting position of each line, position starts from 1
        line = sequence[i:i + line_length]
        formatted_sequence += f"{position:>8}  {line}\n"  # Right-align the position for a clean format
    return formatted_sequence
