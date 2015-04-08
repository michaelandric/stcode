## This accompanies 40.pwr_funcs.R and from 41.pwr_funcs_stats.R
## It uses 'fitting*.txt' outputs from 40.pwr_funcs.R to do bar graphs that accompany group stats
library(gplots)   # this library only on servers 30 and 32
library(RColorBrewer)

subjects <- c("ANGO","CLFR","MYTP","TRCO","PIGL","SNNW","LDMW","FLTM","EEPA","DNLN","CRFO","ANMS","MRZM","MRVV","MRMK","MRMC","MRAG","MNGO","LRVN")
conditions <- seq(4)
condition_names <- c("Highly ordered", "Some order", "Random", "Almost Random")

dat_matA = matrix(nrow=length(subjects),ncol=4)
dat_matB = matrix(nrow=length(subjects),ncol=4)
dat_matG = matrix(nrow=length(subjects),ncol=4)

setwd(paste("/mnt/tier2/urihas/Andric/steadystate/links_files5p/",sep=""))
for (ss in 1:length(subjects))
{
    for (i in conditions)
    {
        #setwd(paste("/mnt/tier2/urihas/Andric/steadystate/",subjects[ss],"/corrTRIM_BLUR/",sep=""))
        dat_matA[ss,i] = as.numeric(strsplit(levels(read.delim(paste("fitting_cond",i,"_",subjects[ss],"_5p.txt",sep=""))[1,])[4]," ")[[1]][4]) ## this is for alpha — shape
        dat_matB[ss,i] = as.numeric(strsplit(levels(read.delim(paste("fitting_cond",i,"_",subjects[ss],"_5p.txt",sep=""))[1,])[5]," ")[[1]][4]) ## this is for beta — scale ("exponent cutoff")
        dat_matG[ss,i] = as.numeric(strsplit(levels(read.delim(paste("fitting_cond",i,"_",subjects[ss],"_5p.txt",sep=""))[1,])[6]," ")[[1]][4]) ## this is for gamma — power law values
    }
}

setwd("/mnt/tier2/urihas/Andric/steadystate/groupstats")

error_vecG <- c()
error_vecB <- c()
error_vecA <- c()
for (i in conditions)
{
    erG <- sd((dat_matG[,i] - rowMeans(dat_matG)) / sqrt(length(subjects)))
    error_vecG <- c(error_vecG, erG)   # These end up same order as condition_names ("Highly ordered, Some order, Random, Almost Random")
    erB <- sd((dat_matB[,i] - rowMeans(dat_matB)) / sqrt(length(subjects)))
    error_vecB <- c(error_vecB, erB)   # These end up same order as condition_names ("Highly ordered, Some order, Random, Almost Random")
    erA <- sd((dat_matA[,i] - rowMeans(dat_matA)) / sqrt(length(subjects)))
    error_vecA <- c(error_vecA, erA)   # These end up same order as condition_names ("Highly ordered, Some order, Random, Almost Random")

}

colnames(dat_matG) <- condition_names
colnames(dat_matB) <- condition_names
colnames(dat_matA) <- condition_names

aG <- apply(dat_matG, 2, mean)
aB <- apply(dat_matB, 2, mean)
aA <- apply(dat_matA, 2, mean)
aG_ordered <- aG[c(1, 2, 4, 3)]
aB_ordered <- aB[c(1, 2, 4, 3)]
aA_ordered <- aA[c(1, 2, 4, 3)]
error_vecG_ordered <- error_vecG[c(1, 2, 4, 3)]
error_vecB_ordered <- error_vecB[c(1, 2, 4, 3)]
error_vecA_ordered <- error_vecA[c(1, 2, 4, 3)]

#thepal = colorRampPalette(brewer.pal(9,"Blues"))(9)[c(7, 5, 3, 1)]
thepal = colorRampPalette(brewer.pal(9,"Set2"))(9)

#pdf("Degrees_PowerLaw_bargraph.pdf")
pdf("Degrees_PowerLaw_bargraph_5p.pdf")
ylimG <- c(1.15, 1.01 * max(aG + error_vecG))
plotaG <- barplot2(aG_ordered, beside = TRUE, ylim = ylimG, ylab = "Power law values", col = thepal, plot.grid = TRUE, xpd=F)
segments(x0 = plotaG, x1 = plotaG, y0 = aG_ordered, y1 = aG_ordered + error_vecG_ordered)
segments(x0 = plotaG - .2, x1 = plotaG + .2, y0 = aG_ordered + error_vecG_ordered, y1 = aG_ordered + error_vecG_ordered)
dev.off()

#pdf("Degrees_ExpCutoff_bargraph.pdf")
pdf("Degrees_ExpCutoff_bargraph_5p.pdf")
ylimB <- c(0, 1.15 * max(aB + error_vecB))
plotaB <- barplot2(aB_ordered, beside = TRUE, ylim = ylimB, ylab = "Exponent cutoff values", col = thepal, plot.grid = TRUE)
segments(x0 = plotaB, x1 = plotaB, y0 = aB_ordered, y1 = aB_ordered + error_vecB_ordered)
segments(x0 = plotaB - .2, x1 = plotaB + .2, y0 = aB_ordered + error_vecB_ordered, y1 = aB_ordered + error_vecB_ordered)
dev.off()

#pdf("Degrees_ExpCutoff_bargraph.pdf")
pdf("Degrees_TruncPShape_bargraph_5p.pdf")
ylimA <- c(0, 1.15 * max(aA + error_vecA))
plotaA <- barplot2(aA_ordered, beside = TRUE, ylim = ylimA, ylab = "Trunc Power Shape values", col = thepal, plot.grid = TRUE)
segments(x0 = plotaA, x1 = plotaA, y0 = aA_ordered, y1 = aA_ordered + error_vecA_ordered)
segments(x0 = plotaA - .2, x1 = plotaA + .2, y0 = aA_ordered + error_vecA_ordered, y1 = aA_ordered + error_vecA_ordered)
dev.off()
