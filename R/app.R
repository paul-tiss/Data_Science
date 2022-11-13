# Import des library
library(shiny)
library(ggplot2)
library(readr)
library(tidyverse)
library(shinydashboard)
library(leaflet)






# Import des données sous format csv (les données sous format json étant
#  traitées au préalable sur python) 
table_finale <- read_csv("table_finale2.csv", show_col_type = FALSE)

# Conversion de la table en data frame
tbl_fin <- as.data.frame(table_finale)









# Défini l'UI du dashboard
ui <- dashboardPage(
  
  # Titre du dashboard
  dashboardHeader(title = "Les communes les plus à risque de France",titleWidth = 500),
  
  # Définition du menu de navigation sur le coté 
  dashboardSidebar(
    sidebarMenu(
      menuItem("Bar Plot", tabName = "scorefinal"),
      menuItem("Carte", tabName = "carte"),
      menuItem("Histogramme", tabName = "Histogramme")
    )
  ),
  
  # Définition de chaque partie du dashboard
  dashboardBody(
    tabItems(
      # Premier onglet
      tabItem(tabName = "scorefinal",
              fluidRow(
                
                # Slider pour choisir la valeure minimale du score final 
                # observé (plus le score faible, plus il y aura de villes)
                box(
                  title = "Score final",
                  sliderInput("slider1", "Valeur minimal du score:", 0, 300, 40),
                  width = NULL
                ),
                
                # Espace pour afficher le bar plot de chaque ville ayant
                # au moins un score_final équivalent à la valeur du slider
                box(plotOutput("plot1"), width = NULL),
                
                # Slider pour choisir la valeure minimale du score de  
                # traitelent observé (plus le score faible, plus il y aura
                # de villes). Cela représente le ratio entre le nombre de 
                # déchets arrivant et le nombre de déchets traités
                box(
                  title = "Score traitment",
                  sliderInput("slider2", "Ratio entre le nombre de déchets reçus et le nombre de déchets traités:", 0, 17, 5),
                  width = NULL
                ),
               
                # Espace pour afficher le bar plot de chaque ville ayant
                # au moins un score de traitment équivalent à la valeur du
                # slider
                box(plotOutput("plot2"), width = NULL),
                
                # Slider pour choisir la valeure minimale du score de  
                # pollution observé (plus le score faible, plus il y aura
                # de villes). Cela représente la quantité de déchets émis
                # pour chaque communes
                box(
                  title = "Score de pollution",
                  sliderInput("slider3", "Quantité de produits polluants émis:", 0, 63, 15),
                  width = NULL
                ),
              
                # Espace pour afficher le bar plot de chaque ville ayant
                # au moins un score de pollution équivalent à la valeur du
                # slider
                box(plotOutput("plot3"), width = NULL),
      )
      
      ),
      
      # Second onglet
      tabItem(tabName = "carte",
              
              # Espace pour afficher la carte qui place un cercle plus ou 
              # mooins foncé en fonction de la quantité d'usines dans la
              # commune
              box(leafletOutput("plot5"), width = NULL),
      ),
      # Troisième onglet
      tabItem(tabName = "Histogramme",
              fluidRow(
                
                # Slider pour choisir la valeure minimale du nombre   
                # d'usines polluantes par communes observé. Le slider  
                # permet d'affiner le nombre d'usine possédé par commune
                # afin de pouvoir voir plus clairement combien de commune
                # ont au moins "la valeur du slider" usines.
                box(
                title = "Nombre d'usines polluantes",
                sliderInput("slider4", "Nombre d'usines minimales:", 0, 250, 1),
                width = NULL
              ),
              
              # Espace pour afficher l'histogramme décris ci-dessus
              box(plotOutput("plot4"), width = NULL, height = NULL),)
      )
    )
  

    )
  )

# Défini les fonctions du serveur 
server <- function(input, output) {
  
 
  # Lien par rapport au plot1 de la ligne 64
  output$plot1 <- renderPlot({
    
    tbl_fin %>%
      filter(score_final>=input$slider1) %>%
      ggplot(aes(x=score_final))+ geom_bar(aes(y=commune),stat = "identity")
    
  })
  
  # Lien par rapport au plot1 de la ligne 79
  output$plot2 <- renderPlot({
    
    tbl_fin %>%
      filter(score_traitement>=input$slider2) %>%
      ggplot(aes(x=score_traitement))+ geom_bar(aes(y=commune),stat = "identity")
    
  })
  
  # Lien par rapport au plot1 de la ligne 94
  output$plot3 <- renderPlot({
    
    tbl_fin %>%
      filter(score_pollution>=input$slider3) %>%
      ggplot(aes(x=score_pollution))+ geom_bar(aes(y=commune),stat = "identity")
    
  })
  
  # Lien par rapport au plot1 de la ligne 123
  output$plot4 <- renderPlot({

    tbl_fin %>%
      filter((nb_usines_polluantes*10/3)>=input$slider4) %>%
      ggplot(aes(x=(nb_usines_polluantes*10/3)))+ geom_histogram()

  })
  
  # Lien par rapport au plot1 de la ligne 105
  output$plot5 <- renderLeaflet({
    
    # Le calcul retourne la racine carré du nombre d'usines poluantes afin
    # que la cartographie soit plus lisible et parlante
    tbl_fin$nb_usines_polluantes <- sqrt(tbl_fin$nb_usines_polluantes*10/3)
    
    
    # Création d'une palette de couleur et des valeures associées
    mybins <- seq(0.1, 16, by=1.8)
    mypalette <- colorBin( palette="YlOrBr", domain=tbl_fin$nb_usines_polluantes, na.color="transparent", bins=mybins)
    
    # Préparation du texte qui s'affiche lorsque la souris passe sur 
    # chaque rond
    mytext <- paste(
      "Nombre usines: ", tbl_fin$nb_usines_polluantes,
      "<br/>",
      "Commune: ", tbl_fin$commune
    ) %>%
      lapply(htmltools::HTML)
    
    # Assemblage de la carte voulue
    m <- leaflet(tbl_fin) %>% 
      addTiles()  %>% 
      setView( lat=47,lng=3, zoom = 5.5) %>%
      addProviderTiles("Esri.WorldImagery") %>%
      addCircleMarkers(~long,
                       ~lat, 
                       fillColor = ~mypalette(nb_usines_polluantes), fillOpacity = 0.7, color="white", radius=5, stroke=FALSE,
                       label = mytext,
                       labelOptions = labelOptions( style = list("font-weight" = "normal", padding = "3px 8px"), textsize = "13px", direction = "auto")
      ) %>%
      addLegend( pal=mypalette, values=~nb_usines_polluantes, opacity=0.9, title = "Nombre usines", position = "bottomright" )
    
    
  })
}

# Lance l'application
shinyApp(ui = ui, server = server)





