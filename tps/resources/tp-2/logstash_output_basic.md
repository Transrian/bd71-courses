```ruby
output {
    elasticsearch {
        hosts => ["https://elasticsearch.bd71.transrian.fr:443"]
        index => "<groupeX>-access"
        user => "<groupeX>"
        password => "<groupeX>"

        # Seulement nécessaire si:
        #   - 1. Vous utilisez Guacamole
        #   - 2. Il y a une erreur mentionnant le fait que Logstash ne reussisse pas
        #        a communiquer avec Elasticsearch
        
        #proxy => "http://proxy.utbm.fr:3128"
    }
}
```