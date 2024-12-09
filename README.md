## Objective:

Summarize all steps to create a simple kubernetes deployment that runs a contianer with python code. The python code uses boto3 to write data (later a pytorch model) to s3.

We want all steps to be executed from the command line (if possible not use the console)

For the cluster creation checkout the EKS course on udemy. 

Furtermore, if we want to save the model to 3 we the pods needs permissions to access s3.

**remark** - in order to work with IAM on eks we must have an OIDC provider associated with the cluster.

### create a bucket `pytorch-svw`
The structure to create a bucket using the aws cli is :
```
aws s3 mb s3://<bucket-name> --region <region>
```

Below we create a bucket `pytorch-svw` in the `us-east-1` region.
```
aws s3 mb s3://pytorch-svw --region us-east-1
```

### create policy to write to S3

create a policy that allows to put objects in our bucket. See the file `s3-putobject-policy.json`.

```
aws iam create-policy --policy-name <PolicyName> --policy-document file://policy.json
```
```
aws iam create-policy --policy-name S3WritePolicy --policy-document file://s3-putobject-policy.json
```
This creates a policy with the name `S3WritePolicy` from our local policy document.
- create an IAM role for a service account. please note you need to fill in your `cluster-name` (here `eksdemo` is the name assumed for cluster)  and `account nr` below (can be taken from the aws console). 

### create a serviceaccount

Please note that this runs a cloudformation script.

```
eksctl create iamserviceaccount \
  --name s3-access-sa \
  --namespace default \
  --cluster <your-cluster-name> \
  --attach-policy-arn arn:aws:iam::<your-account-id>:policy/S3WritePolicy \
  --approve
```
Below we create a service account called `s3-access-sa` on our k8s cluster that refers to the `S3WritePolicy` created earlier. 
```
eksctl create iamserviceaccount \
  --name s3-access-sa \
  --namespace default \
  --cluster eksdemo1 \
  --attach-policy-arn arn:aws:iam::381492237900:policy/S3WritePolicy \
  --approve
```

Using kubectl we can see that it exists:

`k get sa`

for more details we can execute:

 `k describe sa s3-access-sa`.

we can see this service account refers to an IAM role that was created. If you go to the role you can see that our S3WritePolicy has been attached. 

ToDo -how do we do this with IAM directly?

### simple pod that writes directly to s3

The prerequisites have been met: a bucket was created and a service account with sufficient s3 IAM permissions was created.

Now a pod will be created that writes directly to s3. The manifest is located at `./manifest/s3-direct-write.yaml`.

This will just pull a simple container with the aws cli, creates a simple file and uploads this to our `pytorch-svw` bucket. 

### boto3 write to s3

Now a more complex case is covered. We have a python script `write_to_s3.py` will be containerized. It will use `boto3` and the aws cli was included to also do some simple checks when running commands from the container. See the `Dockerfile` for more details. 

`docker build -t longtong/boto3-writer .`

now push the image to docker hub. 

`docker push longtong/boto3-writer`

The `./manifest/s3-boto3-write.yaml` runs the container with the python script. When we create the job a file `boto3-test.txt` should appear in the `pytorch-svw` bucket.

`kubectl apply -f ./manifest/s3-boto3-write.yaml`

### pytorch write to s3

The last example is where a very simple pytorch model is trained and then saved to s3. An example job is defined in `manifest/s3-pytorch.yaml`. This has been setup as a job object. The intention is to run the training job once and then stop. 

`kubectl apply -f manifest/s3-pytorch`

This is a large image to download so it might take some time for the container to run. 

you can run

`kubectl get pods -w` track the status of the pod creation and then use `kubectl logs <pod-name> -f` to see the training in progress.
The `-f` allows live tracking of the logs. 





