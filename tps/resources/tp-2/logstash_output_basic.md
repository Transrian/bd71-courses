```ruby
output {
    elasticsearch {
        hosts => ["https://elasticsearch.bd51.transrian.fr:443"]
        index => "<groupeX>-access"
        user => "<groupeX>"
        password => "<groupeX>"
        ssl_certificate_verification => "false"
    }
}
```