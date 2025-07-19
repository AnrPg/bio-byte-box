#!/usr/bin/env python3

import collections

DNA_NUCLEOTIDES: list[str] = ["A", "C", "G", "T", "a", "c", "g", "t"]
RNA_NUCLEOTIDES: list[str] = ["A", "C", "G", "U", "a", "c", "g", "u"]
DNA_COMPLEMENTS: dict[str, str] = {
    "A": "T",
    "C": "G",
    "G": "C",
    "T": "A",
    "a": "t",
    "c": "g",
    "g": "c",
    "t": "a",
}
RNA_COMPLEMENTS: dict[str, str] = {
    "A": "U",
    "C": "G",
    "G": "C",
    "U": "A",
    "a": "u",
    "c": "g",
    "g": "c",
    "u": "a",
}


def is_valid_dna_sequence(sequence: str) -> bool:
    """Check if the given sequence is a valid DNA sequence.
    A valid DNA sequence contains only the nucleotides A, C, G, and T."""
    return all(nucleotide in DNA_NUCLEOTIDES for nucleotide in sequence)


def is_valid_rna_sequence(sequence: str) -> bool:
    """Check if the given sequence is a valid RNA sequence.
    A valid RNA sequence contains only the nucleotides A, C, G, and U."""
    return all(nucleotide in RNA_NUCLEOTIDES for nucleotide in sequence)


def complement_dna_sequence(sequence: str) -> str:
    """Return the complementary DNA sequence."""
    return "".join(DNA_COMPLEMENTS[nucleotide] for nucleotide in sequence)


def complement_rna_sequence(sequence: str) -> str:
    """Return the complementary RNA sequence."""
    return "".join(RNA_COMPLEMENTS[nucleotide] for nucleotide in sequence)


def transcribe_dna(dna_sequence: str) -> str:
    """Transcribe a DNA sequence into RNA."""
    if not is_valid_dna_sequence(dna_sequence):
        raise ValueError("Invalid DNA sequence")
    return dna_sequence.replace("T", "U")


def reverse_transcribe_rna(rna_sequence: str) -> str:
    """Reverse transcribe an RNA sequence into DNA."""
    if not is_valid_rna_sequence(rna_sequence):
        raise ValueError("Invalid RNA sequence")
    return rna_sequence.replace("U", "T")


def normalize_sequence(sequence: str, is_dna: bool = True) -> str:
    """Normalize a DNA or RNA sequence by converting it to uppercase and validating it.
    Raises ValueError if the sequence is invalid or empty."""
    if not isinstance(sequence, str):
        raise ValueError("Sequence must be a string")
    sequence = sequence.strip()
    if not sequence:
        raise ValueError("Sequence cannot be empty")
    if is_dna:
        if not is_valid_dna_sequence(sequence):
            raise ValueError("Invalid DNA sequence")
    else:
        if not is_valid_rna_sequence(sequence):
            raise ValueError("Invalid RNA sequence")
    sequence = sequence.upper()
    return sequence


def count_nucleotides(sequence: str, is_dna: bool = True) -> collections.Counter:
    """Count the occurrences of each nucleotide in a DNA or RNA sequence.
    Returns a Counter object with nucleotide counts."""
    normalize_sequence(sequence, is_dna)
    return collections.Counter(sequence)


def nucleotide_frequencies(sequence: str, is_dna: bool = True) -> dict[str, float]:
    """Calculate the frequency of each nucleotide in a DNA or RNA sequence.
    Returns a dictionary with nucleotide frequencies."""
    normalize_sequence(sequence, is_dna)
    total_nucleotides = len(sequence)
    if total_nucleotides == 0:
        return {
            nucleotide: 0
            for nucleotide in (DNA_NUCLEOTIDES if is_dna else RNA_NUCLEOTIDES)
        }
    counts = count_nucleotides(sequence, is_dna)
    return {
        nucleotide: counts[nucleotide] / total_nucleotides
        for nucleotide in (DNA_NUCLEOTIDES if is_dna else RNA_NUCLEOTIDES)
    }
