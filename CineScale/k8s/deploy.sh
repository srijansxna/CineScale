#!/bin/bash
# Deploy CineScale to Kubernetes
set -e

echo "Deploying CineScale to Kubernetes..."

kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmap.yaml

# Infrastructure first
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/minio.yaml

echo "Waiting for infrastructure to be ready..."
kubectl rollout status deployment/postgres -n cinescale
kubectl rollout status deployment/redis    -n cinescale
kubectl rollout status deployment/minio    -n cinescale

# Application
kubectl apply -f k8s/api.yaml
kubectl apply -f k8s/worker.yaml
kubectl apply -f k8s/ingress.yaml

echo "Waiting for application to be ready..."
kubectl rollout status deployment/api    -n cinescale
kubectl rollout status deployment/worker -n cinescale

echo ""
echo "Deployment complete!"
kubectl get pods -n cinescale
