# Prompt-to-Prod: Complete Setup & Usage Guide

## ✅ Your Platform is Ready!

Your **Prompt-to-Prod AI-powered DevOps platform** is fully containerized and ready to deploy with 3 different options.

---

## 🚀 QUICK START (Choose One)

### OPTION 1: Local Development (Fastest - 2 minutes)

Perfect for development and testing locally.

```powershell
cd C:\Projects\Prompt-to-Prod

# Build and start
docker build -t p2p-agent:latest ./ai-agent
docker compose up -d

# Verify
docker ps
curl http://localhost:8000/health

# View logs
docker compose logs -f ai-agent
```

**Access Points:**
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`
- Metrics: `http://localhost:8000/metrics`
- Database: `localhost:5432` (admin/testpassword123)

**Stop:**
```powershell
docker compose down
```

---

### OPTION 2: Kubernetes (Local/Cloud Cluster - 5 minutes)

Deploy to an existing Kubernetes cluster (minikube, EKS, GKE, AKS).

**Prerequisites:**
- `kubectl` installed and configured
- Access to a Kubernetes cluster

```powershell
# Create namespace
kubectl apply -f manifests\namespace.yaml

# Create secrets
kubectl create secret generic ai-agent-secrets `
  --from-literal=OPENAI_API_KEY=sk-your-key-here `
  -n ai-agent

# Deploy
kubectl apply -f manifests\

# Verify
kubectl get pods -n ai-agent
kubectl get svc -n ai-agent

# Port forward to access
kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent

# In another terminal, test:
curl http://localhost:8000/health
```

**View Logs:**
```powershell
kubectl logs -n ai-agent deployment/ai-agent
kubectl logs -n ai-agent deployment/ai-agent -f  # follow
```

**Cleanup:**
```powershell
kubectl delete namespace ai-agent
```

---

### OPTION 3: Full Infrastructure on AWS (10-15 minutes)

Provisions entire infrastructure: VPC, EKS cluster, RDS database, NAT gateways, etc.

**Prerequisites:**
- AWS account with credentials configured
- `terraform` installed
- `aws` CLI configured (`aws configure`)
- `kubectl` installed

```powershell
cd C:\Projects\Prompt-to-Prod\terraform

# Check AWS credentials
aws sts get-caller-identity

# Initialize
terraform init

# Plan (review what will be created)
terraform plan -var-file=terraform.tfvars -out=tfplan

# Apply (creates AWS resources)
terraform apply tfplan

# Wait 5-10 minutes for EKS cluster to be ready...

# Get cluster info
terraform output

# Configure kubectl
aws eks update-kubeconfig --region us-east-1 --name p2p-eks-dev

# Verify connection
kubectl get nodes

# Deploy application to the new cluster
cd ..
kubectl apply -f manifests\

# Verify deployment
kubectl get pods -n ai-agent
kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent
```

**Destroy (Remove AWS Resources):**
```powershell
cd terraform
terraform destroy -var-file=terraform.tfvars
```

---

## 🧪 TESTING

### Test the API

```powershell
# Health check
curl http://localhost:8000/health

# Chat endpoint
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{"query": "What are Kubernetes best practices?"}'

# Metrics
curl http://localhost:8000/metrics

# Web UI
Start-Process "http://localhost:3000"
```

### Run Unit Tests

```powershell
cd C:\Projects\Prompt-to-Prod

pip install -r ai-agent\requirements.txt pytest
pytest ai-agent\tests\ -v
```

### Docker Compose Tests

```powershell
# Start stack
docker compose up -d

# Wait 30 seconds
Start-Sleep -Seconds 30

# Test
curl http://localhost:8000/health
docker compose logs

# Stop
docker compose down
```

---

## 📊 MONITORING

### Local Monitoring Stack

```powershell
# Start with Prometheus and Grafana
docker compose -f docker-compose.monitoring.yml up -d

# Access dashboards
Start-Process "http://localhost:9090"      # Prometheus
Start-Process "http://localhost:3001"      # Grafana (admin/admin)
```

### Kubernetes Monitoring

```powershell
# Install Prometheus on cluster
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring

# Port forward Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

---

## 🔄 CI/CD PIPELINE

### GitHub Actions Setup

1. **Push code to GitHub:**
   ```powershell
   git remote add origin https://github.com/your-org/prompt-to-prod.git
   git branch -M main
   git push -u origin main
   ```

2. **Add GitHub Secrets:**
   - Go to: Settings → Secrets and variables → Actions
   - Add these secrets:
     - `KUBE_CONFIG` (base64-encoded kubeconfig)
     - `DOCKER_USERNAME` (container registry username)
     - `DOCKER_PASSWORD` (container registry token)

3. **Workflows trigger on:**
   - Push to `main` or `develop` branches
   - Pull requests to `main`
   - Git tags starting with `v*`

**Workflow files:**
- `.github\workflows\build-test-push.yml` - Build, test, push image
- `.github\workflows\deploy.yml` - Deploy to Kubernetes

---

## 🛠️ COMMON COMMANDS

### Docker Compose

```powershell
# Start
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f
docker compose logs ai-agent
docker compose logs postgres

# Rebuild
docker compose build --no-cache

# Remove volumes
docker compose down -v

# Shell into container
docker compose exec ai-agent bash
docker compose exec postgres psql -U admin -d p2pdb
```

### Kubernetes

```powershell
# View all resources
kubectl get all -n ai-agent

# View pods
kubectl get pods -n ai-agent
kubectl get pods -n ai-agent -o wide

# View services
kubectl get svc -n ai-agent

# View logs
kubectl logs -n ai-agent deployment/ai-agent
kubectl logs -n ai-agent pod/<pod-name>
kubectl logs -n ai-agent -f deployment/ai-agent   # Follow

# Describe pod
kubectl describe pod <pod-name> -n ai-agent

# Port forward
kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent
kubectl port-forward pod/<pod-name> 8000:8000 -n ai-agent

# Execute command in pod
kubectl exec -it <pod-name> -n ai-agent -- bash
kubectl exec -it <pod-name> -n ai-agent -- python -c "print('hello')"

# Delete resources
kubectl delete pod <pod-name> -n ai-agent
kubectl delete deployment ai-agent -n ai-agent
kubectl delete namespace ai-agent

# Scale deployment
kubectl scale deployment ai-agent --replicas=3 -n ai-agent

# Update image
kubectl set image deployment/ai-agent \
  ai-agent=p2p-agent:latest -n ai-agent

# Check events
kubectl get events -n ai-agent
kubectl describe events -n ai-agent
```

### Terraform

```powershell
cd terraform

# Initialize
terraform init

# Validate
terraform validate

# Format code
terraform fmt

# Plan
terraform plan -var-file=terraform.tfvars -out=tfplan

# Apply
terraform apply tfplan

# Show resources
terraform show

# Output values
terraform output
terraform output eks_cluster_name

# Destroy
terraform destroy -var-file=terraform.tfvars
terraform destroy -var-file=terraform.tfvars -auto-approve
```

---

## 📈 SCALING & MANAGEMENT

### Horizontal Scaling (Kubernetes)

```powershell
# Scale to 5 replicas
kubectl scale deployment ai-agent --replicas=5 -n ai-agent

# Auto-scaling (requires metrics-server)
kubectl apply -f - <<EOF
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-agent-hpa
  namespace: ai-agent
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-agent
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
EOF
```

### Update Application

```powershell
# Build new image
docker build -t p2p-agent:v1.1.0 ./ai-agent
docker tag p2p-agent:v1.1.0 your-registry/p2p-agent:v1.1.0
docker push your-registry/p2p-agent:v1.1.0

# Update Kubernetes deployment
kubectl set image deployment/ai-agent \
  ai-agent=your-registry/p2p-agent:v1.1.0 -n ai-agent --record

# Check rollout status
kubectl rollout status deployment/ai-agent -n ai-agent

# Rollback if needed
kubectl rollout undo deployment/ai-agent -n ai-agent
```

---

## 🐛 TROUBLESHOOTING

### Container won't start

```powershell
# Check logs
docker logs p2p-agent
docker compose logs ai-agent

# Rebuild without cache
docker build -t p2p-agent:latest ./ai-agent --no-cache

# Check image
docker inspect p2p-agent:latest
```

### Pod stuck in pending

```powershell
# Check pod status
kubectl describe pod <pod-name> -n ai-agent

# Check nodes
kubectl get nodes
kubectl top nodes

# Check events
kubectl get events -n ai-agent --sort-by='.lastTimestamp'
```

### Database connection issues

```powershell
# Check database pod
kubectl get pod -n ai-agent -l app=postgres
kubectl logs -n ai-agent deployment/postgres

# Test connection
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- \
  psql -h postgres.ai-agent.svc.cluster.local -U admin -d p2pdb

# Port forward and test locally
kubectl port-forward svc/postgres 5432:5432 -n ai-agent
psql -h localhost -U admin -d p2pdb
```

### API endpoint not responding

```powershell
# Check service
kubectl get svc -n ai-agent
kubectl describe svc ai-agent -n ai-agent

# Check endpoints
kubectl get endpoints -n ai-agent

# Port forward
kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent

# Check pod logs
kubectl logs -n ai-agent deployment/ai-agent

# Check resource usage
kubectl top pods -n ai-agent
```

---

## 📋 CHECKLIST

### Initial Setup
- [ ] Docker Desktop installed
- [ ] `.env` file created with `OPENAI_API_KEY`
- [ ] `kubectl` configured (for K8s option)
- [ ] AWS credentials configured (for Terraform option)
- [ ] Terraform installed (for Terraform option)

### Local Stack (Option 1)
- [ ] Docker image builds successfully
- [ ] Containers start: `docker ps`
- [ ] Health check passes: `curl http://localhost:8000/health`
- [ ] API responds: `curl http://localhost:8000/docs`

### Kubernetes (Option 2)
- [ ] Cluster accessible: `kubectl get nodes`
- [ ] Namespace created: `kubectl get ns ai-agent`
- [ ] Pods running: `kubectl get pods -n ai-agent`
- [ ] Service endpoints active: `kubectl get endpoints -n ai-agent`
- [ ] API accessible via port-forward

### Terraform (Option 3)
- [ ] AWS credentials verified
- [ ] Terraform initialized: `terraform init`
- [ ] Plan successful: `terraform plan`
- [ ] Infrastructure deployed: `terraform apply`
- [ ] EKS cluster ready: `aws eks describe-cluster`
- [ ] kubectl configured: `kubectl get nodes`

---

## 📚 QUICK REFERENCE

| Task | Command |
|------|---------|
| Start Local Stack | `docker compose up -d` |
| Stop Local Stack | `docker compose down` |
| View Local Logs | `docker compose logs -f` |
| Deploy to K8s | `kubectl apply -f manifests\` |
| Check K8s Pods | `kubectl get pods -n ai-agent` |
| Check K8s Logs | `kubectl logs -n ai-agent deployment/ai-agent` |
| Port Forward K8s | `kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent` |
| Deploy Infrastructure | `terraform apply -var-file=terraform.tfvars` |
| Destroy Infrastructure | `terraform destroy -var-file=terraform.tfvars` |
| Test API | `curl http://localhost:8000/health` |
| Run Tests | `pytest ai-agent\tests\ -v` |

---

## 🎯 NEXT STEPS

1. **Choose your deployment option** (Local, K8s, or Terraform)
2. **Run the setup command** for your option
3. **Verify it's working** with health check
4. **Explore the API** with Swagger docs
5. **Configure monitoring** (Prometheus/Grafana)
6. **Set up CI/CD** (GitHub Actions)
7. **Add production hardening** (TLS, backups, scaling)

---

## 💡 TIPS

- Start with **Option 1 (Local)** to test quickly
- Use **Option 2 (K8s)** for team/staging environments
- Use **Option 3 (Terraform)** for production infrastructure
- Always run `terraform plan` before `terraform apply`
- Keep `.env` file secure (add to `.gitignore`)
- Monitor costs in AWS console when using Terraform
- Use `docker compose logs -f` to debug local issues
- Use `kubectl logs` to debug K8s issues

---

## 📞 SUPPORT

Check files for more details:
- `README.md` - Project overview and architecture
- `DEPLOYMENT.md` - Detailed deployment guide
- `docker-compose.yml` - Local stack configuration
- `manifests/` - Kubernetes manifests
- `terraform/` - Infrastructure as Code
- `.github/workflows/` - CI/CD pipelines

**Your platform is ready to use! 🚀**
