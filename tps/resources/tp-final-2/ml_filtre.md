```json
{
    "bool": {
      "filter": [
        {
          "range": {
            "valeur_fonciere": {
              "lt": 1000000,
              "gte": 0
            }
          }
        },
        {
          "range": {
            "surface_terrain": {
              "lt": 10000,
              "gte": 0
            }
          }
        },
        {
          "bool": {
            "should": [
              {
                "match_phrase": {
                  "local.type": "Appartement"
                }
              },
              {
                "match_phrase": {
                  "local.type": "Maison"
                }
              }
            ],
            "minimum_should_match": 1
          }
        }
      ]
    }
}
```