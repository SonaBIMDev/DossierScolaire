import sys
import argparse
import fitz  # PyMuPDF
from pathlib import Path
from balises_pdf import balises
from données_ods import mapping

def correspond_balises_with_variables(balises, variables):
    if not balises or not variables:
        print("Aucune balise ou variable à traiter.")
        return {}
    
    correspond = {}
    for balise in balises:
        for variable in variables:
            if balise == variable:
                correspond[balise] = variables[variable]
    return correspond

correspond = correspond_balises_with_variables(balises, mapping)
print(f"variables coresspondantes : {correspond}")