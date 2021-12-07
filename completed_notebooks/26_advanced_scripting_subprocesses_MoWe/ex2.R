args = commandArgs(trailingOnly=TRUE)
df = read.table("test_R.txt", header = T, row.names = 1, sep = "\t")
print(sum(df))