```ruby
output {
    elasticsearch {
        hosts => ["https://elasticsearch.bd51.transrian.fr", "https://serv-bd71-2:9200", "https://serv-bd71-3:9200"]
        index => "<groupeX>-access-%{+YYYY.MM.dd}"
        user => "<groupeX>"
        password => "<groupeX>"
        ssl_certificate_verification => "false"
    }
}
```