library(RCurl)
URL <- "http://data.giss.nasa.gov/tmp/gistemp/STATIONS/tmp_305802220000_14_0/station.txt"
destfile <- "bogota.txt"
download.file(URL, destfile, method = "wget", quiet=FALSE)
mydata = read.table("bogota.txt")
str(mydata)
mydata$V1
