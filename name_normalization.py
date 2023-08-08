#!/usr/bin/env python3

import pandas as pd
import pubchempy as pcp

# Solution description (including the Bonus part):
# We have decided to normalize compound names and enrich them with additional properties
# using PubChem databasis. As the normalized form we have decided to choose uppercase 
# variant of the first synonym of the first match of the original form name from the databasis.
# As the additional properties, we have decided to take only molecular weight, smiles and logP.
# Note that the code design allows to expand the list of properties with ease.
# We have decided to rank the compounds only by the molecular weight. We expect that in the real
# life example there would be more complex scoring function based on the number of compound 
# properties. In our example, we have not include any categorical properties, but the desing
# does not limit its usage in the future.

class CompoundProcessor:

    # Table header content strings:
    ORG_FORM_NAME = 'org_form'
    NORMED_FORM_NAME = 'normed_form'
    MOLECULAR_WEIGHT_NAME = 'molecular_weight'
    SMILES_NAME = 'smiles'
    LOGP_NAME = 'logP'

        
    def process_input(self, variants_input : list) -> tuple:
        """Normalize compound names and add additional properties.

        This function normalizes compound names and extracts additional properties 
        from PubChem database.
        
        Args:
            variants_input (list): List of compound names to be processed.

        Returns:
            tuple: A tuple containing two pd.DataFrames:
                   - DataFrame with mapping of original compound names to normalized forms.
                   - DataFrame with normalized compounds and their properties.
        """

        # In order to reduce the number of requests to PubChem databasis we normalize and
        # add properties at once.

        processed_data = []
        org_norm_mapping = {}

        # For fast checking whether the properties of the normalized compound are already added. 
        normed_formes_set = set()

        for name in variants_input:
            pubchem_compounds = pcp.get_compounds(name, 'name')

            if pubchem_compounds:
                # Compound found -> take the first matching variant.
                compound = pubchem_compounds[0]

                # Normalized form it the first synonym in uppercase.
                normed_form_name = compound.synonyms[0].upper()
                org_norm_mapping[name] = normed_form_name

                # Compound already processed -> skip properties addition.
                if normed_form_name in normed_formes_set:
                    continue

                normed_formes_set.add(normed_form_name)

                # Add properties of the compound.
                processed_data.append({
                    CompoundProcessor.NORMED_FORM_NAME : normed_form_name,
                    CompoundProcessor.MOLECULAR_WEIGHT_NAME : compound.molecular_weight,
                    CompoundProcessor.SMILES_NAME : compound.isomeric_smiles,
                    CompoundProcessor.LOGP_NAME : compound.xlogp,
                })
            else:
                # Compound not found:
                # In our case we just print the message to stdout. In real life example, 
                # we should use better way to inform the user about job failure.
                print("Compound not found!")


        org_norm_mapping = pd.DataFrame(
            list(org_norm_mapping.items()), 
            columns=[
                CompoundProcessor.ORG_FORM_NAME,  
                CompoundProcessor.NORMED_FORM_NAME
                ]
            )
        
        compound_properties = pd.DataFrame(processed_data).astype(
            {
                CompoundProcessor.NORMED_FORM_NAME : 'str',
                CompoundProcessor.MOLECULAR_WEIGHT_NAME: 'float',
                CompoundProcessor.SMILES_NAME : 'str',
                CompoundProcessor.LOGP_NAME : 'float',
            }
        )

        return org_norm_mapping, compound_properties
    
    
def save_processed_input(processed_data, filename='compound_data.xlsx'):
    """Save processed data into the excel file."""
    processed_data.to_excel(filename, index=False)


def compound_score(compound_data : pd.DataFrame) -> float:
    """Compute score of the compound.

    This function computes the score of the compound necessary for the ranking.
    The score is equal to molecular weight of the compound.

    Args:
        compound_data (pd.DataFrame): Properties of the compound.

    Returns:
        float: Score of the compound.
    """

    # In our example we rank the data based on the molecular weight. In real life
    # example we would probably use more complex scoring function combining the 
    # properties (and probably dealing with different types of the features).

    return compound_data[CompoundProcessor.MOLECULAR_WEIGHT_NAME]


def rank_data(compound_data : pd.DataFrame, enriched_filename="enriched_compound_data.xlsx"):
    """Rank data.

    This function ranks data based on the computed score computed by the 
    function `compound_score`.

    Args:
        compound_data (pd.DataFrame): Properties of the compounds to rank. 
        Will be modified using the function.
        enriched_filename (str, optional): Name of the file to store the additional 
        information necessary to rank the data. If `None`, then data will not be stored. 
        Defaults to "enriched_compound_data.xlsx".
    """

    compound_data['score'] = compound_data.apply(compound_score, axis=1)
    compound_data.sort_values(by=['score'], inplace=True, ignore_index=True,)

    # If we want to maintain the `score` property -> store it to the specified file. 
    if enriched_filename:
        additional_info = compound_data[[CompoundProcessor.NORMED_FORM_NAME, 'score']]
        additional_info.to_excel(enriched_filename, index=False)


# Example usage
if __name__ == "__main__":
    variants_input = [
        "Adenosine",
        "Adenocard",
        "BG8967",
        "Bivalirudin",
        "BAYT006267",
        "diflucan",
        "ibrutinib",
        "PC-32765",
    ]
    
    # Name normalization and properties addition.
    processor = CompoundProcessor()
    mapping, processed_data = processor.process_input(variants_input)
    print("Name normalization:")
    print("-----------------------------")
    print(mapping)
    print()

    # Save additional properties into the excel file.
    save_processed_input(processed_data)
    # Rank the data.
    rank_data(processed_data)#, enriched_filename=None)

    print("Bonus Part - Enriching Data and Ranking")
    print("-----------------------------")
    print(processed_data)