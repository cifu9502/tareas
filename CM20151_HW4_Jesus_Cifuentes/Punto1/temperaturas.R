library(bitops)
library(RCurl)
library(g.data)
library(ggplot2)

#Por lo que entiendo a veces las url's de los datos se cambian, en ese caso, solo hay que 
#ir a cada una de ellas en http://data.giss.nasa.gov/cgi-bin/gistemp/find_station.cgi?dt=1&ds=14&name=&world_map.x=217&world_map.y=210
#y cambiar las url's que tenemos a continuación

urlBogo <- "http://data.giss.nasa.gov/tmp/gistemp/STATIONS/tmp_305802220000_14_0/station.txt"
urlCali <- "http://data.giss.nasa.gov/tmp/gistemp/STATIONS/tmp_305802590000_14_0/station.txt"
urlBuca <- "http://data.giss.nasa.gov/tmp/gistemp/STATIONS/tmp_305800940000_14_0/station.txt"
urlBarr <- "http://data.giss.nasa.gov/tmp/gistemp/STATIONS/tmp_305800280000_14_0/station.txt"
urlIpia <- "http://data.giss.nasa.gov/tmp/gistemp/STATIONS/tmp_305803700000_14_0/station.txt"

#en este archivo guardaremos los datos descarcados, lo reutilizarmos varias veces
destfile <- "temperatura.txt"

#Esta función recibe como parametro la URL y el nombre de la ciudad asignada, descarga los
# archivos y los organiza en un dataframe

getData <- function(URL, ciudad){
  
  #descarga los archivos en destfile de acuerda a la url dada por parametro. Recuerde que las url's pueden cambiar
  download.file(URL, destfile, method = "wget", quiet=FALSE)
  bog = read.table(destfile, stringsAsFactors = FALSE)
  #Inicializamos las variables que van a corresponder a las columnas del dataframe
  year = ""
  Ciudad = ""
  month = ""
  date = ""
  temp = 0
  acum = 1 
  #se recorren los datos uno por uno
  for (i in 2:length(bog[,1])) {
    for (j in 2: 13) {
      k = j-1
      n = as.numeric(bog[i,j])
      
      #Vamos a omitir aquellos datos que no tienen mediciones, los cuales estan indicados
      #por el numero 999.9
      
      if(n < 999){
        temp[acum] = n
        year[acum] = bog[i,1]
        month[acum] = bog[1,j]
        Ciudad[acum] = ciudad
        if(k<10){
          s = paste(c(0,k), collapse = "")
          date[acum] = paste(c(bog[i,1],s,"01"), collapse = "-")
        }
        if(k>=10){
          date[acum] = paste(c(bog[i,1],k,"01"), collapse = "-")
        }
        acum = acum +1
      }
    }
  }
  #Se guardan los diferentes vectores en el dataframe
  Temp <- data.frame( Year = year, Month = month, Date = date,  City = Ciudad, Temperature = temp)
  #Guardamos la fecha en el formato adecuado
  Temp$Date =  as.Date(Temp$Date , "%Y-%m-%d")
  return(Temp)
}

#Por cada una de las ciudades se invoca getData y se unen los dataframes obtenidos
Data = getData(urlBogo, "Bogota")
data =  getData(urlCali, "Cali")
Data = rbind(Data, data)
data =  getData(urlBuca, "Bucaramanga")
Data = rbind(Data, data)
data =  getData(urlBarr, "Barranquilla")
Data = rbind(Data, data)
data =  getData(urlIpia, "Ipiales")
Data = rbind(Data, data)

#Se escribe el data frame en temperaturas.csv
write.csv(Data, file = "temperaturas.csv")


str(Data)

q <- ggplot(Data, aes(x = Date, y = Temperature) )
q <- q + geom_line(aes( colour = City)) + ggtitle("Temperature in Colombian Cities")+  theme_bw()
q
ggsave(q, file="temperaturas.png")
