# Revised density plot of SNSC
setwd('~/Documents/workspace/steadystate_data/')
snsc <- read.table('snsc_group_median.txt')$V1
iters <- read.table('iters_group_median5p_20vxFltr_warped_median.out')$V1
nonzero_snsc <- snsc[which(snsc > 0)]
nonzero_iters <- iters[which(iters > 0)]

stck <- c(nonzero_snsc, nonzero_iters)
snsc_frame <- data.frame(stck, c(rep("real", length(nonzero_snsc)), rep("null", length(nonzero_iters))))
colnames(snsc_frame) <- c("snsc", "set")

library(ggplot2)
cbbPalette <- c("#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")
pdf('snsc_composite_density_plot.pdf', paper = 'USr', width = 11)
qplot(snsc, data = snsc_frame, geom = "density", fill = set, position = "stack") + scale_fill_manual(values = c("black", "grey")) + theme(panel.background = element_rect(fill = "white", colour = "black"))
dev.off()
