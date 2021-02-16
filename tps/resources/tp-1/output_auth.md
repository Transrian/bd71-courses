```
{
      "@version" => "1",
          "host" => "X970670",
          "path" => "/home/valentin/tmp/logstash/input/auth.log",
          "date" => 2021-04-23T16:01:16.000Z,
           "pid" => 13824,
     "programme" => "sshd",
    "@timestamp" => 2021-02-16T21:21:31.250Z,
       "contenu" => "pam_unix(sshd:session): session opened for user ubuntu by (uid=0)",
       "machine" => "valentin-test",
       "message" => "Apr 23 18:01:16 valentin-test sshd[13824]: pam_unix(sshd:session): session opened for user ubuntu by (uid=0)"
}
{
      "@version" => "1",
          "host" => "X970670",
          "path" => "/home/valentin/tmp/logstash/input/auth.log",
          "date" => 2021-04-23T16:02:25.000Z,
           "pid" => 14053,
     "programme" => "su",
    "@timestamp" => 2021-02-16T21:21:31.250Z,
       "contenu" => "+ /dev/pts/0 root:root",
       "machine" => "valentin-test",
       "message" => "Apr 23 18:02:25 valentin-test su[14053]: + /dev/pts/0 root:root"
}
{
      "@version" => "1",
          "host" => "X970670",
          "path" => "/home/valentin/tmp/logstash/input/auth.log",
          "date" => 2021-04-23T15:05:01.000Z,
           "pid" => 13781,
     "programme" => "CRON",
    "@timestamp" => 2021-02-16T21:21:31.251Z,
       "contenu" => "pam_unix(cron:session): session opened for user root by (uid=0)",
       "machine" => "valentin-test",
       "message" => "Apr 23 17:05:01 valentin-test CRON[13781]: pam_unix(cron:session): session opened for user root by (uid=0)"
}
{
      "@version" => "1",
          "host" => "X970670",
          "path" => "/home/valentin/tmp/logstash/input/auth.log",
          "date" => 2021-04-23T16:01:16.000Z,
           "pid" => 13824,
     "programme" => "sshd",
    "@timestamp" => 2021-02-16T21:21:31.242Z,
       "contenu" => "Accepted publickey for ubuntu from 172.16.180.99 port 53332 ssh2: RSA ...",
       "machine" => "valentin-test",
       "message" => "Apr 23 18:01:16 valentin-test sshd[13824]: Accepted publickey for ubuntu from 172.16.180.99 port 53332 ssh2: RSA ..."
}
{
      "@version" => "1",
          "host" => "X970670",
          "path" => "/home/valentin/tmp/logstash/input/auth.log",
          "date" => 2021-04-23T16:02:25.000Z,
           "pid" => 14053,
     "programme" => "su",
    "@timestamp" => 2021-02-16T21:21:31.250Z,
       "contenu" => "pam_unix(su:session): session opened for user root by ubuntu(uid=0)",
       "machine" => "valentin-test",
       "message" => "Apr 23 18:02:25 valentin-test su[14053]: pam_unix(su:session): session opened for user root by ubuntu(uid=0)"
}
{
      "@version" => "1",
          "host" => "X970670",
          "path" => "/home/valentin/tmp/logstash/input/auth.log",
          "date" => 2021-04-23T16:02:25.000Z,
           "pid" => 14053,
     "programme" => "su",
    "@timestamp" => 2021-02-16T21:21:31.251Z,
       "contenu" => "pam_systemd(su:session): Cannot create session: Already running in a session",
       "machine" => "valentin-test",
       "message" => "Apr 23 18:02:25 valentin-test su[14053]: pam_systemd(su:session): Cannot create session: Already running in a session"
}
{
      "@version" => "1",
          "host" => "X970670",
          "path" => "/home/valentin/tmp/logstash/input/auth.log",
          "date" => 2021-04-23T16:02:25.000Z,
           "pid" => 14053,
     "programme" => "su",
    "@timestamp" => 2021-02-16T21:21:31.250Z,
       "contenu" => "Successful su for root by root",
       "machine" => "valentin-test",
       "message" => "Apr 23 18:02:25 valentin-test su[14053]: Successful su for root by root"
}
```