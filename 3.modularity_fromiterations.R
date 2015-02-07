# evaluate modularity values with repeated measures ANOVA (Friedman) 
# taken from 
# https://github.com/michaelandric/steadystate/blob/master/modularity_conn/72.modularity_fromiterationsMAX.R
writeLines(paste('Evaluating modularity Q vals with non-parametric repeated measures \nWorking dir:',getwd(),'\n',date(),'\n'), sep ="")
subjects <- c("ANGO","CLFR","MYTP","TRCO","PIGL","SNNW","LDMW","FLTM","EEPA","DNLN","CRFO","ANMS","MRZM","MRVV","MRMK","MRMC","MRAG","MNGO","LRVN")
conditions <- seq(4)
densities <- c('0.05')

for (de in densities)
{
    mod_data <- c()
    stddev_data <- c()
    subject_frame <- c()
    condition_frame <- c()
    writeLines(paste('GRAPH LINK DENSITY ',de,'\n',date(), sep = ""))
    for (ss in subjects)
    {
        setwd(paste("/mnt/lnif-storage/urihas/MAstdstt/",ss,"/Qvals/", sep = ""))
        for (i in conditions)
        {
            modscores <- c()
            filelist = list.files(pattern = glob2rx(paste("*",ss,".",i,"*.Qval", sep = "")))
            for (f in filelist)
            {
                modscores <- c(modscores, as.matrix(read.table(f)))
            }
            mod_data <- c(mod_data, max(modscores))
            stddev_data <- c(stddev_data, sd(modscores))
            subject_frame <- c(subject_frame, ss)
            condition_frame <- c(condition_frame, paste("cond",i,sep=""))
        }
    }
    mod_score_frame <- data.frame(mod_data,subject_frame,condition_frame)
    colnames(mod_score_frame) <- c("modularity","subject","condition")
    print(summary(aov(modularity ~ condition + Error(subject/condition), data=mod_score_frame)))
    cond_means <- tapply(mod_score_frame$modularity, mod_score_frame$condition, mean)
    print(cond_means)
    cond_meds <- tapply(mod_score_frame$modularity, mod_score_frame$condition, median)
    print(cond_meds)
    attach(mod_score_frame)
    print(pairwise.t.test(modularity, condition, p.adjust.method="bonferroni",paired=T))
    #with(mod_score_frame, pairwise.t.test(modularity, condition, p.adjust.method="fdr", paired=T))
    c1 = c(modularity[which(condition=="cond1")])
    c2 = c(modularity[which(condition=="cond2")])
    c3 = c(modularity[which(condition=="cond3")])
    c4 = c(modularity[which(condition=="cond4")])
    ## non-parametric 
    print(friedman.test(modularity ~ condition | subject))
    print(wilcox.test(c1,c2,paired=T))
    print(wilcox.test(c1,c3,paired=T))
    print(wilcox.test(c1,c4,paired=T))
    print(wilcox.test(c2,c3,paired=T))
    print(wilcox.test(c2,c4,paired=T))
    print(wilcox.test(c3,c4,paired=T))
}