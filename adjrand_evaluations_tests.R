# looking at NMI value between conditions
setwd('/Users/andric/Documents/workspace/steadystate_data/')
library(dplyr)
ajr <- read.csv('adjrand_evaluations.csv')
ajr <- tbl_df(stack(ajr[, c(2:7)]))
colnames(ajr) <- c('ari', 'cond_pair')
attach(ajr)
combinations <- combn(levels(cond_pair), 2)
for (i in 1:dim(combinations)[2])
{
    print(paste('TEST',i))
    print(combinations[, i])
    a <- filter(ajr, cond_pair == combinations[, i][1])$ari
    b <- filter(ajr, cond_pair == combinations[, i][2])$ari
    #print(t.test(a, b, paired = TRUE)$statistic)
    print(t.test(a, b, paired = TRUE)$p.value)
}