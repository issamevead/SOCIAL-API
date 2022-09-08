# Docker run command

```bash
docker run -d --dns 8.8.8.8 --dns 1.1.1.1 --restart=always -p $(sudo zerotier-cli get e4da7455b2b5ee3b ip):6060:8080 --name social-api evead/social-api
```