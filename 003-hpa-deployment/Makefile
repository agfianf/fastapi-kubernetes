# 1. Start minikube
01-start-minikube:
	minikube start

02-list-profile-minikube:
	minikube profile list

03-set-profile-to-demo-cluster:
	@echo "Creating a new minikube cluster..."
	minikube start -p demo-cluster
	@echo "Minikube cluster started."
	kubectx demo-cluster
	minikube profile list
	
04-set-namespace-to-demo:
	kubectl get ns
	kubens demo
	kubectl config view --minify --output 'jsonpath={..namespace}'


# 2. installation of metrics server
05-check-metrics-server:
	kubectl get pods -n kube-system | grep metrics
	kubectl top nodes

# if not installed, run the following command
06-install:
	@echo "Installing metrics server..."
	@echo "This may take a few seconds..."
	@echo "---------------------"
	minikube addons list
	minikube addons enable metrics-server
	sleep 15
	kubectl get pods -n kube-system | grep metrics
	kubectl top nodes

# do this if 06-install fails
06.1-install-metrics-server:
	kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml


# spec > template > spec > containers > args. Add:
# - --kubelet-insecure-tls
# wait 10-20 seconds and check the metrics server
06.2-edit-container-metrics:
	kubectl -n kube-system edit deployment metrics-server


# deployment ------
07-deploy:
	kubectl apply -f 003-deployment.yaml
	kubectl apply -f 003-hpa-deploy-fastapi-app.yaml

08-deploy-hpa:
	kubectl apply -f 003-hpa-deploy-fastapi-app.yaml

check:
	@echo "Checking the deployment..."
	kubectl get pods -owide
	@echo "---------------------"
	kubectl get hpa -owide
	@echo "---------------------"
	kubectl get services -owide
	@echo "---------------------"
	kubectl top pod
	@echo "---------------------"
	kubectl top nodes

09-watch-pods:
	watch -n 1 kubectl get pods

09.1-watch-hpa:
	watch -n 1 kubectl get hpa

09.2-watch-top-pods:
	watch -n 1 kubectl top pod


#! open new terminal and run this command 
10-tunnel:
	@echo "Tunneling to access the application..."
	@echo "Access the application at http://localhost:8123"
	@echo "Press Ctrl+C to stop tunneling."
	@echo "---------------------"
	minikube profile demo-cluster
	minikube tunnel -c

#! open new terminal and run this command 
# this one can but not scale, because it is not a load balancer
10.1-port-forward:
	@echo "Port forwarding to access the application..."
	@echo "Access the application at http://localhost:8080"
	@echo "Press Ctrl+C to stop port forwarding."
	@echo "---------------------"
	kubectl port-forward svc/fastapi-todo-service 8123:80 -n demo


#! open new terminal and run this command 
11-curl-service:
	while true; \
		do curl -s http://localhost:8123/system/hostname; \
		echo ""; \
		sleep 0.33; \
	done

12-curl-for-load:
	while true; \
		do curl -X 'GET' 'http://localhost:8123/performance/memory'; \
		echo ""; \
		sleep 0.02; \
	done

13-run-locust:
	@echo "Running Locust..."
	uv run locust -f locustfile.py \
	--host http://localhost:8123 \
	--users 50 \
	--spawn-rate 10 \
	--run-time 2m \
	--headless

14-stop-deploy:
	@echo "Stopping the application..."
	kubectl delete -f 003-hpa-deploy-fastapi-app.yaml
	kubectl delete -f 003-deployment.yaml
	@echo "Application stopped."

15-stop:
	minikube stop -p demo-cluster
	@echo "Minikube stopped."

log-metrics:
	kubectl logs -f deployment.apps/metrics-server -n kube-system