#!/usr/bin/env python
'''
Create tables and load data for the Pfam relational database. This includes
the following tables (this version includes pfamA_reg_full_significant):

pfamA - pfam_id indexed
pfamA_interactions - foreign keys defined and indexed
gene_ontology - foreign keys not defined but indexed
pfamA_literature_reference
literature_reference
pfamA_database_links
interpro
pfamA_reg_full_significant - pfamA_acc and pfamseq_acc indexed
architecture - architecture_acc, architecture, type_example indexed
pfamA_architecture - foreign keys defined and indexed
pfamA2pfamA_scoop - foreign keys defined and indexed

Practically speaking, defining the foreign keys has no effect unless
foreign key constraints are turned on at the beginning of a session.

latin1 is the unicode encoding that works with the Pfam text files.

!!! Created for and tested on Pfam release 30.0
ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam29.0/database_files/
'''

from sqlite3 import connect


#################### LOAD version #################################
def load_version (conn, curs, sourceFile = 'version.txt'):
    print('loading version')
    sql = 'DROP TABLE IF EXISTS version;'
    curs.execute(sql)
    
    sql = '''CREATE TABLE version (
    pfam_release TEXT,
    pfam_release_date TEXT DEFAULT NULL,
    swiss_prot_version TEXT,
    trembl_version TEXT,
    reference_proteome_version TEXT,
    hmmer_version TEXT,
    pfamA_coverage FLOAT DEFAULT NULL,
    pfamA_residue_coverage FLOAT DEFAULT NULL,
    number_families INTEGER DEFAULT NULL);'''
    curs.execute(sql)
    conn.commit()
    
    sql = 'INSERT INTO version VALUES (?,?,?,?,?,?,?,?,?);'
    infile = open(sourceFile, encoding='utf8')
    for line in infile:
        fields = line.rstrip('\n').split() #looks like they didn't use tabs
        curs.execute(sql, fields)
    conn.commit()
    infile.close()


######################### LOAD pfamA ###########################
def load_pfamA(conn, curs, sourceFile = 'pfamA.txt'):
    print('Loading pfamA table')
    # clear out old table
    sql = 'DROP TABLE IF EXISTS pfamA;'
    curs.execute(sql)
    # create pfamA table
    sql = '''CREATE TABLE pfamA (
        pfamA_acc TEXT PRIMARY KEY UNIQUE NOT NULL,
        pfamA_id TEXT NOT NULL,
        previous_id TEXT,
        description TEXT NOT NULL,
        author TEXT NOT NULL,
        deposited_by TEXT NOT NULL DEFAULT 'anon',
        seed_source TEXT NOT NULL,
        type TEXT NOT NULL,
        comment TEXT,
        sequence_GA REAL NOT NULL,
        domain_GC REAL NOT NULL,
        sequence_TC REAL NOT NULL,
        domain_TC REAL NOT NULL,
        sequence_NC REAL NOT NULL,
        domain_NC REAL NOT NULL,
        buildMethod TEXT NOT NULL,
        model_length INTEGER NOT NULL,
        searchMethod TEXT NOT NULL,
        msv_lambda REAL NOT NULL,
        msv _mu REAL NOT NULL,
        viterbi_lambda REAL NOT NULL,
        viterbi_mu REAL NOT NULL,
        forward_lambda REAL NOT NULL,
        forward_tau REAL NOT NULL,
        num_seed INTEGER DEFAULT NULL,
        num_full INTEGER DEFAULT NULL,
        updated TEXT NOT NULL,
        created TEXT DEFAULT NULL,
        version INTEGER DEFAULT NULL,
        number_archs INTEGER DEFAULT NULL,
        number_species INTEGER DEFAULT NULL,
        number_structures INTEGER DEFAULT NULL,
        number_ncbi INTEGER DEFAULT NULL,
        number_meta INTEGER DEFAULT NULL,
        average_length REAL DEFAULT NULL,
        percentage_id INTEGER DEFAULT NULL,
        average_coverage REAL DEFAULT NULL,
        change_status TEXT,
        seed_consensus TEXT,
        full_consensus TEXT,
        number_shuffled_hits INTEGER DEFAULT NULL,
        number_uniprot INTEGER DEFAULT NULL,
        rp_seed INTEGER DEFAULT NULL,
        number_rp15 INTEGER DEFAULT NULL,
        number_rp35 INTEGER DEFAULT NULL,
        number_rp55 INTEGER DEFAULT NULL,
        number_rp75 INTEGER DEFAULT NULL);'''
    curs.execute(sql)
    
    infile = open(sourceFile, encoding='utf8')
    # figure out how many fields are in pfamA.txt
    line = infile.readline()
    fields = line.rstrip('\n').split('\t')
    numFields = len(fields)
    infile.seek(0) #reset file to beginning
    
    # The next statement creates a list of question marks, joins them with commas
    # and inserts that into the sql template string. All of the question
    # marks are replaced with the corresponding values in a list passed to the
    # the execute statement.
    sql = '''insert into pfamA values ({});'''.format(','.join(['?'] * numFields))
    
    for line in infile:
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
    infile.close()
    
    # !!!!!!!!!! Don't forget to commit !!!!!!!!!!!!!!
    conn.commit()
    
    print('Indexing pfamA')
    sql = '''CREATE INDEX pfamA_id_idx
    ON pfamA(pfamA_id);'''
    curs.execute(sql)
    conn.commit()


######################### LOAD pfamA_interactions ###########################

def load_pfamA_interactions(conn, curs, sourceFile = 'pfamA_interactions.txt'):
    print('Loading pfamA_interactions')
    sql = 'DROP TABLE IF EXISTS pfamA_interactions;'
    curs.execute(sql)
    sql = '''CREATE TABLE pfamA_interactions (
    pfamA_acc_A TEXT NOT NULL,
    pfamA_acc_B TEXT NOT NULL,
    FOREIGN KEY(pfamA_acc_A) REFERENCES pfamA(pfamA_acc),
    FOREIGN KEY(pfamA_acc_B) REFERENCES pfamA(pfamA_acc));'''
    curs.execute(sql)
    infile = open(sourceFile, encoding='utf8')
    sql = '''INSERT INTO pfamA_interactions VALUES (?,?);
    '''
    for line in infile:
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
    infile.close()
    conn.commit()
    
    # Index the two identifier columns
    print('Indexing pfamA_interactions')
    sql = '''CREATE INDEX pfamA_acc_A_idx
    ON pfamA_interactions(pfamA_acc_A);'''
    curs.execute(sql)
    conn.commit()
    
    print('Indexing pfamA_interactions')
    sql = '''CREATE INDEX pfamA_acc_B_idx
    ON pfamA_interactions(pfamA_acc_B);
    '''
    curs.execute(sql)
    conn.commit()


######################### LOAD gene_ontology ###########################

def load_gene_ontology(conn, curs, sourceFile = 'gene_ontology.txt'):
    print('Loading gene_ontology')
    sql = '''DROP TABLE IF EXISTS gene_ontology;'''
    curs.execute(sql)
    sql = '''CREATE TABLE gene_ontology (
    pfamA_acc TEXT NOT NULL,
    go_id TEXT NOT NULL,
    term TEXT NOT NULL,
    category TEXT NOT NULL,
    FOREIGN KEY(pfamA_acc) REFERENCES pfamA(pfamA_acc));'''
    curs.execute(sql)
    
    sql = '''INSERT INTO gene_ontology VALUES (?,?,?,?);'''
    infile = open(sourceFile, encoding='utf8')
    for line in infile:
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
    infile.close()
    conn.commit()
    
    print('Indexing gene_ontology')
    sql = '''CREATE INDEX gene_ontology_pfamA_acc_idx
    ON gene_ontology(pfamA_acc);
    '''
    curs.execute(sql)
    conn.commit()
    
    sql = '''CREATE INDEX gene_ontology_go_id_idx
    ON gene_ontology(go_id);'''
    curs.execute(sql)
    conn.commit()


######################### LOAD pfamA_literature_reference ######################

def load_pfamA_literature_reference(conn, curs, sourceFile = 'pfamA_literature_reference.txt'):
    print('Loading pfamA_literature_reference')
    sql = 'DROP TABLE IF EXISTS pfamA_literature_reference;'
    curs.execute(sql)
    
    sql = '''CREATE TABLE pfamA_literature_reference (
    pfamA_acc TEXT NOT NULL,
    auto_lit INTEGER NOT NULL DEFAULT 0,
    comment TEXT,
    order_added INTEGER DEFAULT NULL,
    FOREIGN KEY(pfamA_acc) REFERENCES pfamA(pfamA_acc),
    FOREIGN KEY(auto_lit) REFERENCES literature_reference(auto_lit));'''
    curs.execute(sql)
    
    sql = 'INSERT INTO pfamA_literature_reference VALUES (?,?,?,?);'
    infile = open('pfamA_literature_reference.txt', encoding='utf8')
    for line in infile:
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
    infile.close()
    conn.commit()
    
    print('Indexing pfamA_literature_reference')
    sql = '''CREATE INDEX pfamA_lr_pfamA_acc_idx
    ON pfamA_literature_reference(pfamA_acc);'''
    curs.execute(sql)
    conn.commit()
    
    sql = '''CREATE INDEX pfamA_lr_auto_lit_idx
    ON pfamA_literature_reference(auto_lit);'''
    curs.execute(sql)
    conn.commit()
    


######################### LOAD literature_reference ###########################

def load_literature_reference(conn, curs, sourceFile = 'literature_reference.txt'):
    print('loading literature_reference')
    
    sql = 'DROP TABLE IF EXISTS literature_reference;'
    curs.execute(sql)
    
    sql = '''CREATE TABLE literature_reference (
    auto_lit INTEGER PRIMARY KEY UNIQUE NOT NULL,
    pmid INTEGER DEFAULT NULL,
    title TEXT,
    author TEXT,
    journal TEXT);'''
    curs.execute(sql)
    
    sql = 'INSERT INTO literature_reference VALUES (?,?,?,?,?);'
    infile = open(sourceFile, encoding='utf8')
    for line in infile:
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
    infile.close()
    conn.commit()


######################### LOAD pfamA_database_links ###########################
def load_pfamA_database_links(conn, curs, sourceFile = 'pfamA_database_links.txt'):
    
    print('Loading pfamA_database_links')
    
    sql = 'DROP TABLE IF EXISTS pfamA_database_links;'
    curs.execute(sql)
    
    sql = '''CREATE TABLE pfamA_database_links (
    pfamA_acc TEXT NOT NULL,
    db_id TEXT NOT NULL,
    comment TEXT,
    db_link TEXT NOT NULL,
    other_params TEXT,
    FOREIGN KEY(pfamA_acc) REFERENCES pfamA(pfamA_acc));'''
    curs.execute(sql)
    
    sql = 'INSERT INTO pfamA_database_links VALUES (?,?,?,?,?);'
    infile = open(sourceFile, encoding='utf8')
    for line in infile:
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
    infile.close()
    conn.commit()
    
    print('Indexing pfamA_database_links')
    sql = '''CREATE INDEX pfamA_dl_pfamA_acc_idx
    ON pfamA_database_links(pfamA_acc);'''
    curs.execute(sql)
    conn.commit()


######################### LOAD interpro ###########################

def load_interpro(conn, curs, sourceFile = 'interpro.txt'):
    
    print('Loading interpro')
    
    sql = 'DROP TABLE IF EXISTS interpro;'
    curs.execute(sql)
    
    sql = '''CREATE TABLE interpro (
      `pfamA_acc` TEXT NOT NULL,
      `interpro_id` TEXT NOT NULL,
      `abstract` TEXT NOT NULL,
      FOREIGN KEY(pfamA_acc) REFERENCES pfamA(pfamA_acc));'''
    curs.execute(sql)
    
    sql = 'INSERT INTO interpro VALUES (?,?,?);'
    infile = open(sourceFile, encoding='utf8')
    for line in infile:
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
    infile.close()
    conn.commit()
    
    print('Indexing interpro')
    sql = '''CREATE INDEX interpro_pfamA_acc_idx
    ON interpro(pfamA_acc);'''
    curs.execute(sql)
    conn.commit()


######################## LOAD pfamA_reg_full_significant ###########################

def load_pfamA_reg_full_significant(conn, curs, sourceFile = 'pfamA_reg_full_significant.txt'):
    print('Loading pfamA_reg_full_significant')
    sql = 'DROP TABLE IF EXISTS pfamA_reg_full_significant;'
    curs.execute(sql)
    sql = '''CREATE TABLE pfamA_reg_full_significant (
    auto_pfamA_reg_full INTEGER PRIMARY KEY UNIQUE NOT NULL,
    pfamA_acc TEXT NOT NULL,
    pfamseq_acc TEXT NOT NULL,
    seq_start INTEGER NOT NULL DEFAULT 0,
    seq_end INTEGER NOT NULL DEFAULT 0,
    ali_start INTEGER unsigned NOT NULL,
    ali_end INTEGER unsigned NOT NULL,
    model_start INTEGER NOT NULL DEFAULT 0,
    model_end INTEGER NOT NULL DEFAULT 0,
    domain_bits_score REAL NOT NULL DEFAULT 0.00,
    domain_evalue_score TEXT NOT NULL,
    sequence_bits_score REAL NOT NULL DEFAULT 0.00,
    sequence_evalue_score TEXT NOT NULL,
    cigar TEXT,
    in_full INTEGER NOT NULL DEFAULT 0,
    tree_order INTEGER DEFAULT NULL,
    domain_order INTEGER DEFAULT NULL,
    FOREIGN KEY(pfamA_acc) REFERENCES pfamA(pfamA_acc),
    FOREIGN KEY(pfamseq_acc) REFERENCES pfamseq(pfamseq_acc));'''
    curs.execute(sql)
    
    sql = '''INSERT INTO pfamA_reg_full_significant VALUES ({});'''.format(
        ','.join(['?'] * 17))
    infile = open(sourceFile, encoding='utf8')
    # Note: due to the large number of lines in this file, we will commit
    # after every 500,000 lines
    lineNum = 0
    for line in infile:
        lineNum += 1
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
        if lineNum % 500000 == 0:
            conn.commit()
            print('\tRows committed:', lineNum/1000000, 'million')
    infile.close()
    conn.commit()
    
    print('Indexing pfamA_reg_full_significant')
    sql = '''CREATE INDEX pfamA_rfs_pfamA_acc_idx
    ON pfamA_reg_full_significant(pfamA_acc);'''
    curs.execute(sql)
    conn.commit()
    
    sql = '''CREATE INDEX pfamA_rfs_pfamseq_acc_idx
    ON pfamA_reg_full_significant(pfamseq_acc);'''
    curs.execute(sql)
    conn.commit()


#################### End LOAD pfamA_reg_full_significant ################

#################### LOAD architecture #################################

def load_architecture(conn, curs, sourceFile = 'architecture.txt'):
    print('loading architecture')
    
    sql = 'DROP TABLE IF EXISTS architecture;'
    curs.execute(sql)
    
    sql = '''CREATE TABLE architecture (
    auto_architecture INTEGER PRIMARY KEY UNIQUE NOT NULL,
    architecture TEXT,
    type_example TEXT NOT NULL DEFAULT '0',
    no_seqs INTEGER NOT NULL DEFAULT 0,
    architecture_acc TEXT);'''
    curs.execute(sql)
    
    sql = 'INSERT INTO architecture VALUES (?,?,?,?,?);'
    infile = open(sourceFile, encoding='utf8')
    for line in infile:
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
    conn.commit()
    infile.close()
    
    print('Indexing architecture')
    sql = '''CREATE INDEX architecture_acc_idx
    ON architecture(architecture_acc);'''
    curs.execute(sql)
    conn.commit()
    
    sql = '''CREATE INDEX architecture_idx
    ON architecture(architecture);'''
    curs.execute(sql)
    conn.commit()
    
    sql = '''CREATE INDEX type_example_idx
    ON architecture(type_example);'''
    curs.execute(sql)
    conn.commit()


#################### LOAD pfamA_architecture #################################

def load_pfamA_architecture(conn, curs, sourceFile = 'pfamA_architecture.txt'):
    print('loading pfamA_architecture')
    sql = 'DROP TABLE IF EXISTS pfamA_architecture;'
    curs.execute(sql)
    
    sql = '''
    CREATE TABLE pfamA_architecture (
    pfamA_acc TEXT NOT NULL,
    auto_architecture INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(auto_architecture) REFERENCES architecture(auto_architecture),
    FOREIGN KEY(pfamA_acc) REFERENCES pfamA(pfamA_acc) );'''
    curs.execute(sql)
    conn.commit()
    
    sql = 'INSERT INTO pfamA_architecture VALUES (?,?);'
    infile = open(sourceFile, encoding='utf8')
    for line in infile:
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
    conn.commit()
    infile.close()
    
    print('Indexing pfamA_architecture')
    sql = '''CREATE INDEX pfamA_architecture_pfamA_acc_idx
    ON pfamA_architecture(pfamA_acc);'''
    curs.execute(sql)
    conn.commit()
    
    sql = '''CREATE INDEX pfamA_architecture_auto_architecture_idx
    ON pfamA_architecture(auto_architecture);'''
    curs.execute(sql)
    conn.commit()


#################### LOAD pfamA2pfamA_scoop #################################

def load_pfamA2pfamA_scoop(conn, curs, sourceFile = 'pfamA2pfamA_scoop.txt'):
    print('loading pfamA2pfamA_scoop')
    
    sql = 'DROP TABLE IF EXISTS pfamA2pfamA_scoop;'
    curs.execute(sql)
    sql = '''
    CREATE TABLE pfamA2pfamA_scoop (
    pfamA_acc_1 TEXT NOT NULL,
    pfamA_acc_2 TEXT NOT NULL,
    score FLOAT NOT NULL DEFAULT 0,
    FOREIGN KEY(pfamA_acc_1) REFERENCES pfamA(pfamA_acc),
    FOREIGN KEY(pfamA_acc_2) REFERENCES pfamA(pfamA_acc));'''
    curs.execute(sql)
    conn.commit()
    
    sql = 'INSERT INTO pfamA2pfamA_scoop VALUES (?,?,?);'
    infile = open('pfamA2pfamA_scoop.txt', encoding='utf8')
    for line in infile:
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
    conn.commit()
    infile.close()
    
    print('Indexing pfamA2pfamA_scoop')
    
    # Warning: index names must be unique in a database. The pfamA2pfamA_scoop
    # and pfamA2pfamA_hhsearch tables have identical field names that are being
    # indexed as foreign key, so the names are preceded by the table names
    sql = '''CREATE INDEX pfamA2pfamA_scoop_pfamA_acc_1_idx
    ON pfamA2pfamA_scoop(pfamA_acc_1);'''
    curs.execute(sql)
    conn.commit()
    
    sql = '''CREATE INDEX pfamA2pfamA_scoop_pfamA_acc_2_idx
    ON pfamA2pfamA_scoop(pfamA_acc_2);'''
    curs.execute(sql)
    conn.commit()




def load_pfamA2pfamA_hhsearch(conn, curs, sourceFile = 'pfamA2pfamA_hhsearch.txt'):
    print('loading pfamA2pfamA_hhsearch')
    
    sql = 'DROP TABLE IF EXISTS pfamA2pfamA_hhsearch;'
    curs.execute(sql)
    sql = '''
    CREATE TABLE pfamA2pfamA_hhsearch (
    pfamA_acc_1 TEXT NOT NULL,
    pfamA_acc_2 TEXT NOT NULL,
    evalue FLOAT NOT NULL DEFAULT 0,
    FOREIGN KEY(pfamA_acc_1) REFERENCES pfamA(pfamA_acc),
    FOREIGN KEY(pfamA_acc_2) REFERENCES pfamA(pfamA_acc));'''
    curs.execute(sql)
    conn.commit()
    
    sql = 'INSERT INTO pfamA2pfamA_hhsearch VALUES (?,?,?);'
    infile = open(sourceFile, encoding='utf8')
    for line in infile:
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
    conn.commit()
    infile.close()
    
    print('Indexing pfamA2pfamA_hhsearch')
    
    # Warning index names must be unique for the database
    sql = '''CREATE INDEX pfamA2pfamA_hhsearch_pfamA_acc_1_idx
    ON pfamA2pfamA_hhsearch(pfamA_acc_1);'''
    curs.execute(sql)
    conn.commit()
    
    sql = '''CREATE INDEX pfamA2pfamA_hhsearch_pfamA_acc_2_idx
    ON pfamA2pfamA_hhsearch(pfamA_acc_2);'''
    curs.execute(sql)
    conn.commit()


def load_pfamseq(conn, curs, sourceFile = 'pfamseq.txt'):
    pass
    print('loading pfamseq')
    sql = 'DROP TABLE IF EXISTS pfamseq;'
    curs.execute(sql)
    
    sql = '''CREATE TABLE pfamseq (
    pfamseq_acc TEXT PRIMARY KEY UNIQUE NOT NULL,
    pfamseq_id TEXT NOT NULL,
    seq_version INTEGER NOT NULL,
    crc64 TEXT NOT NULL,
    md5 TEXT NOT NULL,
    description TEXT NOT NULL,
    evidence INTEGER NOT NULL,
    length INTEGER NOT NULL DEFAULT 0,
    species TEXT NOT NULL,
    taxonomy TEXT,
    is_fragment INTEGER DEFAULT NULL,
    sequence TEXT NOT NULL,
    updated TEXT,
    created TEXT DEFAULT NULL,
    ncbi_taxid INTEGER NOT NULL DEFAULT 0,
    auto_architecture INTEGER DEFAULT NULL,
    treefam_acc TEXT DEFAULT NULL,
    swissprot INTEGER DEFAULT 0)'''
    curs.execute(sql)
    conn.commit()
    
    sql = '''INSERT INTO pfamseq VALUES ({});'''.format(','.join(['?'] * 18))
    infile = open(sourceFile, encoding='utf8')
    # Note: due to the large number of lines in this file, we will commit
    # after every 500,000 lines
    lineNum = 0
    for line in infile:
        lineNum += 1
        fields = line.rstrip('\n').split('\t')
        curs.execute(sql, fields)
        if lineNum % 500000 == 0:
            conn.commit()
            print('\tRows committed:', lineNum/1000000, 'million')
    infile.close()
    conn.commit()
    
    print('Indexing pfamseq')
    
    sql = '''CREATE INDEX pfamseq_id_idx
    ON pfamseq(pfamseq_id);'''
    curs.execute(sql)
    conn.commit()
    
    sql = '''CREATE INDEX pfamseq_auto_architecture_idx
    ON pfamseq(auto_architecture);'''
    curs.execute(sql)
    conn.commit()
    
    #example of a compound index
    sql = '''CREATE INDEX pfamseq_acc_version_idx
    ON pfamseq(pfamseq_acc, seq_version);'''
    curs.execute(sql)
    conn.commit()
    
    sql = '''CREATE INDEX pfamseq_ncbi_taxid_idx
    ON pfamseq(ncbi_taxid);'''
    curs.execute(sql)
    conn.commit()
    



##############################################################################
########################## MAIN PROGRAM #####################################
print('Building pfam.sqlite')
conn = connect('pfam.sqlite')
curs = conn.cursor()

load_version(conn, curs, sourceFile = 'version.txt')
load_pfamA(conn, curs, sourceFile = 'pfamA.txt')
load_pfamA_interactions(conn, curs, sourceFile = 'pfamA_interactions.txt')
load_gene_ontology(conn, curs, sourceFile = 'gene_ontology.txt')
load_pfamA_literature_reference(conn, curs,
                            sourceFile = 'pfamA_literature_reference.txt')
load_literature_reference(conn, curs, sourceFile = 'literature_reference.txt')
load_pfamA_database_links(conn, curs, sourceFile = 'pfamA_database_links.txt')
load_interpro(conn, curs, sourceFile = 'interpro.txt')
load_pfamA_reg_full_significant(conn, curs,
                            sourceFile = 'pfamA_reg_full_significant.txt')
load_architecture(conn, curs, sourceFile = 'architecture.txt')
load_pfamA_architecture(conn, curs, sourceFile = 'pfamA_architecture.txt')
load_pfamA2pfamA_scoop(conn, curs, sourceFile = 'pfamA2pfamA_scoop.txt')
load_pfamA2pfamA_hhsearch(conn, curs, sourceFile = 'pfamA2pfamA_hhsearch.txt')
load_pfamseq(conn, curs, sourceFile = 'pfamseq.txt')

curs.close()
conn.close()
print('Finished building pfam.sqlite')
