# FastAPI Todo Demo with Minikube, HPA, and Metrics Server

This project demonstrates how to deploy a FastAPI application on a local Kubernetes cluster using Minikube, with Horizontal Pod Autoscaler (HPA) based on memory usage. The setup includes a metrics server for resource monitoring and a LoadBalancer service for easy access.

## Prerequisites

- **Basic knowledge**: You should already understand Pods, ReplicaSets, and Docker images.
- **Installed tools**:  
  - [Minikube](https://minikube.sigs.k8s.io/docs/)
  - [kubectl](https://kubernetes.io/docs/tasks/tools/)
  - [kubectx & kubens](https://github.com/ahmetb/kubectx) (optional, for easier context/namespace switching)
  - [make](https://www.gnu.org/software/make/)

## Quick Start

## 1. Start Minikube

```sh
make 01-start-minikube
```


**Check available profiles:**

```sh
make 02-list-profile-minikube
```

**Create and switch to a new profile for this demo:**
```sh
make 03-set-profile-to-demo-cluster
```

**Set namespace to demo (make sure it exists):**

```sh
make 04-set-namespace-to-demo
```

## 2. Install Metrics Server

Check if metrics server is running:

```sh
make 05-check-metrics-server

```

**Enable metrics server addon:**
```sh
make 06-install
```

**If the above fails, install manually:**
```
make 06.1-install-metrics-server
```

If you see errors about TLS, edit the deployment and add --kubelet-insecure-tls to the container args:
```sh
make 06.2-edit-container-metrics
```

```bash
      labels:
        k8s-app: metrics-server
    spec:
      containers:
      - args:
        - --cert-dir=/tmp
        - --secure-port=10250
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --kubelet-insecure-tls # add this line
        - --metric-resolution=15s
```

Wait 10-20 seconds, then check metrics again.

## 3. Deploy the Application

Apply the deployment and HPA manifests:
```
make 07-deploy
```

**Check the status:**
```bash
make check
```
You should see pods running, HPA status, and the service.

## 4. Access the Application

**Recommended (LoadBalancer, supports scaling):**

Open a new terminal and run:
```sh
make 10-tunnel
```

- Access the app at http://localhost:8123.

**Alternative Tunnel** (Port-forward, not scalable):
```bash
make 10.1-port-forward
```

Access the app at http://localhost:8123.

## 5. Test the Service

In a new terminal, run:
```
make 11-curl-service
```

You should see output like:
```bash
...
{"hostname":"fastapi-todo-demo-app-79676b9549-fzr6p","platform":"Linux","version":"hpa-v22"}
{"hostname":"fastapi-todo-demo-app-79676b9549-b9l5r","platform":"Linux","version":"hpa-v22"}
...
```

If you see different hostnames, it means your requests are being load balanced across pods.

## 6. Stop Everything
```sh
make 12-stop
```
# FAQ & Troubleshooting

**Q: Why do I need minikube tunnel?**
> A: Minikube's LoadBalancer services need a tunnel to expose services on your localhost. Keep the tunnel terminal open.

**Q: Why does kubectl top nodes or kubectl top pods not work?**
> A: Metrics server may not be running or needs the --kubelet-insecure-tls flag. See step 2 above.

**Q: Why is the service's EXTERNAL-IP <pending>?**
> A: This is normal in Minikube. Use minikube tunnel to get a working external IP (localhost).

**Q: Why does port-forwarding not scale?**
> A: kubectl port-forward only forwards to one pod, so you can't test load balancing or HPA scaling.

**Q: How do I trigger HPA scaling?**
> A: Generate enough load (e.g., with a looped curl or a load testing tool) so memory usage exceeds the HPA threshold.

**Q: What if the demo namespace does not exist?**
> A: Create it with kubectl create ns demo.

# Files Overview

- `Makefile`: Automation for all steps.
- `003-deployment.yaml`: FastAPI app Deployment and LoadBalancer Service.
- `003-hpa-deploy-fastapi-app.yaml`: HPA configuration for the deployment.

# Warnings
Do not close the terminal running minikube tunnel or your service will become inaccessible.
If you edit the metrics server deployment, make sure to add --kubelet-insecure-tls under spec.template.spec.containers.args.
Resource limits: The demo app is set with low CPU/memory limits for local testing. Adjust as needed for real workloads.

# Useful Commands
List all pods, HPAs, and services:
```sh
kubectl get pods -owide
kubectl get hpa -owide
kubectl get services -owide
```
View logs:
```sh
kubectl logs -l app.kubernetes.io/name=fastapi-todo-demo-app
```

Delete all resources:
```sh
make 12-stop
```

# Next Steps
Try changing the HPA target utilization or resource limits and see how scaling behavior changes.
Deploy your own FastAPI app by changing the image in 003-deployment.yaml.

Happy hacking!