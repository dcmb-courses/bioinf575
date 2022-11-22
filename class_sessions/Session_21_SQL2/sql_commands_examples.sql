-- Retrieve the gene information for gene alias "p40"
SELECT *
FROM genes 
WHERE gene_id IN (
		SELECT gene_id 
		FROM gene_aliases 
		WHERE alias = "p40");