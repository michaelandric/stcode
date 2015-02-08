## This is to execute fcorr
Args <- Sys.getenv("R_ARGS")
print(noquote(strsplit(Args," ")[[1]]))
print(length(noquote(strsplit(Args," ")[[1]])))
tstxt <- paste(noquote(strsplit(Args," ")[[1]][1]))
nvox <- as.numeric(noquote(strsplit(Args," ")[[1]][2]))
ntp = 90

library(bct)
fcorr(tstxt,nvox,ntp)