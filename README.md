# Deploying Your Portfolio Website on a Virtual Machine on GCP with a Custom Domain

This guide provides the steps to deploy your portfolio website on a VM instance on Google Cloud Platform (GCP) with a custom domain.
Click [HERE](https://dgutierrezengineer.com) to check the website.

## Step 0: Create your VM on Compute Engine, your custom domain on Google Domains and DNS records on Cloud DNS

1. There is a free tier VM option available on GCP, follow the required settings.
2. Create a domain from Google Domains
3. Go to Cloud DNS and create DNS records

Add or update the A records as follows:
- Host: @ (or leave blank, depending on the registrar)
- Type: A
- Value: Your GCE instance's external IP address
- TTL: Default or 3600 seconds
Add or update the A records for the www subdomain:
- Host: www
- Type: A
- Value: Your GCE instance's external IP address
- TTL: Default or 3600 seconds

Verify DNS Propagation:

After updating your DNS records, it may take some time for the changes to propagate. You can check the status of your DNS records using a tool like [DNS Checker](https://dnschecker.org/).

## Step 1: Set Up Your Environment

SSH into your VM:
- Click on SSH in Compute Engine or use the command below:
```bash
gcloud compute ssh your-vm-instance-name
```
Update the package list to ensure you have the latest information on the newest versions of packages and their dependencies:
```bash
sudo apt-get update
```
Install pip, the package installer for Python 3. The VM already had python3:
```bash
sudo apt install python3-pip
```
Clone your portfolio repository from GitHub:
```bash
git clone https://github.com/dieegogutierrez/Portfolio.git
```
Add the local bin directory to the PATH environment variable to ensure all installed packages can be executed:
```bash
echo 'export PATH=$PATH:/home/dieego_gutierrez/.local/bin' >> ~/.bashrc
```
Source the .bashrc file to apply the changes made to the PATH environment variable:
```bash
source ~/.bashrc
```
Change directory to the cloned repository:
```bash
cd Portfolio/
```
Install the required Python packages as specified in the requirements.txt file:
```bash
pip3 install -r requirements.txt
```
Install Nginx, a web server that will be used to serve your application:
```bash
sudo apt install nginx
```

## Step 2: Configure Gunicorn

Create a Gunicorn systemd service file:
```bash
sudo nano /etc/systemd/system/portfolio.service
```
Add the following content, change it accordingly:
```makefile
[Unit]
Description=gunicorn daemon for portfolio
After=network.target

[Service]
User=dieego_gutierrez
Group=www-data
WorkingDirectory=/home/dieego_gutierrez/Portfolio
ExecStart=/home/dieego_gutierrez/.local/bin/gunicorn --workers 3 --bind unix:/home/dieego_gutierrez/Portfolio/portfolio.sock run:app

[Install]
WantedBy=multi-user.target
```
Start and enable the Gunicorn service:
```bash
sudo systemctl start portfolio
sudo systemctl enable portfolio
```

## Step 3: Configure Nginx

Remove the default configuration:
```bash
sudo rm /etc/nginx/sites-enabled/default
```
Create a new Nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/portfolio
```
Add the following content, change it accordingly:
```bash
server {
    listen 80;
    server_name dgutierrezengineer.com www.dgutierrezengineer.com;

    location / {
        proxy_pass http://unix:/home/dieego_gutierrez/Portfolio/portfolio.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Enable the configuration:
```bash
sudo ln -s /etc/nginx/sites-available/yourprojectname /etc/nginx/sites-enabled
```
Test and reload Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

## Step 4: Enable HTTPS with Certbot

Install Certbot and the Nginx plugin:
```bash
sudo apt install certbot python3-certbot-nginx
```
Obtain the SSL certificate:
```bash
sudo certbot --nginx -d dgutierrezengineer.com -d www.dgutierrezengineer.com
```

## Step 5: Verify Your Deployment

Check the status of Gunicorn and Nginx:
```bash
sudo systemctl status portfolio
sudo systemctl status nginx
```

## Step 6: Continuos Deployment

[DOCUMENTATION](https://cloud.google.com/build/docs/automating-builds/github/connect-repo-github#console)

Enable Cloud Build API and Secret Manager API.

On Cloud Build Repositories 2nd gen create a new host connection.

Link your repository.

Create a trigger.
Adapt the code below and create a cloudbuild.yml or use the inline option while creating the trigger.
```yml
steps:
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['compute', 'ssh', 'your-vm-instance-name', '--command', 'cd /home/your_username/Portfolio && git pull origin main && sudo systemctl restart portfolio']
options:
  logging: CLOUD_LOGGING_ONLY
```