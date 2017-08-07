# Initialize

1 Create instance

* Go to [EC2 Instances Console](https://us-west-2.console.aws.amazon.com/ec2/v2/home)
* Select **Launch Instance**
* Choose an Amazon Machine Image (AMI) - Ubuntu Server
* Choose an Instance Type - t2.small
* Select **Review and Launch**, Select **Launch**
* Select an existing key pair - **Moxylus**
* Select **View Instances**


2 Assign security group

* Go to EC2 NETWORK & SECURITY>Security Groups
* Create Security Group
- Enter Security group name 
- Select **Inbound** and **Add Rule**: Type = SSH, Protocol = TCP, Port Range = 22, Source = 67.188.133.71/32
- Select **Inbound** and **Add Rule**: Type = HTTP, Protocol = TCP, Port Range = 80, Source = 0.0.0.0/0
- Select **Outbound** and enter: Type = All traffic, Protocol = All, Port Range = All, Destination = 0.0.0.0/0
* Assign Security Group
- Go to INSTANCES>Instances>Actons>Networking>Change Security Groups
- Select Security Group Name and click **Assign Security Groups**

3 Assign fixed address - elastic IP

* Go to EC2 NETWORK & SECURITY>Security Groups>Elastic IPs
* Create address
- Click **Allocate new address** to create a new address
* Alternatively, select a existing Elastic IP
- Go to Actions>Associated address
- Enter **Instance** and click **Associate**

# Install Odoo and Git

# Update

1 Connect to server through PuTTY

2 Update server 
```
cd /odoo/odoo-fhir
sudo git fetch origin
sudo git pull origin master
```
3 Restart server
```
cd /odoo/odoo-server
sudo service odoo-server restart
```

4 Login with browser

```
<IP Address that looks like 99.99.999.999>:8069
```
5 Troubleshooting

- Error: `remote: fatal error in commit_refs`

`sudo git gc`

- If this does not work, try

```
sudo git fsck
sudo git gc
```

# Set up website with domain name

## References

* [Overview](http://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-custom-domain-walkthrough.html)
* Blog - [Amazon Route 53 – The AWS Domain Name Service](https://aws.amazon.com/blogs/aws/amazon-route-53-the-aws-domain-name-service/)
* Documentation - [Amazon Route 53](https://aws.amazon.com/route53/)
* Video - [Setting up AWS Route 53 DNS System](https://www.youtube.com/watch?time_continue=246&v=olEz_cTqGWM)
* Video - [AWS Knowledge Center Videos: "How do I move my domain that is hosted with another registrar to AWS?"](https://www.youtube.com/watch?v=OxuqoqzjZYI#t=174.521)
* Video - [How to create DNS entries on AWS Route 53](https://www.youtube.com/watch?v=dNlibHYABLU)

## Procedure

1 Create DNS account in AWS
* Go to [Route 53](https://console.aws.amazon.com/route53/home?#)
* Go to **DNS Management - Hosted zones**
* Create **Hosted Zone**
- **Domain Name** (like fioresoft.com)
- **Comment** (like "FHIR on Odoo")
* Create **Record Set**
- Enter **Type**: `A - IPv4 address` (default)
- Enter **Value**: Type `IPv4 address` of instance found in [EC2 Dashboard](https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#Instances:sort=instanceId) (eg, 52.26.227.152)
- **Save Record Set**
* Create **Record Set**
- Enter **Name**: `www` **Type**: `A - IPv4 address` (default)
- Enter **Value**: Type `IPv4 address` of instance found in [EC2 Dashboard](https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#Instances:sort=instanceId) (eg, 52.26.227.152)
- **Save Record Set**

2 Point domain name to account
* Go to Domain Service like [GoDaddy](www.godaddy.com)
* Login
* Select **Domains** 
* Select **Manage DNS** for the domain (like foresoft.com)
* Edit **Type A** record
- Enter `IPv4 address` in **Points to** box
- Save

3 Install Apache

* Installation
```
sudo -i #Go to root
apt-get install apache2 # Install Apache Server
systemctl start apache2 # Start Apache Server
systemctl status apache2 # Check Apache Server status
netstat -l # Check network status. 
           # `tcp6	0	0	[::]:http  [::]:* LISTEN` means that the server is running
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8069 #Reroute from port 80 to port 8069
iptables -t nat -L # Check status
```
* Troubleshooting

- Find out if Odoo has errors
```
cd /var/log/odoo #Go to directory of Odoo Server Log
tail -n 20 odoo-server.log # Display last 20 lines of Odoo Server Log
```

4 Test
* Wait an hour for the servers to update
* Test by typing the IPv4 address in your browser (like www.fioresoft.com)
* Success if page of IPv4 address appears

# Set up a mail server

- [Request to Remove Email Sending Limitations](https://aws.amazon.com/forms/ec2-email-limit-rdns-request?catalog=true&isauthcode=true)
- [odoo 9 email configuration](https://youtu.be/lvOq86Sqh5Y)