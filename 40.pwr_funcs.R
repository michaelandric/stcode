##generate histograms for each person in each condition.
##average histograms across conditions
subjects <- c("ANGO","CLFR","MYTP","TRCO","PIGL","SNNW","LDMW","FLTM","EEPA","DNLN","CRFO","ANMS","MRZM","MRVV","MRMK","MRMC","MRAG","MNGO","LRVN")
#subjects <- c("ANGO")
conditions <- seq(4)

library(RColorBrewer)
thepal = colorRampPalette(brewer.pal(9,"Set2"))(9)

#library(brainwaver)
cutoff = 1
deg_func <- function(x)
{
    degree.dist = x[which(x > cutoff)]
    nmax = max(degree.dist)
    tmp = hist(degree.dist, breaks=c(cutoff:nmax),plot=F)
    cum.dist = 1-cumsum(tmp$counts)/length(degree.dist)
    d = fitting(x, nmax)
    ptshape = d$alpha + d$gamma
    gamma.trace<-1-pgamma((0:nmax),shape=d$alpha,scale=d$beta) 
    Rsq = round((cor(log10(cum.dist)[1:(nmax-1)], log10(gamma.trace)[1:(nmax-1)]))^2, 4)

    return(list("gamma.trace"=gamma.trace, "cum.dist"=cum.dist, "nmax"=nmax, "shape"=ptshape))
}

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
    AIC.exp <- -2 * (n.regions * log(mu) - mu * sum(degree.dist)) + 
        2
    AIC.pow <- -2 * (n.regions * log(gamma - 1) - gamma * sum(log(x))) + 
        2
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
    write.table(fitting, "fitting.txt", row.names = FALSE, col.names = FALSE, 
        quote = FALSE)
    list(mu = mu, gamma = gamma, alpha = alpha, beta = beta)
}


condition_names = c("Highly ordered", "Some order", "Random", "Almost Random")
thepalOrder = thepal[c(1,2,4,3)] 

#pdf(paste("/mnt/tier2/urihas/Andric/steadystate/groupstats/Vers2deg_distribution_plotsGROUP",cutoff,".pdf",sep=""), paper="a4r", width=10.5)
pdf(paste("/mnt/tier2/urihas/Andric/steadystate/groupstats/Vers2deg_distribution_plotsGROUP",cutoff,"_5p.pdf",sep=""), paper="a4r", width=10.5)   # doing this at the new level of density threshold 5%
par(mfrow=c(2,4))
setwd(paste("/mnt/tier2/urihas/Andric/steadystate/links_files5p/", sep = ""))   # doing this at the new level of density threshold 5%
for (ss in subjects)
{
#    setwd(paste("/mnt/tier2/urihas/Andric/steadystate/",ss,"/corrTRIM_BLUR",sep=""))
    dat <- c()
    for (i in conditions)
    {
        #dat <- c(dat, as.matrix(read.table(paste(ss,".",i,".degrees_gray",sep=""))))
        dat <- c(dat, as.matrix(read.table(paste(ss,".",i,".5p_linksthresh_proportion.degrees_gray", sep = ""))))
    }
    dat_matrix <- matrix(dat, ncol=4)
    rsquares <- c()
    for (i in conditions)
    {
        out = deg_func(dat_matrix[,i])
        Rsq = round((cor(log10(out$cum.dist)[1:(out$nmax-2)], log10(out$gamma.trace)[1:(out$nmax-2)]))^2, 4)
        rsquares = c(rsquares, Rsq)
        #plot(log10(cutoff:(out$nmax-1)), out$log10cnts, main=paste(condition_names[i]," R^2+",out$Rsq,4,sep=""))
        plot(log10(cutoff:(out$nmax-1)),log10(out$cum.dist),pch=3,xlab="log(k)",ylab="log(cumulative distribution)", main=paste(ss," ",condition_names[i]," // R^2=",round(Rsq,4),sep=""))
        #lines(log10(cutoff:(out$nmax-1)), out$gamma.trace, col=thepalOrder[i],lwd=2)
        lines(log10(cutoff:(out$nmax-1)),log10(out$gamma.trace)[1:(out$nmax-1)], lwd=2, col=thepalOrder[i])
        system(paste("cp fitting.txt fitting_cond",i,"_",ss,"_5p.txt",sep=""))
    }
    #dev.off()
    rsquared_mat = matrix(rsquares, nrow=1, byrow=T)
    #write.table(rsquared_mat, paste("Vers2Rsq_vals",ss,"cutoff",cutoff,".txt",sep=""), row.names=F,col.names=F,quote=F)
}
dev.off()
