# COPY-PASTE READY COMMANDS

Use these commands exactly as shown. Copy and paste into your terminal.

---

## 📍 NAVIGATE TO PROJECT FIRST

```powershell
cd C:\Projects\Prompt-to-Prod
```

---

## OPTION 1: LOCAL DOCKER STACK (Recommended for testing)

### Build Image
```powershell
docker build -t p2p-agent:latest ./ai-agent
```

### Start Services
```powershell
docker compose up -d
```

### Verify Running
```powershell
docker ps
```

### Test Health
```powershell
curl http://localhost:8000/health
```

### View Logs
```powershell
docker compose logs -f ai-agent
```

### Access API Docs
Open browser: `http://localhost:8000/docs`

### Test Chat API
```powershell
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{"query":"What is Kubernetes?"}'
```

### Access Database
```powershell
docker compose exec postgres psql -U admin -d p2pdb
```

### Stop Services
```powershell
docker compose down
```

### Remove Everything (including data)
```powershell
docker compose down -v
```

---

## OPTION 2: KUBERNETES DEPLOYMENT

### Prerequisites Check
```powershell
kubectl version --client
kubectl cluster-info
```

### Create Namespace
```powershell
kubectl apply -f manifests\namespace.yaml
```

### Create Secrets
```powershell
kubectl create secret generic ai-agent-secrets `
  --from-literal=OPENAI_API_KEY=sk-your-key-here `
  -n ai-agent
```

### Deploy Application
```powershell
kubectl apply -f manifests\deployment.yaml
kubectl apply -f manifests\service.yaml
kubectl apply -f manifests\configmap.yaml
```

### Or Deploy All At Once
```powershell
kubectl apply -f manifests\
```

### Verify Deployment
```powershell
kubectl get pods -n ai-agent
kubectl get svc -n ai-agent
```

### View Pod Status
```powershell
kubectl describe pod -n ai-agent
```

### View Logs
```powershell
kubectl logs -n ai-agent deployment/ai-agent
```

### Follow Logs (Real-time)
```powershell
kubectl logs -n ai-agent deployment/ai-agent -f
```

### Port Forward to Access Locally
```powershell
kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent
```

### Test from New Terminal
```powershell
curl http://localhost:8000/health
```

### Scale to 3 Replicas
```powershell
kubectl scale deployment ai-agent --replicas=3 -n ai-agent
```

### Check Scaling Status
```powershell
kubectl get pods -n ai-agent
```

### Delete Entire Deployment
```powershell
kubectl delete namespace ai-agent
```

---

## OPTION 3: TERRAFORM AWS INFRASTRUCTURE

### Navigate to Terraform Directory
```powershell
cd terraform
```

### Prerequisites Check
```powershell
terraform version
aws sts get-caller-identity
```

### Initialize Terraform
```powershell
terraform init
```

### Validate Configuration
```powershell
terraform validate
```

### Create Plan
```powershell
terraform plan -var-file=terraform.tfvars -out=tfplan
```

### Review Plan Output
```powershell
# Review the output above before applying
```

### Apply Infrastructure (Creates AWS Resources)
```powershell
terraform apply tfplan
```

### Wait 10-15 minutes for EKS cluster to be created...

### Get Output Values
```powershell
terraform output
```

### Extract Cluster Name
```powershell
terraform output -raw eks_cluster_name
```

### Configure kubectl
```powershell
aws eks update-kubeconfig --region us-east-1 --name p2p-eks-dev
```

### Verify Connection to New Cluster
```powershell
kubectl get nodes
```

### Go Back to Project Root
```powershell
cd ..
```

### Deploy Application to New Cluster
```powershell
kubectl apply -f manifests\namespace.yaml
kubectl create secret generic ai-agent-secrets `
  --from-literal=OPENAI_API_KEY=sk-your-key-here `
  -n ai-agent
kubectl apply -f manifests\
```

### Verify Deployment on New Cluster
```powershell
kubectl get pods -n ai-agent
```

### Access Application
```powershell
kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent
```

### Test (from new terminal)
```powershell
curl http://localhost:8000/health
```

### Destroy Infrastructure (Removes All AWS Resources)
```powershell
cd terraform
terraform destroy -var-file=terraform.tfvars
```

### Confirm Destruction (Type 'yes' when prompted)
```powershell
# Type: yes
```

---

## ADDITIONAL USEFUL COMMANDS

### View API Documentation
Open in browser: `http://localhost:8000/docs`

### Test Multiple Endpoints

**Health Check:**
```powershell
curl http://localhost:8000/health
```

**Chat Endpoint:**
```powershell
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{"query":"Hello, how are you?"}'
```

**Metrics:**
```powershell
curl http://localhost:8000/metrics
```

### Run Tests
```powershell
pytest ai-agent\tests\ -v
```

### View Docker Images
```powershell
docker images | findstr p2p
```

### View All Docker Containers
```powershell
docker ps -a
```

### View Compose Configuration
```powershell
docker compose config
```

### Check Kubernetes All Resources
```powershell
kubectl get all -n ai-agent
```

### Check Kubernetes Events
```powershell
kubectl get events -n ai-agent
```

### Check Node Resources
```powershell
kubectl top nodes
kubectl top pods -n ai-agent
```

### Execute Command in Kubernetes Pod
```powershell
kubectl exec -it <pod-name> -n ai-agent -- bash
```

### Copy File from Pod
```powershell
kubectl cp ai-agent/<pod-name>:/app/logfile.log ./logfile.log
```

### Describe Service
```powershell
kubectl describe svc ai-agent -n ai-agent
```

### Edit ConfigMap
```powershell
kubectl edit configmap ai-agent-config -n ai-agent
```

### Patch Deployment
```powershell
kubectl patch deployment ai-agent -n ai-agent -p '{"spec":{"replicas":5}}'
```

### Rollout Status
```powershell
kubectl rollout status deployment/ai-agent -n ai-agent
```

### Rollback Deployment
```powershell
kubectl rollout undo deployment/ai-agent -n ai-agent
```

---

## MONITORING COMMANDS

### Start Monitoring Stack
```powershell
docker compose -f docker-compose.monitoring.yml up -d
```

### Access Prometheus
Browser: `http://localhost:9090`

### Access Grafana
Browser: `http://localhost:3001`
Username: `admin`
Password: `admin`

### Stop Monitoring
```powershell
docker compose -f docker-compose.monitoring.yml down
```

---

## TROUBLESHOOTING COMMANDS

### Check Docker Logs
```powershell
docker logs p2p-agent
```

### Check Docker Compose Logs
```powershell
docker compose logs
```

### Check Docker Compose Specific Service
```powershell
docker compose logs ai-agent
docker compose logs postgres
```

### Inspect Docker Container
```powershell
docker inspect p2p-agent
```

### Docker System Info
```powershell
docker system df
```

### Clean Docker System
```powershell
docker system prune -a
```

### Check Kubernetes Pod Events
```powershell
kubectl describe pod <pod-name> -n ai-agent
```

### Check Kubernetes Service Endpoints
```powershell
kubectl get endpoints -n ai-agent
```

### Check Kubernetes Node Status
```powershell
kubectl describe node <node-name>
```

### Check Kubernetes Events (sorted by time)
```powershell
kubectl get events -n ai-agent --sort-by='.lastTimestamp'
```

### Database Connection Test
```powershell
docker compose exec postgres psql -U admin -c "SELECT version();"
```

---

## DEPLOYMENT CHECKLIST

### Before Starting
- [ ] Navigate to: `C:\Projects\Prompt-to-Prod`
- [ ] Check `.env` file exists
- [ ] Verify Docker installed: `docker --version`

### Option 1 (Local)
- [ ] Build image: `docker build -t p2p-agent:latest ./ai-agent`
- [ ] Start stack: `docker compose up -d`
- [ ] Check running: `docker ps`
- [ ] Test health: `curl http://localhost:8000/health`
- [ ] View API docs: `http://localhost:8000/docs`

### Option 2 (Kubernetes)
- [ ] Verify kubectl: `kubectl version --client`
- [ ] Check cluster: `kubectl cluster-info`
- [ ] Create namespace: `kubectl apply -f manifests\namespace.yaml`
- [ ] Deploy: `kubectl apply -f manifests\`
- [ ] Verify: `kubectl get pods -n ai-agent`
- [ ] Port forward: `kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent`
- [ ] Test: `curl http://localhost:8000/health`

### Option 3 (Terraform)
- [ ] Verify Terraform: `terraform version`
- [ ] Check AWS: `aws sts get-caller-identity`
- [ ] Init: `terraform init` (in terraform dir)
- [ ] Plan: `terraform plan -var-file=terraform.tfvars`
- [ ] Apply: `terraform apply tfplan`
- [ ] Wait 15 minutes...
- [ ] Configure kubectl: `aws eks update-kubeconfig --region us-east-1 --name p2p-eks-dev`
- [ ] Deploy app: `kubectl apply -f manifests\`
- [ ] Verify: `kubectl get pods -n ai-agent`

---

## QUICK REFERENCE

| Task | Command |
|------|---------|
| Start Local | `docker compose up -d` |
| Stop Local | `docker compose down` |
| Local Logs | `docker compose logs -f` |
| K8s Deploy | `kubectl apply -f manifests\` |
| K8s Status | `kubectl get pods -n ai-agent` |
| K8s Logs | `kubectl logs -n ai-agent deployment/ai-agent -f` |
| K8s Access | `kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent` |
| TF Init | `terraform init` |
| TF Plan | `terraform plan -var-file=terraform.tfvars` |
| TF Apply | `terraform apply tfplan` |
| TF Destroy | `terraform destroy -var-file=terraform.tfvars` |
| Test Health | `curl http://localhost:8000/health` |
| API Docs | `http://localhost:8000/docs` |

---

**Pick Option 1, 2, or 3 and copy-paste the commands above!** 🚀
