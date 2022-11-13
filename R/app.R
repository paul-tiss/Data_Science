library(shiny)
library(dplyr)
library(ggplot2)
library(readr)
library(tidyverse)
library(shinydashboard)
library(leaflet)
library(sf)
library(scales)
library(ggmap)
library(geojsonio)
library(broom)
library(mapproj)
library(maps)


table_finale <- read_csv("C:/Users/HP/OneDrive/Bureau/Projet_DSIA/Data_Science/R/table_finale2.csv")
# View(table_finale)

tbl_fin <- as.data.frame(table_finale)

view(tbl_fin)





# Define UI for application that draws a histogram
ui <- dashboardPage(
  
  # Application title
  dashboardHeader(title = "Les communes les plus à risque de France",titleWidth = 500),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Histogrammes", tabName = "scorefinal", icon = icon("dashboard")),
      menuItem("Carte", tabName = "carte", icon = icon("th"))
    )
  ),
  dashboardBody(
    tabItems(
      # First tab content
      tabItem(tabName = "scorefinal",
              fluidRow(
                
                box(
                  title = "Score final",
                  sliderInput("slider1", "Valeur minimal du score:", 0, 300, 40),
                  width = NULL
                ),
                
                box(plotOutput("plot1"), width = NULL),
                
                
                
                box(
                  title = "Score traitment",
                  sliderInput("slider2", "Ratio entre le nombre de déchets reçus et le nombre de déchets traités:", 0, 17, 5),
                  width = NULL
                ),
                
                box(plotOutput("plot2"), width = NULL),
                
                box(
                  title = "Score de pollution",
                  sliderInput("slider3", "Quantité de produits polluants émis:", 0, 63, 15),
                  width = NULL
                ),
              
                box(plotOutput("plot3"), width = NULL),
                
                box(
                  title = "Nombre d'usines polluantes",
                  sliderInput("slider4", "Nombre d'usines:", 1, 241, 100),
                  width = NULL
                ),
                
                box(plotOutput("plot4"), width = NULL),
      )
      
      ),
      
      # Second tab content
      tabItem(tabName = "carte",
              box(plotOutput("plot5"), width = NULL),
      )
    )
  

    )
  )


server <- function(input, output) {
  
 
  
  output$plot1 <- renderPlot({
    
    tbl_fin %>%
      filter(score_final>=input$slider1) %>%
      ggplot(aes(x=score_final))+ geom_bar(aes(y=commune),stat = "identity")
    
  })
  output$plot2 <- renderPlot({
    
    tbl_fin %>%
      filter(score_traitement>=input$slider2) %>%
      ggplot(aes(x=score_traitement))+ geom_bar(aes(y=commune),stat = "identity")
    
  })
  output$plot3 <- renderPlot({
    
    tbl_fin %>%
      filter(score_pollution>=input$slider3) %>%
      ggplot(aes(x=score_pollution))+ geom_bar(aes(y=commune),stat = "identity")
    
  })
  output$plot4 <- renderPlot({

    tbl_fin %>%
      filter((nb_usines_polluantes*10/3)>=input$slider4) %>%
      ggplot(aes(x=(nb_usines_polluantes*10/3)))+ geom_bar(aes(y=commune),stat = "identity")

  })
  output$plot5 <- renderPlot({
    
    tbl_fin %>%
      filter((nb_usines_polluantes*10/3)>=input$slider4) %>%
      ggplot(aes(x=(nb_usines_polluantes*10/3)))+ geom_bar(aes(y=commune),stat = "identity")
    
  })
}

# Run the application 
shinyApp(ui = ui, server = server)



# m <- leaflet() %>%
#   addTiles()
# m
# help(package='maps')
# maps::map('france', fill = TRUE)

# 
# 
# 

# names(tbl_fin)[names(tbl_fin)=='code_insee'] <- 'code_commune'
# 
# 
# spdf <- geojsonio::geojson_read("C:/Users/HP/OneDrive/Bureau/Projet_DSIA/Data_Science/R/communes_light.geojson",what = "sp")
# 
# tbl_test <- tbl_fin %>% select(code_commune, classe_potentiel)
# 
# cartefrance<- merge(tbl_test, spdf,  on = "code_commune" )
# 
# m_exemple <- leaflet(cartefrance) %>% 
#   setView(3,47, zoom = 5) %>%
#   addTiles()
# m_exemple
# 
# m_exemple %>% addPolygons(
#   fillColor = ~pal(classe_potentiel),
#   weight = 2,
#   opacity = 1,
#   color = "white",
#   dashArray = "3",
#   fillOpacity = 0.7)
# cartedata <- as.data.frame(cartefrance$geo_point)
# ligne1 <- cartedata[1:1,]
# ligne2 <- cartedata[2:2,]
# view(ligne2)
# 
# m_exemple %>% addPolygons(
#   lat=ligne1,
#   lng = ligne2
# )
# 
# view(cartefrance$geo_point)
# 
# leaflet::leaflet(cartefrance) %>% 
#   leaflet::addPolygons(
#     data = cartefrance$geo_point,
#     color = "#222", weight = 2, opacity = 1,
#     fillColor = ~pal(classe_potentiel), fillOpacity = 0.7
#   )
# help("addPolygons")
# 
# 
# # spdf_fortified <- tidy(spdf)
# # mypalette <- colorNumeric( palette="viridis", domain=tbl_fin@data$classe_potentiel, na.color="transparent")
# # mypalette(c(45,43))
# 
# 
# 
# 
# ggplot() +
#   geom_polygon(data = spdf, aes( x = long, y = lat, group = group), fill="black", color="red") +
#   theme_void() +
#   coord_map()
