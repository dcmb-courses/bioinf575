# Script created with the use of perplexity.ai. 
# Checked and updated for correctness and clarity.

# Object-Relational Mapping (ORM) is a programming technique that acts as a bridge between object-oriented programming languages and relational databases. It allows developers to interact with a database using the familiar constructs of their chosen programming language (e.g., objects, classes) instead of directly writing SQL queries. 

# This script builds a simple bioinformatics SQLite database named 'bioinfo.db' on disk using SQLAlchemy.
# It defines three tables: Gene, GoTerm, and GeneGoTerm (relationship table).
# Each key SQLAlchemy operation is explained with comments above code lines.
# After inserting records, updating, querying, and deleting, the script tests referential integrity—
# by attempting to insert a GeneGoTerm with a geneid not present in the Gene table (should fail due to foreign key constraints).
# Finally, it drops the relationship table.

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, inspect
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

# Define the base ORM model class for table definitions
Base = declarative_base()

# Define Gene table: stores gene information
class Gene(Base):
    __tablename__ = 'gene'
    geneid = Column(Integer, primary_key=True)
    symbol = Column(String)
    description = Column(String)
    go_terms = relationship("GoTerm", secondary="gene_go_term", back_populates="genes")

# Define GoTerm table: stores gene ontology term information
class GoTerm(Base):
    __tablename__ = 'goterm'
    gotermid = Column(Integer, primary_key=True)
    abbreviation = Column(String)
    description = Column(String)
    genes = relationship("Gene", secondary="gene_go_term", back_populates="go_terms")

# Define the join table: GeneGoTerm; creates many-to-many mapping between genes and terms
class GeneGoTerm(Base):
    __tablename__ = 'gene_go_term'
    geneid = Column(Integer, ForeignKey('gene.geneid', ondelete="CASCADE"), primary_key=True)
    gotermid = Column(Integer, ForeignKey('goterm.gotermid', ondelete="CASCADE"), primary_key=True)

# Create the SQLite database file bioinfo.db in current directory for persistent storage
engine = create_engine('sqlite:///bioinfo.db', echo=False, future=True)

# Ensure foreign key constraints are enforced on SQLite (required for integrity checks)
from sqlalchemy import event
from sqlite3 import Connection as SQLite3Connection
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

# Create all tables from defined models if not already existing
Base.metadata.create_all(engine)

# Create a session for managing database transactions
Session = sessionmaker(bind=engine)
session = Session()

# Create an Inspector to check the database structure.
# The Inspector object allows direct introspection of the database schema.
inspector = inspect(engine)
table_names = inspector.get_table_names()

print("Tables in the database:")
for table_name in table_names:
    print(f"- {table_name}")
print()

# Prepare and insert gene records into the Gene table
genes = [
    Gene(geneid=1, symbol='BRCA1', description='DNA repair'),
    Gene(geneid=2, symbol='TP53', description='Tumor suppressor'),
    Gene(geneid=3, symbol='EGFR', description='Growth factor receptor')
]
session.add_all(genes)
session.commit()

# Query: Print genes
print("All genes:")
for g in session.query(Gene).all():
    print(f"- {g.symbol}: {g.description}")
print()

# Prepare and insert go term records into GoTerm table
goterms = [
    GoTerm(gotermid=1, abbreviation='BP', description='Biological Process'),
    GoTerm(gotermid=2, abbreviation='MF', description='Molecular Function'),
    GoTerm(gotermid=3, abbreviation='CC', description='Cellular Component'),
    GoTerm(gotermid=4, abbreviation='TF', description='Transcription Factor'),
    GoTerm(gotermid=5, abbreviation='KR', description='Kinase Receptor')
]
session.add_all(goterms)
session.commit()

# Query: Print go terms
print("All go terms:")
for gt in session.query(GoTerm).all():
    print(f"- {gt.abbreviation}: {gt.description}")
print()

# Insert connections into the relationship table (GeneGoTerm)
session.add_all([
    GeneGoTerm(geneid=1, gotermid=1),
    GeneGoTerm(geneid=1, gotermid=2),
    GeneGoTerm(geneid=2, gotermid=2),
    GeneGoTerm(geneid=2, gotermid=3),
    GeneGoTerm(geneid=3, gotermid=1),
    GeneGoTerm(geneid=3, gotermid=5)
])
session.commit()

# Query: Print genes whose symbol starts with 'B'
print("Genes that start with 'B':")
for g in session.query(Gene).filter(Gene.symbol.like('B%')).all():
    print(f"- {g.symbol}: {g.description}")
print()

# Update: Change description of gene with symbol 'TP53'
print("Update TP53 description.")
gene = session.query(Gene).filter_by(symbol='TP53').first()
gene.description = 'Genome guardian'
session.commit()

print("Genes that start with 'T':")
# Query: Print genes whose symbol starts with 'T'
for g in session.query(Gene).filter(Gene.symbol.like('T%')).all():
    print(f"- {g.symbol}: {g.description}")
print()

# Delete: Remove the gene with symbol 'BRCA1' and cascade deletes in gene_go_term
gene_to_delete = session.query(Gene).filter_by(symbol='BRCA1').first()
session.delete(gene_to_delete)
session.commit()

# Try to insert a row into GeneGoTerm with an invalid geneid (e.g., geneid=99 does not exist)
# This should fail and rollback the transaction due to foreign key constraint
print("Try to insert a row into GeneGoTerm with an invalid geneid (99)")
try:
    session.add(GeneGoTerm(geneid=99, gotermid=1))
    session.commit()
    print("ERROR: Inserted invalid gene-go term pair; foreign key constraint not enforced!")
except IntegrityError as e:
    session.rollback()
    print("Foreign key constraint enforced (IntegrityError):", e)
print()

# Drop the relationship table from the schema
GeneGoTerm.__table__.drop(engine)

table_names = inspector.get_table_names()

print("Tables in the database:")
for table_name in table_names:
    print(f"- {table_name}")

# Close the session to release database resources
session.close()