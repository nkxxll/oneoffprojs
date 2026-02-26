# Overleaf Server Fixes - Work Completed

## Summary
Fixed a self-hosted Overleaf (ShareLaTeX) Community Edition server by resolving multiple configuration, version compatibility, and data migration issues.

## Problems Solved

1. **Incompatible Configuration**: Sandboxed compiles enabled (Server Pro feature only) causing startup failures
2. **Path Mismatches**: Host paths in `docker-compose.yml` used wrong SSH user home directory
3. **MongoDB Version Mismatch**: Server running MongoDB 6.0 but Overleaf required MongoDB 8.0
4. **Data Incompatibility**: Upgrading MongoDB/Redis caused failures due to incompatible data formats
5. **Replica Set Issues**: MongoDB replica set not initialized, blocking startup
6. **SSL/Proxy Issues**: Initial Nginx proxy attempts failed due to certificate and port conflicts

## Solutions Implemented

### 1. Docker Compose Configuration Updates
- **Disabled Sandboxed Compiles**: Commented out `SANDBOXED_COMPILES` environment variables
- **Fixed Paths**: Updated all host volume paths from `/home/user/` to `/home/nkxxll/`
- **MongoDB Upgrade**: Changed image from `mongo:6.0` to `mongo:8.0`
- **Automated Replica Set**: Modified MongoDB healthcheck to auto-initialize replica set

### 2. Data Migration
Wiped existing data directories to resolve version conflicts:
```bash
sudo rm -rf ~/snap/docker/3377/mongo_data ~/snap/docker/3377/redis_data
```

### 3. Startup Script (`dockerup.sh`)
Created automated startup script with replica set initialization:
```bash
#!/bin/bash
ssh nkxxll@<ip> "cd overleaf && docker compose up -d && sleep 5 && docker exec mongo mongosh --eval 'rs.initiate({_id: \"overleaf\", members: [{_id: 0, host: \"mongo:27017\"}]})' || true"
```

### 4. Nginx Reverse Proxy (HTTPS)
Configured local Nginx on host providing HTTPS on port 4322 → proxies to Overleaf on port 4321

**Key Configuration:**
```nginx
server {
    listen 4322 ssl;
    server_name <ip>;
    ssl_certificate /etc/ssl/certs/overleaf.crt;
    ssl_certificate_key /etc/ssl/private/overleaf.key;
    
    location / {
        proxy_pass http://localhost:4321;
        proxy_set_header X-Forwarded-Proto https;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Key Code Changes

### MongoDB Service (docker-compose.yml)
```yaml
mongo:
  restart: always
  image: mongo:8.0
  container_name: mongo
  command: --replSet overleaf --bind_ip_all
  volumes:
    - ~/mongo_data:/data/db
  healthcheck:
    test: >
      mongosh --quiet --eval "
      try { rs.status().ok && 1 }
      catch(e) { rs.initiate({_id:'overleaf', members:[{_id:0, host:'mongo:27017'}]}) && 1 }
      "
    interval: 10s
    timeout: 10s
    retries: 10
```

### Overleaf Port Exposure
```yaml
sharelatex:
  ports:
    - "4321:80"
```

## Result
Overleaf server now starts successfully with proper MongoDB 8.0, initialized replica set, and HTTPS access via local Nginx proxy.
