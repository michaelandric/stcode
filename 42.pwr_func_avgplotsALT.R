##generate histograms for each person in each condition.
subjects <- c("ANGO","CLFR","MYTP","TRCO","PIGL","SNNW","LDMW","FLTM","EEPA","DNLN","CRFO","ANMS","MRZM","MRVV","MRMK","MRMC","MRAG","MNGO","LRVN")
conditions <- seq(4)

library(RColorBrewer)
thepal = colorRampPalette(brewer.pal(9,"Set2"))(9)

cutoff = 1

fitting <- function (degree.dist, nmax) 
{
    n.regions <- length(degree.dist)
    tmp <- hist(degree.dist, breaks = c(0:nmax),plot=F)
    cum.dist <- 1 - cumsum(tmp$counts)/n.regions
    mu <- 1/(sum(degree.dist)/n.regions)
    nb <- length(degree.dist[degree.dist > 0])
    gamma <- 1 + nb/(sum(log(degree.dist[degree.dist > 0])))
    x <- degree.dist
    x <- x[x > 0]
    n <- length(x)
    fn <- function(p) -(-n * p * log(sum(x)/(n * p)) - n * log(gamma(p)) + 
        (p - 1) * sum(log(x)) - n * p)
    out <- nlm(fn, p = 1, hessian = TRUE)
    alpha <- out$estimate
    beta <- sum(degree.dist)/(n.regions * alpha)
    AIC.exp <- -2 * (n.regions * log(mu) - mu * sum(degree.dist)) + 2
    AIC.pow <- -2 * (n.regions * log(gamma - 1) - gamma * sum(log(x))) + 2
    AIC.trunc <- -2 * (-out$minimum) + 2
    fitting <- "mu ="
    fitting <- paste(fitting, mu, sep = " ")
    fitting <- paste(fitting, "gamma = ", sep = "\n")
    fitting <- paste(fitting, gamma, sep = " ")
    fitting <- paste(fitting, "alpha = ", sep = "\n")
    fitting <- paste(fitting, alpha, sep = " ")
    fitting <- paste(fitting, "beta = ", sep = "\n")
    fitting <- paste(fitting, beta, sep = " ")
    fitting <- paste(fitting, "AIC exp = ", sep = "\n")
    fitting <- paste(fitting, AIC.exp, sep = " ")
    fitting <- paste(fitting, "AIC pow = ", sep = "\n")
    fitting <- paste(fitting, AIC.pow, sep = " ")
    fitting <- paste(fitting, "AIC trunc = ", sep = "\n")
    fitting <- paste(fitting, AIC.trunc, sep = " ")
    #write.table(fitting, "fitting.txt", row.names = FALSE, col.names = FALSE, quote = FALSE)
    list(mu = mu, gamma = gamma, alpha = alpha, beta = beta)
}


condition_names = c("Highly ordered", "Some order", "Random", "Almost Random")
thepalOrder = thepal[c(1,2,4,3)] 
#pdf(paste("/mnt/tier2/urihas/Andric/steadystate/groupstats/AvgCountHists_deg_distributions",cutoff,".pdf",sep=""), paper="a4r", width=10.5)
#par(mfrow=c(2,2))
i=1
indiv_counts <-c()
dat1 <- c()
dat2 <- c()
dat3 <- c()
dat4 <- c()
for (ss in subjects)
{
    #setwd(paste("/mnt/tier2/urihas/Andric/steadystate/",ss,"/corrTRIM_BLUR",sep=""))
    setwd(paste("/mnt/tier2/urihas/Andric/steadystate/links_files5p/",sep=""))
    indiv_counts <- c(indiv_counts, length(as.matrix(read.table(paste(ss,".",i,".5p_linksthresh_proportion.degrees_gray",sep="")))))
    dat1 <- c(dat1, as.matrix(read.table(paste(ss,".",i,".5p_linksthresh_proportion.degrees_gray",sep=""))))
}

setwd(paste("/mnt/tier2/urihas/Andric/steadystate/groupstats/",sep=""))
dat1 = dat1[which(dat1 > cutoff)]
tmp1 = hist(dat1, breaks=c(cutoff:max(dat1)),plot=F)
cum.dist1 = 1-cumsum(tmp1$counts)/length(dat1)
d1 = fitting(dat1, max(dat1))
gamma.trace1 <- 1-pgamma((0:max(dat1)),shape=d1$alpha,scale=d1$beta)
#points(log10(cutoff:(max(dat1)-1)),log10(cum.dist1),pch=3,xlab="log(k)",ylab="log(cumulative distribution)")
#lines(log10(cutoff:(max(dat1))),log10(gamma.trace1)[1:(max(dat1))], lwd=2, col=thepalOrder[i])
   
i=2
indiv_counts <-c()
for (ss in subjects)
{
    #setwd(paste("/mnt/tier2/urihas/Andric/steadystate/",ss,"/corrTRIM_BLUR",sep=""))
    setwd(paste("/mnt/tier2/urihas/Andric/steadystate/links_files5p/",sep=""))
    indiv_counts <- c(indiv_counts, length(as.matrix(read.table(paste(ss,".",i,".5p_linksthresh_proportion.degrees_gray",sep="")))))
    dat2 <- c(dat2, as.matrix(read.table(paste(ss,".",i,".5p_linksthresh_proportion.degrees_gray",sep=""))))
}

setwd(paste("/mnt/tier2/urihas/Andric/steadystate/groupstats/",sep=""))
dat2 = dat2[which(dat2 > cutoff)]
tmp2 = hist(dat2, breaks=c(cutoff:max(dat2)),plot=F)
cum.dist2 = 1-cumsum(tmp2$counts)/length(dat2)
d2 = fitting(dat2, max(dat2))
gamma.trace2 <- 1-pgamma((0:max(dat2)),shape=d2$alpha,scale=d2$beta)
#points(log10(cutoff:(max(dat2)-1)),log10(cum.dist2),pch=3,xlab="log(k)",ylab="log(cumulative distribution)")
#lines(log10(cutoff:(max(dat2))),log10(gamma.trace2)[1:(max(dat))], lwd=2, col=thepalOrder[i])

i=3
indiv_counts <-c()
for (ss in subjects)
{
    #setwd(paste("/mnt/tier2/urihas/Andric/steadystate/",ss,"/corrTRIM_BLUR",sep=""))
    setwd(paste("/mnt/tier2/urihas/Andric/steadystate/links_files5p/",sep=""))
    indiv_counts <- c(indiv_counts, length(as.matrix(read.table(paste(ss,".",i,".5p_linksthresh_proportion.degrees_gray",sep="")))))
    dat3 <- c(dat3, as.matrix(read.table(paste(ss,".",i,".5p_linksthresh_proportion.degrees_gray",sep=""))))
}

setwd(paste("/mnt/tier2/urihas/Andric/steadystate/groupstats/",sep=""))
dat3 = dat3[which(dat3 > cutoff)]
tmp3 = hist(dat3, breaks=c(cutoff:max(dat3)),plot=F)
cum.dist3 = 1-cumsum(tmp3$counts)/length(dat3)
d3 = fitting(dat3, max(dat3))
gamma.trace3 <- 1-pgamma((0:max(dat3)),shape=d3$alpha,scale=d3$beta)
#points(log10(cutoff:(max(dat3)-1)),log10(cum.dist3),pch=3,xlab="log(k)",ylab="log(cumulative distribution)")
#lines(log10(cutoff:(max(dat3))),log10(gamma.trace3)[1:(max(dat3))], lwd=2, col=thepalOrder[i])

i=4
indiv_counts <-c()
for (ss in subjects)
{
    #setwd(paste("/mnt/tier2/urihas/Andric/steadystate/",ss,"/corrTRIM_BLUR",sep=""))
    setwd(paste("/mnt/tier2/urihas/Andric/steadystate/links_files5p/",sep=""))
    indiv_counts <- c(indiv_counts, length(as.matrix(read.table(paste(ss,".",i,".5p_linksthresh_proportion.degrees_gray",sep="")))))
    dat4 <- c(dat4, as.matrix(read.table(paste(ss,".",i,".5p_linksthresh_proportion.degrees_gray",sep=""))))
}

setwd(paste("/mnt/tier2/urihas/Andric/steadystate/groupstats/",sep=""))
dat4 = dat4[which(dat4 > cutoff)]
tmp4 = hist(dat4, breaks=c(cutoff:max(dat4)),plot=F)
cum.dist4 = 1-cumsum(tmp4$counts)/length(dat4)
d4 = fitting(dat4, max(dat4))
gamma.trace4 <- 1-pgamma((0:max(dat4)),shape=d4$alpha,scale=d4$beta)

#pdf("Condition_log10fits.pdf")
pdf("Condition_log10fits_5p.pdf")
#plot(log10(cutoff:(max(dat1)-1)),log10(cum.dist1),pch=1,xlab="log(k)",ylab="log(cumulative distribution)",cex=.25)
#points(log10(cutoff:(max(dat2)-1)),log10(cum.dist2),pch=2,xlab="log(k)",ylab="log(cumulative distribution)",cex=.25)
#points(log10(cutoff:(max(dat3)-1)),log10(cum.dist3),pch=3,xlab="log(k)",ylab="log(cumulative distribution)",cex=.25)
#points(log10(cutoff:(max(dat4)-1)),log10(cum.dist4),pch=4,xlab="log(k)",ylab="log(cumulative distribution)",cex=.25)
plot(log10(cutoff:(max(dat1))),log10(gamma.trace1)[1:(max(dat1))], lwd=3, col=thepalOrder[1],type="l")
lines(log10(cutoff:(max(dat2))),log10(gamma.trace2)[1:(max(dat2))], lwd=3, col=thepalOrder[2])
lines(log10(cutoff:(max(dat3))),log10(gamma.trace3)[1:(max(dat3))], lwd=3, col=thepalOrder[3])
lines(log10(cutoff:(max(dat4))),log10(gamma.trace4)[1:(max(dat4))], lwd=3, col=thepalOrder[4])
legend("bottomleft",legend=c("Highly ordered","Some order", "Almost random", "Random"),pch=15,col=c(thepal[1:4]))
dev.off()
#dev.off()

