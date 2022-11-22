SELECT * FROM genes;

SELECT * FROM gene_aliases;


SELECT genes.gene_id, gene_symbol, count(alias) 
FROM gene_aliases 
    INNER JOIN genes ON genes.gene_id = gene_aliases.gene_id
GROUP BY genes.gene_id, gene_symbol;
