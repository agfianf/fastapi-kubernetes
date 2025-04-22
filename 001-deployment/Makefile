# Makefile for FastAPI Kubernetes Deployment
# This Makefile provides commands to manage a FastAPI application in Kubernetes using Minikube

# 1. Initialize Minikube Cluster
# Creates a local Kubernetes cluster using Minikube
# Use this command when starting fresh or after 'minikube delete'
create-minikube:
	@echo "Starting minikube cluster..."
	minikube start

# 2. Verify Minikube Status
# Checks if the Minikube cluster is running properly
# Useful for troubleshooting connection issues
check-minikube:
	@echo "Checking if minikube is running..."
	minikube status

# 3. Monitor Kubernetes Resources
# Shows the current state of pods and services
# Regular monitoring helps identify deployment issues
check-pods:
	@echo "Checking pods..."
	kubectl get pods
	@echo "Checking services..."
	kubectl get services

# 4. Deploy Application
# Applies the Kubernetes configuration from YAML
# Creates/Updates both Deployment and Service resources
deploy:
	@echo "Deploying the application with deployment and service configuration..."
	kubectl apply -f 001-simple-deploy-fastapi-app.yaml

# 5. Verify Deployment Status
# Comprehensive check of all deployed resources
# Use this after deployment to ensure everything is running
check-deployment:
	@echo "Checking the deployment..."
	kubectl get deployments
	@echo "---------------------"
	@echo "Checking the pods..."
	kubectl get pods
	@echo "---------------------"
	@echo "Checking the services..."
	kubectl get services

# 6. Access Application
# Creates a tunnel to access the application locally
# Maps container port 80 to local port 8080
port-forward:
	@echo "Port forwarding to access the application..."
	@echo "Access the application at http://localhost:8080"
	@echo "Press Ctrl+C to stop port forwarding."
	@echo "---------------------"
	kubectl port-forward svc/fastapi-todo-service 8080:80 -n python-fastapi