gp2plate1vsplate2 <- function(plate1.dt, plate2.dt, plate1.id, plate2.id, probecolorname, ncols){
  
  names(plate1.dt) <- make.names(names(plate1.dt))
  names(plate2.dt) <- make.names(names(plate2.dt))
  
  plate2.dt$`Well.Position` <- trimws(plate2.dt$`Well.Position`)
  plate1.dt$`Well.Position` <- trimws(plate1.dt$`Well.Position`)
  
  plate1.dt$Number.of.Unique.Labels[plate1.dt$Number.of.Unique.Labels >6] <- 6
  plate2.dt$Number.of.Unique.Labels[plate2.dt$Number.of.Unique.Labels >6] <- 6
  
  plate1.dt.Summary <- plate1.dt %>% group_by(Well.Position,probe.set, Number.of.Unique.Labels) %>% dplyr::summarise(n = n()) %>% dplyr::mutate(total = sum(n)) %>% dplyr::mutate(freq = n/sum(n))
  plate1.dt.Summary$Replicate <- plate1.id
  
  
  plate1.dt.msd <- ddply(plate1.dt.Summary , c("probe.set", "Number.of.Unique.Labels"), dplyr::summarise,
                         mean = mean(freq),
                         sd   = sd(freq),
                         meanN = mean(total),
                         sdN = sd(total)
  )
  plate1.dt.msd$Replicate <- plate1.id
  
  plate2.dt.Summary <- plate2.dt %>% group_by(Well.Position,probe.set, Number.of.Unique.Labels) %>% dplyr::summarise(n = n()) %>% dplyr::mutate(total = sum(n)) %>% dplyr::mutate(freq = n/sum(n))
  plate2.dt.Summary$Replicate <- plate2.id
  
  plate2.dt.msd <- ddply(plate2.dt.Summary , c("probe.set", "Number.of.Unique.Labels"), dplyr::summarise,
                         mean = mean(freq),
                         sd   = sd(freq),
                         meanN = mean(total),
                         sdN = sd(total)
  )
  plate2.dt.msd$Replicate <- plate2.id
  
  
  plate1and2.dt.msd <- rbind(plate2.dt.msd, plate1.dt.msd)
  
  gp2<- ggplot(plate1and2.dt.msd, aes(x=Number.of.Unique.Labels, y=mean, group=probe.set, color=Replicate)) 
  gp2 <- gp2 + theme_bw()+
    #geom_bar(stat="identity", color="black", position=position_dodge())+
    geom_point()+
    geom_errorbar(aes(ymin=mean-sd, ymax=mean+sd), width=.2,position=position_dodge(0.05))+
    ylab('Proportion of Nuclei') + 
    coord_cartesian(xlim = c(0,6), ylim=c(0,0.85)) +
    scale_x_continuous(breaks = 0:6, label = c("0", "1", "2", "3", "4", "5", "6+")) +
    xlab(paste0('Number of ', probecolorname,' FISH signals per nucleus'))+ 
    facet_wrap(~probe.set, ncol=ncols)+
    theme(text = element_text(size=14, family="sans"), 
          legend.position="bottom", legend.direction='horizontal',legend.box='horizontal', 
          legend.title=element_text(size=14, face="bold"), legend.text=element_text(size=12),
          axis.text=element_text(size=14), 
          axis.title.y = element_text(size=18, face="bold"), 
          axis.title.x = element_text(size=18, face="bold"))
  
  out <- list("msd" = plate1and2.dt.msd, "gp2" = gp2)
  
  
  return(out)
}
