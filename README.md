# cripto_test


### Run
```bash
     docker-compose up 
```

### NetWork
```yaml
backend_swagger: http://localhost:8000/docs
backend_redoc: http://localhost:8000/redoc
front_end: http://localhost:3000
```

### Run backend test
```bash
 docker exec -it cripto_back_end pytest --durations=0 -vv
```
