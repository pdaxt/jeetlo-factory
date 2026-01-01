"""
Pronunciation Validator
=======================

Validates audio scripts follow JeetLo pronunciation rules:
1. Scientific terms in Title Case (not ALL CAPS)
2. Acronyms with hyphens (A-T-P, not ATP)
3. Hindi words in Devanagari (भाई, not BHAI)
4. Numbers in English (twenty, not बीस)

This validator runs in CI and CANNOT be bypassed.
"""

import re
from typing import List, Tuple
from ..exceptions import ValidationError


# Scientific terms that should NEVER be in ALL CAPS
SCIENTIFIC_TERMS = [
    "CRISTAE", "MATRIX", "ENDOSYMBIOSIS", "MITOCHONDRIA", "CHLOROPLAST",
    "NUCLEUS", "RIBOSOME", "LYSOSOME", "VACUOLE", "CYTOPLASM", "MEMBRANE",
    "CHROMOSOME", "CHROMATIN", "NUCLEOLUS", "CENTRIOLE", "FLAGELLA",
    "PHOTOSYNTHESIS", "RESPIRATION", "GLYCOLYSIS", "KREBS", "ELECTRON",
    "HEMOGLOBIN", "ERYTHROCYTE", "LEUKOCYTE", "PLATELET", "PLASMA",
    "ENZYME", "PROTEIN", "CARBOHYDRATE", "LIPID", "NUCLEOTIDE",
    "ADENINE", "GUANINE", "CYTOSINE", "THYMINE", "URACIL",
    "TRANSCRIPTION", "TRANSLATION", "REPLICATION", "MUTATION",
    "ALLELE", "GENOTYPE", "PHENOTYPE", "DOMINANT", "RECESSIVE",
    "BICONCAVE", "EUKARYOTE", "PROKARYOTE", "ORGANELLE"
]

# Acronyms that MUST have hyphens
ACRONYMS_NEEDING_HYPHENS = {
    "ATP": "A-T-P",
    "DNA": "D-N-A",
    "RNA": "R-N-A",
    "NEET": "N-E-E-T",
    "JEE": "J-E-E",
    "NCERT": "N-C-E-R-T",
    "RBC": "R-B-C",
    "WBC": "W-B-C",
    "PCR": "P-C-R",
    "IUPAC": "I-U-P-A-C",
    "SN1": "S-N-one",
    "SN2": "S-N-two",
}

# Romanized Hindi words that should be in Devanagari
ROMANIZED_HINDI = [
    "BHAI", "DEKHO", "SAMJHO", "YAAD", "RAKHO", "KARO", "SUNO",
    "PADHO", "LIKHO", "SOCHO", "JANO", "SEEKHO", "BATAO",
    "KYA", "KAISE", "KYUN", "KAHAN", "KAB", "KAUN",
    "HAI", "HO", "HAIN", "THA", "THE", "THI",
    "MATLAB", "ACTUALLY", "BASICALLY",
    "KHUD", "APNA", "HAMARA", "TUMHARA", "USKA", "ISKA",
    "SAARE", "SABHI", "BAHUT", "THODA", "ZYADA"
]


class PronunciationValidator:
    """Validates audio scripts follow pronunciation rules."""

    def __init__(self, content: str):
        self.content = content
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Run all pronunciation validations.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self._check_scientific_terms()
        self._check_acronyms()
        self._check_romanized_hindi()
        self._check_numbers()

        return len(self.errors) == 0, self.errors, self.warnings

    def _check_scientific_terms(self):
        """Check for scientific terms in ALL CAPS."""
        for term in SCIENTIFIC_TERMS:
            pattern = r'\b' + term + r'\b'
            if re.search(pattern, self.content):
                correct = term.title()
                self.errors.append(
                    f"PRONUNCIATION ERROR: '{term}' in ALL CAPS will be spelled letter-by-letter. "
                    f"Use '{correct}' instead."
                )

    def _check_acronyms(self):
        """Check for acronyms without hyphens."""
        for acronym, correct in ACRONYMS_NEEDING_HYPHENS.items():
            # Match the acronym but not if already hyphenated
            pattern = r'\b' + acronym + r'\b(?!-)'
            if re.search(pattern, self.content):
                # Check it's not already the hyphenated version nearby
                if correct not in self.content:
                    self.errors.append(
                        f"PRONUNCIATION ERROR: '{acronym}' without hyphens will be pronounced as a word. "
                        f"Use '{correct}' for letter-by-letter pronunciation."
                    )

    def _check_romanized_hindi(self):
        """Check for romanized Hindi in CAPS."""
        for word in ROMANIZED_HINDI:
            pattern = r'\b' + word + r'\b'
            if re.search(pattern, self.content, re.IGNORECASE):
                # Check if it's in CAPS (not just present)
                if re.search(r'\b' + word + r'\b', self.content):
                    self.errors.append(
                        f"PRONUNCIATION ERROR: '{word}' is romanized Hindi in CAPS. "
                        f"Use Devanagari script instead for natural pronunciation."
                    )

    def _check_numbers(self):
        """Check for Hindi numbers that should be English."""
        hindi_numbers = {
            "एक": "one", "दो": "two", "तीन": "three", "चार": "four",
            "पांच": "five", "छह": "six", "सात": "seven", "आठ": "eight",
            "नौ": "nine", "दस": "ten", "बीस": "twenty", "तीस": "thirty",
            "चालीस": "forty", "पचास": "fifty"
        }

        for hindi, english in hindi_numbers.items():
            if hindi in self.content:
                self.warnings.append(
                    f"WARNING: Hindi number '{hindi}' found. "
                    f"Consider using English '{english}' for consistency."
                )


def validate_script(script_path: str) -> Tuple[bool, List[str], List[str]]:
    """
    Validate an audio script file.

    This is called by CI to validate all scripts in a reel.
    """
    with open(script_path, "r") as f:
        content = f.read()

    validator = PronunciationValidator(content)
    return validator.validate()
