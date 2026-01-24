# Port Configuration Summary

## Overview
This document describes the port configuration across all services in the chatbot application.

## Service Ports

### 1. Backend (FastAPI)
- **Container Port**: `8000`
- **Service Port**: `8000`
- **Exposed in Dockerfile**: `8000`
- **Health Check**: `/health` on port `8000`
- **Metrics**: `/metrics` on port `8000`
- **Status**: ✅ Consistent across all configurations

### 2. Frontend (Next.js)
- **Container Port**: `3001`
- **Service Port**: `80` (LoadBalancer) → `3001` (targetPort)
- **Exposed in Dockerfile**: `3001`
- **Health Check**: `/` on port `3001`
- **Status**: ✅ Fixed - Now consistent across all configurations
- **Changes Made**:
  - Updated `containerPort` from `3000` to `3001`
  - Updated liveness/readiness probe ports from `3000` to `3001`

### 3. Monitoring (Prometheus + Grafana)
- **Prometheus Port**: `9090`
  - Container Port: `9090`
  - Service Port: `9090`
  - Exposed in Dockerfile: `9090`
  
- **Grafana Port**: `3003`
  - Container Port: `3003`
  - Service Port: `3003`
  - Exposed in Dockerfile: `3003`
  - Configured in Grafana: `3003` (consistent)
  
- **Status**: ✅ Fixed - Now consistent across all configurations
- **Changes Made**:
  - Updated Grafana `containerPort` from `3000` to `3003`
  - Updated Grafana service `targetPort` from `3000` to `3003`
  - Updated Grafana internal configuration from `3001` to `3003`

## Port Mapping Summary

| Service | Internal Port | Docker Compose | Kubernetes Service | External Access |
|---------|--------------|----------------|-------------------|-----------------|
| Backend | 8000 | 8000:8000 | ClusterIP:8000 | Internal only |
| Frontend | 3001 | 3001:3001 | LoadBalancer:80→3001 | Port 80 |
| Prometheus | 9090 | 9090:9090 | LoadBalancer:9090 | Port 9090 |
| Grafana | 3003 | 3003:3003 | LoadBalancer:3003 | Port 3003 |

## Access URLs (Kubernetes)

When deployed in Kubernetes with LoadBalancer services:

- **Frontend**: `http://<EXTERNAL-IP>:80` or `http://<EXTERNAL-IP>`
- **Prometheus**: `http://<EXTERNAL-IP>:9090`
- **Grafana**: `http://<EXTERNAL-IP>:3003`
- **Backend**: Internal only via `http://chatbot-backend-service:8000`

## Docker Compose Access URLs

When running with docker-compose:

- **Frontend**: `http://localhost:3001`
- **Backend**: `http://localhost:8000`
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3003`

## Notes

1. The backend is exposed as `ClusterIP` in Kubernetes (internal only) for security reasons
2. Frontend uses LoadBalancer to expose on port 80 (standard HTTP port)
3. Monitoring services use LoadBalancer for easy access to dashboards
4. All health checks and probes use the correct internal container ports
5. Grafana is configured internally on port 3003 and exposed on port 3003 (consistent)

## Health Check Endpoints

- **Backend**: `GET /health` on port `8000`
- **Frontend**: `GET /` on port `3001`
- **Monitoring**: No health checks configured (Recreate strategy used)

## Prometheus Scrape Targets

Configured in `prometheus.yml`:
- Backend: `chatbot-backend-service:8000/metrics`
- Prometheus: `localhost:9090`
