from datetime import datetime
from balises_pdf import balises
from données_ods import mapping

def search_usable_variables(date):
    balises_variables = {}

    for var in balises:
        var_without_spaces = var.replace(" ","")
        for keys in mapping.keys():

            if var_without_spaces == "[900]":
                balises_variables[var] = date

            else:
                if keys == var_without_spaces:
                    balises_variables[var] = mapping[keys]
    
    print ("balises_variables :", balises_variables)
    return balises_variables

date = datetime.now().strftime("%d-%m-%Y")
balises_variables = search_usable_variables(date)