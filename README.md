# cripto_test


### Run
```bash
     docker-compose up 
```

### NetWork
```yaml
backend_swagger: http://localhost:8100/docs #para loguearse en el campo username va el correo
backend_redoc: http://localhost:8100/redoc
front_end: http://localhost:3100
postgres: 
  host: localhost
  port: 5100
  user: postgres
  password: postgres

```

```yaml
default_user: master@master.com
default_pass: master
```

### Run backend test
```bash
 docker exec -it cripto_back_end pytest --durations=0 -vv
```
