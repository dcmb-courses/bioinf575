from demo_pkg import enhanced_gene_module as egm_p
import sys

def another_method(egene):
    egene.symbol = "updated gene symbol"
    egene.update_symbol("test BRCA1")
    egene.update_snps(["rs1","rs2","rs3"])

def main():
    print("this is another script")
    print(sys.argv)
    gene1 = egm_p.EnhancedGene()
    another_method(gene1)
    print(gene1)
    
    
if __name__ == "__main__":
    main()
