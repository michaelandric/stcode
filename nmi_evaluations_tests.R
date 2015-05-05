# looking at NMI value between conditions
setwd('/Users/andric/Documents/workspace/steadystate_data/')
library(dplyr)
nn <- read.csv('nmi_evaluations.csv')
nn <- tbl_df(stack(nn[, c(2:7)]))
colnames(nn) <- c('nmi', 'cond_pair')
attach(nn)
combinations <- combn(levels(cond_pair), 2)
for (i in 1:dim(combinations)[2])
{
    print(paste('TEST',i))
    print(combinations[, i])
    a <- filter(nn, cond_pair == combinations[, i][1])$nmi
    b <- filter(nn, cond_pair == combinations[, i][2])$nmi
    print(t.test(a, b, paired = TRUE))
}