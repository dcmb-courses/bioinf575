# implement the Gene class
# implement the __init__ method 
# in __init__ we create custom attributes:  gid, symbol and description
# implement __str__ and __repr__ methods to be able to display the object 
# implement the __eq__ method to be able to chech equality between Gnee objects

class Gene:
    "Gene class description"
    def __init__(self,  gid, sym, desc): 
        # checks can be done to make sure the data is not missing and 
        # each parameter should ahve the correct type
        self.gid = gid
        self.symbol = sym
        self.description = desc
        
    def __str__(self):
        return f"Gene({self.gid},'{self.symbol}','{self.description}')"
    
    def __repr__(self):
        return f"Gene({self.gid},'{self.symbol}','{self.description}')"
    
    def __eq__(self, g):
        return self.gid == g.gid and self.symbol == g.symbol and self.description == g.description
    
# __________________________________________


# implement the GOTerm class
# implement the __init__ method 
# in __init__ we create custom attributes:  gid, symbol and description
# implement __str__ and __repr__ methods to be able to display the object 

class GOTerm:
    "GOTerm class description"
    def __init__(self,  gtid, name): 
        # checks can be done to make sure the data is not missing and 
        # each parameter should ahve the correct type
        self.gtid = gtid
        self.name = name
        
    def __str__(self):
        return f"GOTerm({self.gtid},'{self.name}')"
    
    def __repr__(self):
        return f"GOTerm({self.gtid},'{self.name}')"
        
# __________________________________________


# implement the GeneGOTerm class
# implement the __init__ method 
# in __init__ we create custom attributes:  gid, symbol and description
# implement __str__ and __repr__ methods to be able to display the object 

class GeneGOTerm:
    "GeneGOTerm class description"
    def __init__(self,  gid, gtid): 
        # checks can be done to make sure the data is not missing and 
        # each parameter should ahve the correct type
        self.gene_id = gid
        self.GO_term_id = gtid
        
    def __str__(self):
        return f"GeneGOTerm({self.gene_id},'{self.GO_term_id}')"
    
    def __repr__(self):
        return f"GeneGOTerm({self.gene_id},'{self.GO_term_id}')"
        

# __________________________________________

# the following code will run and test the classes 
# but only when the file is ran as a script

if __name__ == "__main__":
    print("We create a Gene, a GOTerm, and a GeneGOTerm:")
    print(Gene(42, "TestGene", "Gene to test the code"))
    print(GOTerm(84, "Gene Ontology Term associated with the test gene"))
    print(GeneGOTerm(42,84))