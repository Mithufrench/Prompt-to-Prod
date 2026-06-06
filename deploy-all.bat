@echo off
REM Prompt-to-Prod Complete Deployment Script
REM Deploys all 3 options: Local Docker, Kubernetes, and Terraform

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo Prompt-to-Prod Complete Deployment
echo ==========================================
echo.

REM Colors (using findstr for colored output)
set "SUCCESS=[OK]"
set "ERROR=[ERROR]"
set "INFO=[INFO]"

echo %INFO% Starting deployment...
echo.

REM ========== OPTION 1: LOCAL DOCKER COMPOSE ==========
echo.
echo ========== OPTION 1: LOCAL DOCKER COMPOSE ==========
echo %INFO% Building Docker image...

docker build -t p2p-agent:latest .\ai-agent
if errorlevel 1 (
    echo %ERROR% Docker build failed
    goto error
)
echo %SUCCESS% Docker image built

echo %INFO% Starting Docker Compose stack...
docker compose up -d
if errorlevel 1 (
    echo %ERROR% Docker Compose startup failed
    goto error
)
echo %SUCCESS% Docker Compose stack started

REM Wait for services
echo %INFO% Waiting for services to be healthy...
for /L %%i in (1,1,30) do (
    curl -s http://localhost:8000/health >nul 2>&1
    if not errorlevel 1 (
        echo %SUCCESS% API is healthy
        goto compose_success
    )
    timeout /t 1 /nobreak >nul
)
echo %INFO% (Services may still be starting - check with 'docker compose logs')

:compose_success
echo.
echo ========== OPTION 1 COMPLETE ==========
echo API running at: http://localhost:8000
echo Database: localhost:5432 (admin/testpassword123)
echo.

REM ========== OPTION 2: KUBERNETES DEPLOYMENT ==========
echo.
echo ========== OPTION 2: KUBERNETES DEPLOYMENT ==========
echo %INFO% Checking kubectl...

kubectl version --client >nul 2>&1
if errorlevel 1 (
    echo %ERROR% kubectl not found. Install kubectl to continue with K8s deployment
    echo %INFO% Skipping Kubernetes deployment
    goto skip_k8s
)

echo %INFO% Creating Kubernetes namespace...
kubectl apply -f manifests\namespace.yaml
if errorlevel 1 (
    echo %ERROR% Failed to create namespace
    goto skip_k8s
)

echo %INFO% Creating secrets...
kubectl create secret generic ai-agent-secrets ^
  --from-literal=OPENAI_API_KEY=sk-test-key-placeholder ^
  -n ai-agent --dry-run=client -o yaml ^| kubectl apply -f -
if errorlevel 1 (
    echo %ERROR% Failed to create secrets
    goto skip_k8s
)

echo %INFO% Deploying to Kubernetes...
kubectl apply -f manifests\
if errorlevel 1 (
    echo %ERROR% Failed to deploy manifests
    goto skip_k8s
)

echo %SUCCESS% Kubernetes manifests deployed

echo %INFO% Waiting for deployment to be ready...
kubectl rollout status deployment/ai-agent -n ai-agent --timeout=5m >nul 2>&1
if not errorlevel 1 (
    echo %SUCCESS% Deployment is ready
)

echo.
echo ========== OPTION 2 COMPLETE ==========
echo To access: kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent
echo.

:skip_k8s

REM ========== OPTION 3: TERRAFORM DEPLOYMENT ==========
echo.
echo ========== OPTION 3: TERRAFORM DEPLOYMENT ==========
echo %INFO% Checking Terraform...

terraform version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Terraform not found. Install Terraform to continue with infrastructure deployment
    echo %INFO% Skipping Terraform deployment
    goto skip_terraform
)

echo %INFO% Checking AWS credentials...
aws sts get-caller-identity >nul 2>&1
if errorlevel 1 (
    echo %ERROR% AWS credentials not configured. Run 'aws configure' first
    echo %INFO% Skipping Terraform deployment
    goto skip_terraform
)

echo %INFO% Initializing Terraform...
cd terraform
terraform init
if errorlevel 1 (
    echo %ERROR% Terraform init failed
    cd ..
    goto skip_terraform
)

echo %INFO% Planning Terraform deployment...
terraform plan -var-file=terraform.tfvars -out=tfplan >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Terraform plan failed
    cd ..
    goto skip_terraform
)

echo %INFO% Applying Terraform configuration...
echo %INFO% This will provision AWS infrastructure (EKS, VPC, RDS)
echo %INFO% Press CTRL+C to cancel, or wait...
timeout /t 5

terraform apply tfplan
if errorlevel 1 (
    echo %ERROR% Terraform apply failed
    cd ..
    goto skip_terraform
)

echo %SUCCESS% Infrastructure deployed

echo %INFO% Extracting cluster information...
for /f %%i in ('terraform output -raw eks_cluster_name 2^>nul') do set CLUSTER_NAME=%%i
for /f %%i in ('terraform output -raw eks_cluster_endpoint 2^>nul') do set CLUSTER_ENDPOINT=%%i

echo %INFO% Configuring kubectl...
aws eks update-kubeconfig --region us-east-1 --name !CLUSTER_NAME! >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Failed to update kubeconfig
    cd ..
    goto skip_terraform
)

echo %SUCCESS% kubectl configured

cd ..

echo.
echo ========== OPTION 3 COMPLETE ==========
echo EKS Cluster: !CLUSTER_NAME!
echo Endpoint: !CLUSTER_ENDPOINT!
echo.

:skip_terraform

REM ========== FINAL STATUS ==========
echo.
echo ==========================================
echo DEPLOYMENT COMPLETE
echo ==========================================
echo.
echo OPTION 1 - LOCAL DOCKER COMPOSE
echo   Status: RUNNING
echo   API: http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo   Database: localhost:5432
echo   Command: docker compose logs -f
echo.
echo OPTION 2 - KUBERNETES
echo   Status: DEPLOYED
echo   Check status: kubectl get pods -n ai-agent
echo   View logs: kubectl logs -n ai-agent deployment/ai-agent
echo   Port forward: kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent
echo.
echo OPTION 3 - TERRAFORM
echo   Status: Check console output above
echo   EKS Cluster: !CLUSTER_NAME!
echo   Next: Deploy application to new cluster
echo.
echo ==========================================
echo NEXT STEPS:
echo.
echo 1. Test Local Stack:
echo    curl http://localhost:8000/health
echo.
echo 2. Test Kubernetes (if deployed):
echo    kubectl port-forward svc/ai-agent 8000:8000 -n ai-agent
echo    curl http://localhost:8000/health
echo.
echo 3. View logs:
echo    docker compose logs -f
echo    kubectl logs -n ai-agent deployment/ai-agent
echo.
echo 4. Stop services:
echo    docker compose down
echo    kubectl delete namespace ai-agent
echo    terraform destroy -var-file=terraform.tfvars
echo.
echo ==========================================
echo.

goto end

:error
echo.
echo %ERROR% Deployment failed. Check errors above.
exit /b 1

:end
