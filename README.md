# UE-AD-A1-REST  

## Sommaire
- [Introduction](#introduction-)
- [Détails des composants](#archi)
- [Utilisation](#utilisation)
- 
## Introduction
Il s’agit d’une application jouet et peu réaliste pour gérer les films et les réservations d’utilisateurs dans un cinéma. Cette application est composée de 4 micro-services :

![Diagramme  conceptuel de la solution](conception.png "Diagramme conceptuel")
## Détails des composants
- 🎥 Movie : micro-service responsable de la gestion des films du cinéma. Il contient et gère une petite base de données json contenant la liste des films disponibles avec quelques informations sur les films.
```json
//Exemple de configuration pour un film
  {     
      "title": "The Good Dinosaur",
      "rating": 7.4,
      "director": "Peter Sohn",
      "id": "720d006c-3a57-4b6a-b18f-9b713b073f3c"
    } 
```
- ⏲ Times : micro-service responsable des jours de passage des films dans le cinéma. Il contient et gère une petite base de données json contenant la liste des dates avec l’ensemble des films disponibles à cette date.
```json
//Exemple d'une journée de disponibilité de films
{
      "date":"20151130",
      "movies":[
        "720d006c-3a57-4b6a-b18f-9b713b073f3c",
        "a8034f44-aee4-44cf-b32c-74cf452aaaae",
        "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab"
      ]
    }
```
- 📖 Booking : micro-service responsable de la réservation des films par les utilisateurs. Il contient et gère une petite base de données json contenant une entrée par utilisateurs avec la liste des dates et films réservés. Booking fait appel à Times pour connaître et vérifier que les créneaux réservés existent bien puisqu’il ne connait pas lui même les créneaux des films.
```json
//Exemple de réservations d'un utilisateur
   {
      "userid": "chris_rivers",
      "dates": [
        {
          "date": "20151201",
          "movies": [
            "267eedb8-0f5d-42d5-8f43-72426b9fb3e6"
          ]
        }
      ]
    } 
```
- 👥 User : micro-service qui sert de point d’entrée à tout utilisateur et qui permet ensuite de récupérer des informations sur les films, sur les créneaux disponibles et de réserver. Il contient et gère une petite base de données json avec la liste des utilisateurs. User fait appel à Booking et Movie pour respectivement permettre aux utilisateurs de réserver un film ou d’obtenir des informations sur les films.
```json
//Exemple d'un utilisateur
{
      "date":"20151130",
      "movies":[
        "720d006c-3a57-4b6a-b18f-9b713b073f3c",
        "a8034f44-aee4-44cf-b32c-74cf452aaaae",
        "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab"
      ]
    }
```

