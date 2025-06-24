```bash
0. Install Kubernetes and Set Up a Local Cluster

Objective: Learn how to set up and use Kubernetes locally.

Instructions:

    Write a script, kurbeScript that:
        Starts a Kubernetes cluster on your machine
        verifies that the cluster is running using kubectl cluster-info.
        Retrieves the available pods

    Ensure minikube is installed

Repo:

    GitHub repository: alx-backend-python
    Directory: messaging_app
    File: messaging_app/kurbeScript

```

```bash
    1. Deploy the Django Messaging App on Kubernetes


    Objective: Deploy your containerized Django app on Kubernetes.

    Instructions:

        Create a deployment.yaml YAML file for your Django messaging app.

        Define the Docker image to be used for the app in the deployment.yaml file.

        Expose the Django app via a Service (use a ClusterIP service to keep it internal).

        Apply the Deployment using kubectl apply -f deployment.yaml.

        Verify that the app is running by checking the pods and logs (kubectl get pods, kubectl logs <pod-name>).

    Repo:

        GitHub repository: alx-backend-python
        Directory: messaging_app
        File: messaging_app/deployment.yaml

    # Commands

    # 1. Creates config map for env variables
    kubectl create configmap django-env --from-env-file=.env

    # 2. Secure passwords and secrets
    kubectl create secret generic mysql-secret \
    --from-literal=MYSQL_PASSWORD=somesecret \
    --from-literal=MYSQL_ROOT_PASSWORD=root_password

    # 3. Deploy to k8s
    kubectl apply -f deployment.yaml
```

```bash
    2. Scale the Django App Using Kubernetes

    Objective: Learn how to scale applications in Kubernetes.

    Instructions:

        Write a script kubctl-0x01 if run achieves the following:
        Use kubectl scale to increase the number of replicas to 3 of your Django app deployment.
        Verify that multiple pods are running by using kubectl get pods.
        Perform load testing on your app using wrk to see how the scaled app handles traffic
        Monitors Resource Usage using kubectl top

    Repo:

        GitHub repository: alx-backend-python
        Directory: messaging_app
        File: messaging_app/kubctl-0x01
```

```bash
3. Set Up Kubernetes Ingress for External Access

Objective: Expose your Django app to the internet using an Ingress controller.

Instructions:

    Install an Nginx Ingress controller in your cluster .

    Create an Ingress resource (ingress.yaml) to route traffic to your Django app’s service.

    Configure domain names or paths in the Ingress resource for different services (e.g., /api/ for the Django API).

    In commands.txt file write the command you used to apply the Ingress configuration

Repo:

    GitHub repository: alx-backend-python
    Directory: messaging_app
    File: ingress.yaml,commands.txt


# Make the app accessible with
echo "$(minikube ip) messaging-app.local" | sudo tee -a /etc/hosts

# Access the app with
http://messaging-app.local/api/
```

```bash
4. Implement a Blue-Green Deployment Strategy

Objective: Learn how to perform zero-downtime deployments.

Instructions:
    Set up a blue-green deployment strategy in Kubernetes where you deploy a new version of the Django app (green_deployment.yaml) alongside the current version: (rename the deployment.yaml file to blue_deployment.yaml). hint

    Create Kubernetes Services kubeservice.yaml to switch traffic from the blue version to the green version gradually.

    Write a script,kubctl-0x02 with that uses kubectl apply to deploy the blue and green version, and uses kubectl logs to check for errors in the new version

Repo:
    GitHub repository: alx-backend-python
    Directory: messaging_app
    File: green_deployment.yaml,blue_deployment.yaml,kubeservice.yaml,kubctl-0x02
```

```bash
5. Applying rolling updates

Objective: Update the application without downtime

Instructions:

    Modify the docker image version to 2.0 in the now blue_deployment.yaml

    Write a bash script kubctl-0x03 that:
        Applies the updated deployment file and triggers a rolling update
        Monitors the update progress using kubectl rollout status
        Uses curl to test if the app experiences any downtime or disruption by continuously sending requests
        Verify the Rolling Update is Complete by checking the current pods

    Run your script

Repo:

    GitHub repository: alx-backend-python
    Directory: messaging_app
    File: messaging_app/blue_deployment.yaml, kubctl-0x03


```
