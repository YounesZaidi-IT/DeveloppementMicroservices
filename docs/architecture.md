## Services

- vehicules : possède les VÉHICULES (modèle, tarif par jour, places)
- locations : possède les LOCATIONS (véhicule, date début, date fin, prix total)
- notifications : ne possède pas de donnée métier principale, il réagit aux événements

## Qui appelle qui

- locations -> vehicules : vérifier que le véhicule existe et récupérer son tarif avant de créer une location

vehicules   → manages vehicules
locations   → manages locations

For Vehicle location theme :

- vehicules → owns vehicles
  - id
  - modele
  - tarif_par_jour
  - places

- locations → owns rentals
  - id
  - vehicule_id
  - date_debut
  - date_fin
  - prix_total

- notifications → optional, sends/reacts to rental events.

Relation
locations → vehicules

Before creating a rental, locations asks vehicules:
- does the vehicle exist?
- what is its daily price?