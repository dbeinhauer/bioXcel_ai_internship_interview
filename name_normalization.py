#!/usr/bin/env python3

import json
import pandas as pd


# Name Normalization:

# In order to normalize the compound names we have decided to use the dictionary 
# of the `normed_form : [variants]` key:value pairs stored in the separed JSON file.
# Alternatively, it might be possible to use dictionary of the `variant : normed_form`
# pairs or even other aproach based on the more specific task description.


def normalize_name(compound_name : str, normed_forms) -> str:
    """Normalize compound name.

    This function normalizes the compound name based on the
    given template.

    Args:
        compound_name (str): Name to be normalized.
        normed_forms : Template for name normalization.

    Returns:
        str: The normalized compound name.
    """

    # In order to normalize compound name, we just run through all possible 
    # variants and find the maching normalized form.

    for normed, variations in normed_forms.items():
        if compound_name in variations:
            return normed

    # Normalized variant not found.
    return compound_name
            

def normalize_input(variants_input : list, mapping_filename="variants_mapping.json") -> pd.DataFrame:
    """Normalize all given compound names.

    Args:
        variants_input (list): Names to be normalized
        mapping_filename (str, optional): Name of the file containg template for name 
        normalization. Defaults to "variants_mapping.json".

    Returns:
        pd.Dataframe: Normalized compound names from the `variants_input`.
    """

    # Load template for normalization.
    with open(mapping_filename, 'r') as variants_file:
        variants_mapping = json.load(variants_file)

    return pd.DataFrame(
        {
            'org_form': variants_input, 
            'normed_form': [normalize_name(name, variants_mapping) for name in variants_input]
        }
    )   


# Bonus Part - Enriching Data and Ranking

# In order to solve the bonus part, we have prepared the simplified version of the
# excel file for the demonstration of the solution. The file only contains normed name 
# and molecular weight of the compounds. Note that because of the simplification 
# the file does not contain all of the specified feature variants (contains only
# numerical features). The missing parameter types would have the biggest impact on the
# ranking, where it might be neccesary to properly design the score function based on the
# parameter types. In our example, we just ranked the compounds based on their
# molecular weights.


def load_compound_data(compound_data_filename="compound_data.xlsx") -> pd.DataFrame:
    """Load additional compound properties."""

    # If working with the more complex dataset it would be probably necessary
    # to preprocess the data more profoundly.

    return pd.read_excel(compound_data_filename)


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

    return compound_data["molecular_weight"]


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
        additional_info = compound_data[['normed_form', 'score']]
        additional_info.to_excel(enriched_filename, index=False)



# Call the functions.
if __name__ == "__main__":
    # Input specified in the task assignment.
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


    # Name Normalization: 
    # Normalize and print the compound names. 
    print("Name normalization:")
    print("-----------------------------")
    print(normalize_input(variants_input))
    print()


    # Bonus Part - Enriching Data and Ranking
    # Assuming you have a data file 'compound_data.xlsx' containing additional properties.
    # Load the additional data, rank them and print the ranked data.
    compound_data = load_compound_data("compound_data.xlsx")
    rank_data(compound_data)

    print("Bonus Part - Enriching Data and Ranking")
    print("-----------------------------")
    print(compound_data)