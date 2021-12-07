args = commandArgs(trailingOnly=TRUE)
df = read.table(args, header = T, row.names = 1, sep = "\t")
print(sum(df))