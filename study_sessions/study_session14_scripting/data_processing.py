# to be able to use the classes from the gene_annotations file 
# we need to import it

import gene_annotations as ga
import pandas as pd

# __________________________________________

def process_line(line, go_terms_names):
    """
    Process a line and return a dictionary with a gene and associated goterms
    Arguments:
        line (str): the line to parse, should have gene id symbol and description at the beginning, and at the end go terms separated by semicolon
        go_terms_names (list of str): the go terms that have been processed so far
    Returns:
        dict: dictionary with three items a gene, a list of goterms, a list of genegoterms
    """
    go_terms = []
    gene_go_terms = []
    gene = None
    
    line_lst = line.strip().split("\t")
    if len(line_lst) >= 4:
        gene_id = int(line_lst[0])
        gene = ga.Gene(gene_id, line_lst[1], line_lst[0])
        gene_gts_lst = line_lst[-1].split(";")
        for gt in gene_gts_lst:
            gts = gt.strip()
            if gts not in go_terms_names:
                go_terms_names.append(gts)
                gt_id = len(go_terms_names)
                go_terms.append(ga.GOTerm(gt_id, gts))
            else:
                gt_id = go_terms_names.index(gt) 
            gene_go_terms.append(ga.GeneGOTerm(gene_id, gt_id))
    
    return {"Gene":gene, 
            "GOTerms": go_terms, 
            "GeneGOTerms": gene_go_terms}
    
# __________________________________________


def process_file(file_name):
    """
    Process a file and return a dictionary with genes and associated goterms
    Arguments:
        file_name (str): the file to parse (has a header line), each data line should have gene id symbol and description at the beginning, and at the end go terms separated by semicolon
    Returns:
        dict: dictionary with three items a list of genes, a list of goterms, a list of genegoterms
    """
    
    genes = []
    go_terms = []
    gene_go_terms = []
    
    with open(file_name) as data_file:
        processed_gts  = []
        header_line = data_file.readline()
        for line in data_file:
            res_dict = process_line(line, processed_gts)
            genes.append(res_dict["Gene"])
            go_terms.extend(res_dict["GOTerms"])
            gene_go_terms.extend(res_dict["GeneGOTerms"])

    return {"Genes": genes, "GOTerms": go_terms, "GeneGOTerms": gene_go_terms}

# __________________________________________

def list_to_dataframe(lst):
    """
    Create a dataframe from a list of objects with the columns being the object attribute
    Arguments:
        lst (list of objects): tthe list of objects
    Returns:
        andas.core.frame.DataFrame: datafreame with the the columns being the object attribute and the values of the attributes are values on the rows
    Requires pandas
    """
    return pd.DataFrame([vars(obj) for obj in lst])

# __________________________________________



# the following code will run and test the classes 
# but only when the file is ran as a script

if __name__ == "__main__":
    
    print("Testing line processing:")
    
    line = "672	BRCA1	BRCA1 DNA repair associated	17q21.31	17	NC_000017.11	43044295	43125364	minus	24	intrinsic apoptotic signaling pathway in response to DNA damage;transcription cis-regulatory region binding;transcription coactivator activity;ubiquitin-protein transferase activity"
    
    print("We are processing the line!")
    print(line)
    print("The result is:")
    print(process_line(line, []))
    print()
    
    print("We are processing the file!")
    filename = "genes_info2.txt"
    print(filename)
    print("The result is:")
    pf_res = process_file(filename)
    print(pf_res)
    print()
    
    print("We are making the genes list a dataframe!")
    print("The result is:")
    print(list_to_dataframe(pf_res["Genes"]))