[0;1;31m●[0m nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: [0;1;31mfailed[0m (Result: exit-code) since Thu 2021-03-18 02:07:39 UTC; 5s ago
       Docs: man:nginx(8)
    Process: 11607 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; [0;1;31m(code=exited, status=1/FAILURE)[0m

Mar 18 02:07:39 ip-172-31-44-91 systemd[1]: Starting A high performance web server and a reverse proxy server...
Mar 18 02:07:39 ip-172-31-44-91 nginx[11607]: nginx: [emerg] "location" directive is not allowed here in /etc/nginx/sites-enabled/onhwa:1
Mar 18 02:07:39 ip-172-31-44-91 nginx[11607]: nginx: configuration file /etc/nginx/nginx.conf test failed
Mar 18 02:07:39 ip-172-31-44-91 systemd[1]: [0;1;39m[0;1;31m[0;1;39mnginx.service: Control process exited, code=exited, status=1/FAILURE[0m
Mar 18 02:07:39 ip-172-31-44-91 systemd[1]: [0;1;38;5;185m[0;1;39m[0;1;38;5;185mnginx.service: Failed with result 'exit-code'.[0m
Mar 18 02:07:39 ip-172-31-44-91 systemd[1]: [0;1;31m[0;1;39m[0;1;31mFailed to start A high performance web server and a reverse proxy server.[0m
