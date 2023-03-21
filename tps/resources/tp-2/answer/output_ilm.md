```ruby
output {
    elasticsearch {
        hosts => ["https://elasticsearch.bd71.transrian.fr:443"]
        ilm_rollover_alias => "<groupeX>-access_ilm"
        ilm_pattern => "000001"
        ilm_policy => "<groupeX>-access-logs"
        user => "<groupeX>"
        password => "<groupeX>"
        ssl_certificate_verification => "false"
    
        # Seulement nécessaire si:
        #   - 1. Vous utilisez Guacamole
        #   - 2. Il y a une erreur mentionnant le fait que Logstash ne reussisse pas
        #        a communiquer avec Elasticsearch
        
        #proxy => "http://proxy.utbm.fr:3128"
    }
}
```