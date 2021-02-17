```elixir
Apr  3 18:01:16 valentin-test sshd[13824]: Accepted publickey for ubuntu from 172.16.180.99 port 53332 ssh2: 
  RSA key was accepted
Apr 23 18:01:16 valentin-test sshd[13824]: pam_unix(sshd:session): session opened for user ubuntu by (uid=0)
Apr 23 18:02:25 valentin-test su[14053]: Successful su for root by root
Apr 23 18:02:25 valentin-test su[14053]: + /dev/pts/0 root:root
Apr 23 18:02:25 valentin-test su[14053]: pam_unix(su:session): session opened:
  User is root, logged-in by ubuntu (uid=0)
Apr 23 18:02:25 valentin-test su[14053]: pam_systemd(su:session): Cannot create session: Already running in a session
Apr 23 17:05:01 valentin-test CRON[13781]: pam_unix(cron:session): session opened for user root by (uid=0)
```