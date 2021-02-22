```ruby
output {
    elasticsearch {
        hosts => ["https://serv-bd71-1:9200", "https://serv-bd71-2:9200", "https://serv-bd71-3:9200"]
        index => "<groupeX>-access"
        user => "<groupeX>"
        password => "<groupeX>"
        ssl_certificate_verification => "false"
    }
}
```