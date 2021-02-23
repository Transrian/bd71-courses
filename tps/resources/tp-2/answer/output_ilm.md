```ruby
output {
    elasticsearch {
        hosts => ["https://serv-bd71-1:9200", "https://serv-bd71-2:9200", "https://serv-bd71-3:9200"]
        ilm_rollover_alias => "<groupeX>-access_ilm"
        ilm_pattern => "000001"
        ilm_policy => "<groupeX>-access-logs"
        user => "<groupeX>"
        password => "<groupeX>"
        ssl_certificate_verification => "false"
    }
}
```