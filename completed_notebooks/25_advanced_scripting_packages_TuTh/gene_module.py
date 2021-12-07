"""
    Gene - A class for demonstration purposes.
    The class has 2 attributes:
    - symbol - text (str) - the gene symbol
    - snp_no - numeric (int) - the number of SNPs known for the gene
    
    The class allows for the update of the numeric attribute.
    - update_snp_no updates snp_no by a given additional number of SNPs
"""
class Gene:
    def __init__(self, gene_symbol = "Gene Symbol", snp_number = 0):
        self.symbol = gene_symbol
        self.snp_no = snp_number
        
    def __str__(self):
        return f"Gene object: Gene symbol = '{self.symbol}', Number of SNPs = {self.snp_no}"
        
    def __repr__(self):
        return f"Gene('{self.symbol}',{self.snp_no})"
    
    def update_snp_no(self, additional_snps = 0):
        """
        Add parameter value to snp_no.

        Keyword arguments:
        int: additional_snps - the number to add (0)
        
        Returns:
        int: updated snp_no
        """         
        old_value = self.snp_no
        try:
            self.snp_no = self.snp_no + additional_snps
        except TypeError: 
            self.snp_no = self.snp_no + 1
            print(f"'{additional_snps}' is not a numeric value, we added 1 because at least one new SNP was found.")
        finally:
            print(f"Old value was {old_value}, new value is {self.snp_no}")
        return self.snp_no