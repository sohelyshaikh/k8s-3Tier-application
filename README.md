# k8s-3Tier-application
A 3Tier web application to demonstrate and deploy different resources of k8s.
*****

Steps to Follow:


Step1: Create cluster using eks_config.yaml


Step2: Create service account using eksctl.


Step3: Apply PVC, secrets, configmap.


Step4: Apply 'mysql.yaml' for MySQL deployment.


Step5: Exec into mysql, create db and table; insert few entries.



Step6: Apply 'service.yaml' to expose mysqldb.


Step7: Apply 'pod-frontend.yaml' to deploy frontend application.


Step8: Apply 'lb-service.yaml' to expose frontend application via loadbalancer.


Step9: Copy loadbalancer dns and add home to url <br>
--> [{url}/home], to land on homepage.<br>
--> [{url}/users], to display all users in db.


****
k8s ServiceAccount is mapped with <strong>IAM Role</strong> to access background image from private S3 bucket.<br>
Boto3 {python interface to AWS} is used to download image from S3 bucket .

