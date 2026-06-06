# Prompt-to-Prod: Deployment & Testing Guide

## ✅ Status

Your complete AI-powered DevOps platform is **containerized and ready to deploy**.

## 🏗️ Project Components Built

| Component | Status | Location |
|-----------|--------|----------|
| **AI Agent** (LangChain + FastAPI) | ✅ Ready | `ai-agent/` |
| **Frontend** (React Web UI) | ✅ Ready | `frontend/` |
| **Terraform IaC** | ✅ Ready | `terraform/` |
| **Ansible Playbooks** | ✅ Ready | `ansible/` |
| **Kubernetes Manifests** | ✅ Ready | `manifests/` |
| **GitOps (ArgoCD)** | ✅ Ready | `gitops/` |
| **CI/CD Workflows** | ✅ Ready | `.github/workflows/` |
| **Docker Compose** | ✅ Ready | `docker-compose.yml` |
| **Monitoring** | ✅ Ready | `monitoring/` |

---

## 🚀 Local Deployment (Docker Compose)

### 1. Setup Environment

```bash
cd C:\Projects\Prompt-to-Prod

# Copy environment template
copy .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 2. Build and Start Services

```bash
# Build AI Agent image
docker build -t p2p-agent:latest ./ai-agent

# Start all services
docker compose up -d

# Verify services are running
docker ps

# Check logs
docker compose logs -f ai-agent
```

### 3. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are Kubernetes best practices?"}'

# Check metrics
curl http://localhost:8000/metrics

# Access web UI
# Open browser: http://localhost:3000 (when frontend is running)
```

### 4. Stop Services

```bash
docker compose down
```

---

## ☸️ Kubernetes Deployment

### 1. Prerequisites

```bash
# Install kubectl
# Install Helm (optional)
# Access to a Kubernetes cluster (EKS, GKE, AKS, or local minikube)

# Verify cluster access
kubectl cluster-info
```

### 2. Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f manifests/namespace.yaml

# Create secrets
kubectl create secret generic ai-agent-secrets \
  --from-literal=OPENAI_API_KEY=sk-your-key-here \
  -n ai-agent

# Apply all manifests
kubectl apply -f manifests/

# Verify deployment
kubectl get pods -n ai-agent
kubectl get svc -n ai-agent

# Check pod status
kubectl describe pod -n ai-agent

# View logs
kubectl logs -n ai-agent deployment/ai-agent
```

### 3. Access the Service

```bash
# Port forward to local machine
kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent

# Test from another terminal
curl http://localhost:8000/health
```

### 4. Deploy with GitOps (ArgoCD)

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Create ArgoCD app
kubectl apply -f gitops/argocd-app.yaml

# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

---

## 🏗️ Infrastructure Deployment (Terraform)

### 1. Setup AWS Credentials

```bash
# Configure AWS CLI
aws configure

# Verify credentials
aws sts get-caller-identity
```

### 2. Initialize Terraform

```bash
cd terraform

# Initialize working directory
terraform init

# Validate configuration
terraform validate

# Plan deployment
terraform plan -var-file="terraform.tfvars" -out=tfplan
```

### 3. Deploy Infrastructure

```bash
# Apply configuration
terraform apply tfplan

# Get outputs
terraform output

# Extract EKS cluster name and endpoint
CLUSTER_NAME=$(terraform output -raw eks_cluster_name)
CLUSTER_ENDPOINT=$(terraform output -raw eks_cluster_endpoint)
```

### 4. Configure kubectl

```bash
# Update kubeconfig
aws eks update-kubeconfig --region us-east-1 --name $CLUSTER_NAME

# Verify connection
kubectl get nodes
```

---

## 🔧 Configuration with Ansible

### 1. Setup Inventory

Edit `ansible/inventory/hosts` with your server IPs:

```ini
[p2p_agent]
agent-server-1 ansible_host=10.0.1.10
agent-server-2 ansible_host=10.0.1.11

[all:vars]
ansible_user=ubuntu
ansible_private_key_file=~/.ssh/id_rsa
```

### 2. Run Playbook

```bash
cd ansible

# Test connectivity
ansible all -i inventory/hosts -m ping

# Run deployment playbook
ansible-playbook -i inventory/hosts playbooks/deploy-agent.yml

# Verify installation
ansible all -i inventory/hosts -m command -a "docker ps"
```

---

## 🧪 Testing

### Unit Tests

```bash
# Install test dependencies
pip install -r ai-agent/requirements.txt pytest

# Run tests
pytest ai-agent/tests/ -v

# With coverage
pytest ai-agent/tests/ --cov=ai_agent --cov-report=html
```

### Integration Tests

```bash
# Start services
docker compose up -d

# Run integration tests
pytest ai-agent/tests/integration/ -v

# Stop services
docker compose down
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/load_test.py --host=http://localhost:8000
```

---

## 📊 Monitoring & Observability

### Local Monitoring Stack

```bash
# Start full stack with monitoring
docker compose -f docker-compose.monitoring.yml up -d

# Access dashboards:
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001 (admin/admin)
```

### Kubernetes Monitoring

```bash
# Install Prometheus Operator
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

# Port forward Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

#### Build & Push Workflow

Triggered on: `push to main/develop`, `pull requests`, `version tags`

```yaml
# .github/workflows/build-test-push.yml
- Build Docker image with BuildKit
- Run unit tests
- Security scanning with Docker Scout
- Push to container registry
- Deploy to Kubernetes
```

#### Deploy Workflow

Triggered on: `push to main`

```yaml
# .github/workflows/deploy.yml
- Update Kubernetes deployment
- Wait for rollout
- Verify health checks
```

### Setup CI/CD

```bash
# Create GitHub secrets
# Settings → Secrets → Actions

# Required secrets:
# KUBE_CONFIG - base64-encoded kubeconfig
# DOCKER_USERNAME - container registry username
# DOCKER_PASSWORD - container registry password
```

---

## 📋 Deployment Checklist

- [ ] Docker installed and running
- [ ] `.env` file created with `OPENAI_API_KEY`
- [ ] Local stack tested (`docker compose up`)
- [ ] API endpoints responding (`curl http://localhost:8000/health`)
- [ ] Kubernetes cluster configured (`kubectl cluster-info`)
- [ ] Manifests deployed (`kubectl apply -f manifests/`)
- [ ] Terraform initialized (`terraform init`)
- [ ] AWS credentials configured (`aws configure`)
- [ ] GitHub Actions secrets created
- [ ] CI/CD workflows pushed to `main` branch
- [ ] Monitoring dashboards accessible
- [ ] Load tests passing

---

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs
docker logs p2p-agent
docker compose logs ai-agent

# Rebuild image
docker build -t p2p-agent:latest ./ai-agent --no-cache
```

### Pod stuck in pending

```bash
# Check pod status
kubectl describe pod <pod-name> -n ai-agent

# Check node resources
kubectl top nodes
kubectl top pods -n ai-agent

# Check events
kubectl get events -n ai-agent
```

### Database connection issues

```bash
# Test connection
kubectl exec -it <agent-pod> -n ai-agent -- psql -h postgres -U admin -d p2pdb

# Check database pod
kubectl logs -n ai-agent deployment/postgres
```

### API endpoint not accessible

```bash
# Check service
kubectl get svc -n ai-agent

# Port forward
kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent

# Test locally
curl http://localhost:8000/health
```

---

## 📈 Next Steps

1. **Deploy to Development**: Run local docker-compose stack, verify all endpoints
2. **Test Infrastructure**: Deploy Terraform stack to AWS/GCP
3. **Configure GitOps**: Set up ArgoCD for automated deployments
4. **Enable Monitoring**: Deploy Prometheus + Grafana stack
5. **Run CI/CD**: Push code to main branch, verify GitHub Actions workflows
6. **Production Hardening**:
   - Enable TLS/SSL certificates
   - Set up backup and disaster recovery
   - Configure autoscaling
   - Implement rate limiting and authentication
   - Set up centralized logging (ELK, Loki)
   - Configure alerting rules

---

## 📚 Documentation

- [AI Agent](./ai-agent/README.md) - LangChain agent implementation
- [Terraform](./terraform/README.md) - Infrastructure as Code
- [Kubernetes](./manifests/README.md) - Kubernetes manifests
- [Ansible](./ansible/README.md) - Configuration management
- [CI/CD](../.github/workflows/README.md) - GitHub Actions workflows

---

**Your Prompt-to-Prod platform is ready to deploy! 🚀**
