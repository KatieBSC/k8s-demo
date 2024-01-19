# k8s-demo

## Description

This project contains examples of a Kubernetes job which writes an output
to a volume.

These examples aim to provide an introduction to a common use case for Kubernetes Jobs
and tips for getting started with Helm. See also [Useful Helm commands](#useful-helm-commands).

- [`k8s`](./k8s): Contains examples to create a PersistentVolume, PersistentVolumeClaim, Job, Pod that uses your PersistentVolumeClaim as a volume
- [`helm`](./helm): Contains examples to create a Helm chart for a job

## Prerequistes

- Install [minikube](https://minikube.sigs.k8s.io/docs/start/), tested with v1.32.0
- Install [Helm](https://helm.sh/docs/intro/install/), tested with v3.14.0
- Optionally install [helm-diff](https://github.com/databus23/helm-diff)

Check installation:
```
which minikube
```

```
which helm
```

## Create storage

The following command will create a PersistentVolume and PersistentVolumeClaim:
```
kubectl apply -f k8s/volume.yaml
```

```
persistentvolume/kt-volume created
persistentvolumeclaim/kt-pvc created
```

For more information, check out the [Kubernetes docs](https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/) on configuring persistent volume storage.

## Run Job with kubectl

The following will run a Kubernetes job which writes to the volume that was previously created:
```
kubectl apply -f k8s/job.yaml
```

Check it out:
```
kubectl get job
```

Clean up:
```
kubectl delete job kt-job
```

## Check out the file

We can use a task pod which uses the PersistentVolumeClaim as a volume.
```
kubectl apply -f k8s/task_pv_pod.yaml
```

Get a shell to the container running in the pod:
```
kubectl exec -it task-pv-pod -- /bin/bash
```

Check out the file that the job wrote:
```
cat mnt/data/demo_file.txt
```

Copy the file that was created:
```
kubectl cp task-pv-pod:/mnt/data/demo_file.txt demo_file.txt
```

Clean up:
```
kubectl delete pod task-pv-pod
```

## Run Job with Helm

We can also use Helm to run the same job. This will make our job easier to customize,
such as changing the environment variables, container image, and other job specs.

Install / upgrade `job-demo` Helm chart with default values:
```
helm upgrade job-demo helm/job_demo/ -i
```

Alternatively, install / upgrade `job-demo` Helm chart overriding values from the command line:
```
helm upgrade --set env.filename=new_file.txt job-demo helm/job_demo/ -i
```

Check out the job that got created:
```
kubectl describe job job-demo
```

Clean up the job:
```
kubectl delete job job-demo
```

To check out the file that updated / created, see [Check out the file](#check-out-the-file).


## Useful Helm commands

Below are a few commands that are helpful for working with Helm charts.


Render chart template and display the output:
```
helm template helm/job_demo/ 
```

Check the chart for possible issues:
```
helm lint helm/job_demo/ 
```

Dry-run chart install / upgrade to check computed values:
```
helm upgrade job-demo helm/job_demo/ -i --dry-run --debug 
```

List releases:
```
helm list
```

```
NAME    	NAMESPACE	REVISION	STATUS  	CHART
job-demo	default  	2       	deployed	job-demo-0.1.0	      
```

Check out everything that was installed with the Helm release:
```
helm get manifest job-demo
```

Check out the history of a Helm release:
```
helm history job-demo
```

Show what changed in two revisions (requires installing helm-diff):
```
helm diff revision job-demo 1 2
```
