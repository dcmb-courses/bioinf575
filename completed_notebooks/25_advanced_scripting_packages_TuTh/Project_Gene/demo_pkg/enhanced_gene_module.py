from demo_pkg import gene_module as g

"""
    EnhancedGene - A class for demonstration purposes.
    The class extends the class Gene with the methods:
    - update_symbol - updates symbol
    - update_snps - updates the snp number given a list of new SNPs
    
"""
class EnhancedGene(g.Gene):
    
    def update_symbol(self, new_symbol = ""):
        """
        Change symbol to new_symbol

        Keyword arguments:
        str: new_symbol - the string to replace the gene symbol, should contain test ("")
        
        Returns:
        str: updated gene symbol
        """        
        old_value = self.symbol
        try:
            self.symbol = new_symbol
            index = self.symbol.index("test")
        except TypeError: 
            self.symbol = self.symbol + " " + str(new_symbol)
            print(f"'{new_symbol}' is not a string, we made the conversion and added it")
        except ValueError: 
            self.symbol = self.symbol + " test"
            print(f"'{self.symbol}' does not contain 'test', we added 'test' to it")

        finally:
            print(f"Old value was '{old_value}', new value is '{self.symbol}'")
        return self.symbol
    

    def update_snps(self, snp_list = []):
        """
        Add parameter snp_list length to snp_no.
        """
        old_snp_no = self.snp_no
        try:
            self.snp_no += len(snp_list)
        except TypeError:
            print("We did not change the SNP no, no collection of SNPs was provided!")
        else:
            print("SNP no updated!")        
        finally:
            print(f"Old value for the SNP no was {old_snp_no}, new value is {self.snp_no}.")
        return self.snp_no