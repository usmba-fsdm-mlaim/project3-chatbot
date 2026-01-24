#!/bin/bash
# =========================================
# Simple K8s Management Script for Chatbot
# Usage: ./k8s.sh deploy   OR   ./k8s.sh cleanup
# =========================================

set -e

# Function to load .env file
load_env() {
    if [ -f "../.env" ]; then
        echo "📄 Loading environment variables from .env file..."
        export $(cat ../.env | grep -v '^#' | xargs)
        echo "✅ Environment variables loaded"
    elif [ -f ".env" ]; then
        echo "📄 Loading environment variables from .env file..."
        export $(cat .env | grep -v '^#' | xargs)
        echo "✅ Environment variables loaded"
    else
        echo "⚠️  No .env file found"
        if [ -z "$WANDB_API_KEY" ]; then
            read -p "Enter your W&B API key: " WANDB_API_KEY
            export WANDB_API_KEY
        fi
    fi
}

# Function to deploy
deploy() {
    echo "🚀 Deploying Chatbot to Kubernetes..."
    echo ""

    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        echo "❌ kubectl is not installed. Please install it first."
        exit 1
    fi

    # Check if Kubernetes cluster is running
    echo "🔍 Checking Kubernetes cluster..."
    if ! kubectl cluster-info &> /dev/null; then
        echo "❌ Kubernetes cluster is not running!"
        echo ""
        echo "Please start your Kubernetes cluster first:"
        echo "  - Docker Desktop: Start Docker Desktop and enable Kubernetes"
        echo "  - Minikube: minikube start"
        echo "  - Kind: kind create cluster"
        echo ""
        exit 1
    fi
    echo "✅ Kubernetes cluster is running"
    echo ""

    # Load environment variables
    load_env
    echo ""

    # Check required variables
    if [ -z "$WANDB_API_KEY" ]; then
        echo "❌ WANDB_API_KEY is not set!"
        exit 1
    fi

    # Create ConfigMap with environment variables
    echo "🔧 Creating ConfigMap with environment variables..."
    kubectl create configmap chatbot-config \
        --from-literal=WANDB_API_KEY="$WANDB_API_KEY" \
        --from-literal=WANDB_PROJECT="${WANDB_PROJECT:-qwen-finetuning}" \
        --from-literal=WANDB_LOG_MODEL="${WANDB_LOG_MODEL:-true}" \
        --from-literal=WANDB_SILENT="${WANDB_SILENT:-true}" \
        --from-literal=ARTIFACT_ADDRESS="${ARTIFACT_ADDRESS:-chatbot-team/qwen-finetuning/youssef-qwen2-medical-bot:v0}" \
        --from-literal=NEXT_PUBLIC_API_URL="http://chatbot-backend-service:8000" \
        --dry-run=client -o yaml | kubectl apply -f -
    echo "✅ ConfigMap created"
    echo ""

    # Deploy everything
    echo "📦 Deploying all resources..."
    kubectl apply -f all-in-one.yaml
    echo "✅ Resources deployed"
    echo ""

    # Show status
    echo "📊 Initial Status:"
    kubectl get pods,svc,hpa
    echo ""
    
    # Watch pod events to see image pulling
    echo "🔍 Watching deployment progress (Ctrl+C to stop)..."
    echo "💡 This will show image pulling and pod startup events..."
    echo ""
    sleep 2
    kubectl get events --watch --field-selector involvedObject.kind=Pod &
    EVENT_PID=$!
    
    # Wait for pods to be ready (with timeout)
    echo "⏳ Waiting for pods to be ready (this may take 2-5 minutes for large images)..."
    kubectl wait --for=condition=ready pod -l app=chatbot-backend --timeout=600s 2>/dev/null || true
    kubectl wait --for=condition=ready pod -l app=chatbot-frontend --timeout=300s 2>/dev/null || true
    
    # Stop watching events
    kill $EVENT_PID 2>/dev/null || true
    
    echo ""
    echo "📊 Final Status:"
    kubectl get pods,svc
    echo ""
    echo "✨ Deployment complete!"
    echo ""
    echo "🌐 Access your services:"
    echo "  Frontend: kubectl get svc chatbot-frontend-service"
    echo "  Monitoring: kubectl get svc chatbot-monitoring-service"
    echo ""
    echo "📋 Useful commands:"
    echo "  kubectl get pods              # Check pod status"
    echo "  kubectl logs -f deployment/chatbot-backend    # View backend logs"
    echo "  kubectl logs -f deployment/chatbot-frontend   # View frontend logs"
}

# Function to cleanup
cleanup() {
    echo "🧹 Cleaning up Chatbot Kubernetes resources..."
    echo ""
    
    kubectl delete -f all-in-one.yaml --ignore-not-found=true
    echo "✅ Resources deleted"
    echo ""
    
    read -p "Delete ConfigMap too? (y/N): " delete_config
    if [[ $delete_config == "y" || $delete_config == "Y" ]]; then
        kubectl delete configmap chatbot-config --ignore-not-found=true
        echo "✅ ConfigMap deleted"
    fi
    
    echo ""
    echo "🎉 Cleanup complete!"
}

# Function to check status
status() {
    echo "📊 Chatbot Kubernetes Status"
    echo "================================"
    echo ""
    
    echo "🔹 Pods:"
    kubectl get pods
    echo ""
    
    echo "🔹 Services:"
    kubectl get svc | grep chatbot
    echo ""
    
    echo "🔹 Autoscalers:"
    kubectl get hpa
    echo ""
    
    echo "🔹 Recent Events:"
    kubectl get events --sort-by='.lastTimestamp' | grep -i "chatbot\|pull\|image" | tail -10
    echo ""
    
    echo "💡 To watch live updates: kubectl get pods -w"
    echo "💡 To see pod details: kubectl describe pod <pod-name>"
    echo "💡 To view logs: kubectl logs -f deployment/chatbot-backend"
}

# Main
case "$1" in
    deploy)
        deploy
        ;;
    cleanup)
        cleanup
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {deploy|cleanup|status}"
        echo ""
        echo "Commands:"
        echo "  deploy    # Deploy chatbot to Kubernetes"
        echo "  cleanup   # Remove all resources"
        echo "  status    # Check deployment status and events"
        echo ""
        echo "Examples:"
        echo "  $0 deploy"
        echo "  $0 status"
        exit 1
        ;;
esac
