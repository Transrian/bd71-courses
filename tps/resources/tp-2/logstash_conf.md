# Input

> Pensez à remplacer avec les bonnes valeurs!

```ruby
input {
      elasticsearch {
        hosts => "https://elasticsearch.bd71.transrian.fr:443"
        query => '{ "query": { "range": { "@timestamp": { "gte": "now-1m/m" } } }, "_source": [ "host", "@timestamp", "message", "path" ] } '
        user => "<groupeX>"
        password => "<groupeX>"
        index => "PROF_ACCESS"
        schedule => "* * * * *"

        # Seulement nécessaire si:
        #   - 1. Vous utilisez Guacamole
        #   - 2. Il y a une erreur mentionnant le fait que Logstash ne reussisse pas
        #        a communiquer avec Elasticsearch
        
        #proxy => "http://proxy.utbm.fr:3128"
      }
    }
```

# Filter

```ruby
filter {
  
  # If start by an ip followed with a space
  if [message] =~ /^(?<![0-9])(?:(?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5]))(?![0-9]) / {
    
    # We take into account the more common web format
    grok {
      pattern_definitions => {
        "NOT_QUOTE" => '[^"]+'
        "BASE_HTTP" => '%{IPORHOST:[source][address]} - %{DATA:[user][name]} \[%{HTTPDATE:[apache][access][time]}\] "(?:%{WORD:[http][request][method]} %{NOTSPACE:[url][original]}(?: HTTP/%{NUMBER:[http][version]:float})?|%{DATA:rawrequest})" (?:-|%{NUMBER:[http][response][status_code]:int}) (?:-|%{NUMBER:[http][response][body][bytes]:int})'
        "COMBINE_HTTP" => '%{BASE_HTTP} "%{NOT_QUOTE:[http][request][referrer]}" "%{NOT_QUOTE:[user_agent][original]}"'
        "PROXY_ACCESS" => '%{COMBINE_HTTP} %{NUMBER:[proxy][access][request_count]:int} "%{NOTSPACE:[proxy][access][frontend_name]}" "%{NOTSPACE:[proxy][access][backend_url]}" %{NUMBER:[event][duration]:float}'
      }
      match => {
        "message" => [
          "%{PROXY_ACCESS}",
          "%{COMBINE_HTTP}",
          "%{BASE_HTTP}"
        ]
      }
      tag_on_failure => []
      add_field => {
        "[@metadata][parsing_done]" => true
      }
    }
    
    # If parsing was successfull
    if [@metadata][parsing_done] {
      mutate {
        add_field => {
          "[event][category]" => "web"
          "[event][kind]" => "event"
          "[event][type]" => "access"
          "[event][created]" => "%{@timestamp}"
        }
      }
      
      # We add some ECS fields
      if !([http][response][status_code]) {
        mutate {
          add_field => {
            "[event][outcome]" => "unknown"
          }
        }
      } else if [http][response][status_code] > 400 {
        mutate {
          add_field => {
            "[event][outcome]" => "failure"
          }
        }
      } else {
        mutate {
          add_field => {
            "[event][outcome]" => "success"
          }
        }
      }
    }
    
    # We try to locate the ip adress (will only work on public ips)
    if [source][address] {
      mutate {
        add_field => {
          "[source][ip]" => "%{[source][address]}"
        }
      }
    }
    
    if [source][address] {
      geoip {
         source => "[source][address]"
         target => "[source][geo]"
         fields => ["location", "city_name", "country_code2"]
         tag_on_failure => ["geoip_failure"]
      }
      
      if "geoip_failure" in [tags] {
        mutate {
          remove_field => ["[source][geo]"]
          remove_tag => ["geoip_failure"]
        }
      } else if [source][geo][country_code2] {
        mutate {
          add_field => {
            "[source][geo][country_iso_code]" => "%{[source][geo][country_code2]}"
          }
        }
        mutate {
          remove_field => [ "[source][geo][country_code2]" ]
        }
      }
    }
    
    # We parse the date
    date {
      match => [ "[apache][access][time]", "dd/MMM/yyyy:HH:mm:ss Z" ]
      target => "@timestamp"
      remove_field => ["[apache]"]
    }
    
    # We split the urls, for being easier to manipulate in Kibana
    if [url][original] {
       grok {
        pattern_definitions => {
          "URL_PASSWORD" => '[^@]*'
          "NOT_HASHTAG" => '[^#]+'
        }
        match => {
          "[url][original]" => [
            "((%{URIPROTO:[url][scheme]}://)?(%{USER:[url][username]}:%{USER:[url][password]}@)?%{IPORHOST:[url][address]}(:%{POSINT:[url][port]})?)?%{URIPATH:[url][path]}(\?%{NOT_HASHTAG:[url][query]})?(#%{NOTSPACE:[url][fragment]})?"
            ]
        }
      }
      grok {
        pattern_definitions => {
          "NOT_SLASH" => '[^/]+'
        }
        break_on_match => false
        match => {
          "[url][path]" => ["%{GREEDYDATA}/%{NOT_SLASH}\.%{PROG:[url][extension]}"]
        }
        tag_on_failure => []
      }
      
      if ![url][extension] or [url][extension] in ["html", "htm", "xhtm", "xht", "mht", "mhtml", "maff", "asp", "aspx", "bml", "cfm", "cgi", "ihtml", "jsp", "las", "lasso", "lassoapp", "pl", "php", "phtml", "shtml", "stm"] {
        mutate {
          add_field => {
            "[url][type]" => "server"
          }
        }
      } else {
        mutate {
          add_field => {
            "[url][type]" => "resource"
          }
        }
      }
      
      if [event][duration] {
        ruby {
          code => "event.set('[event][duration]', event.get('[event][duration]') * 1000000)"
        }
      }
    }
    
    # We split user agent in subparts
    if [user_agent][original] and [user_agent][original] != "-" {
      useragent {
        source => "[user_agent][original]"
        target => "[@metadata][user_agent_tmp]"
      }
      
      if [@metadata][user_agent_tmp][device] {
        mutate { add_field => { "[user_agent][device][name]" => "%{[@metadata][user_agent_tmp][device]}" } }
      }
      if [@metadata][user_agent_tmp][os_name] {
        mutate { add_field => { "[user_agent][os][name]" => "%{[@metadata][user_agent_tmp][os_name]}" } }
      }
      if [@metadata][user_agent_tmp][name] {
        mutate { add_field => { "[user_agent][name]" => "%{[@metadata][user_agent_tmp][name]}" } }
      }
      
      # Same thing for OS
      if [@metadata][user_agent_tmp][os_major] {
        mutate {
          add_field => {
            "[user_agent][os][version]" => "%{[@metadata][user_agent_tmp][os_major]}"
          }
        }
      
        if [@metadata][user_agent_tmp][os_minor] {
          mutate {
            replace => {
              "[user_agent][os][version]" => "%{[user_agent][os][version]}.%{[@metadata][user_agent_tmp][os_minor]}"
            }
          }
      
          if [@metadata][user_agent_tmp][os_patch] {
            mutate {
              replace => {
                "[user_agent][os][version]" => "%{[user_agent][os][version]}.%{[@metadata][user_agent_tmp][os_patch]}"
              }
            }
      
            if [@metadata][user_agent_tmp][os_build] {
              mutate {
                replace => {
                  "[user_agent][os][version]" => "%{[user_agent][os][version]}.%{[@metadata][user_agent_tmp][os_build]}"
                }
              }
            }
          }
        }
      
        mutate {
          add_field => {
            "[user_agent][os][full]" => "%{[user_agent][os][name]} %{[user_agent][os][version]}"
          }
        }
      }
      
      # User agent version ECS compatibility
      if [@metadata][user_agent_tmp][major] {
        mutate {
          add_field => {
            "[user_agent][version]" => "%{[@metadata][user_agent_tmp][major]}"
          }
        }
      
        if [@metadata][user_agent_tmp][minor] {
          mutate {
            replace => {
              "[user_agent][version]" => "%{[user_agent][version]}.%{[@metadata][user_agent_tmp][minor]}"
            }
          }
      
          if [@metadata][user_agent_tmp][patch] {
            mutate {
              replace => {
                "[user_agent][version]" => "%{[user_agent][version]}.%{[@metadata][user_agent_tmp][patch]}"
              }
            }
      
            if [@metadata][user_agent_tmp][build] {
              mutate {
                replace => {
                  "[user_agent][version]" => "%{[user_agent][version]}.%{[@metadata][user_agent_tmp][build]}"
                }
              }
            }
          }
        }
      }

    }
    
    if [tags] and (![tags][0]) {
      mutate {
        remove_field => ["tags"]
      }
    }
    
  }
  
}
```