# Initialize

Assign security group
Assign fixed address - elastic IP

# Update

* Connect to server through PuTTY

* Update server 

```
cd /odoo/odoo-fhir
sudo git fetch origin
sudo git pull origin master
```
* Restart server
```
cd /odoo/odoo-server
sudo service odoo-server restart
```

* Login with browser

```
<IP Address that looks like 99.99.999.999>:8069
```
# Error: `remote: fatal error in commit_refs`

`sudo git gc`

if this does not work, try

```
sudo git fsck
sudo git gc
```

* Set up website with domain name

Ref: http://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-custom-domain-walkthrough.html

* Blog - [Amazon Route 53 – The AWS Domain Name Service](https://aws.amazon.com/blogs/aws/amazon-route-53-the-aws-domain-name-service/)
* Documentation - [Amazon Route 53 ](https://aws.amazon.com/route53/)
* Video - [Setting up AWS Route 53 DNS System ](https://www.youtube.com/watch?time_continue=246&v=olEz_cTqGWM)
Video - [AWS Knowledge Center Videos: "How do I move my domain that is hosted with another registrar to AWS?" ](https://www.youtube.com/watch?v=OxuqoqzjZYI#t=174.521)
Video - []()

1 Create DNS account in AWS
* Go to [Route 53](https://console.aws.amazon.com/route53/home?#)
* Go to **DNS Management - Hosted zones**
* Create **Hosted Zone**
- Domain Name (like fioresoft.com)
- Comment
* Create Record Set
- Type: A - IPv4 address (default)
- Value: Type `IPv4 address` of instance found in [EC2 Dashboard](https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#Instances:sort=instanceId) (eg, 52.26.227.152)

2 Point domain name to account
* Go to Domain Service like [GoDaddy](www.godaddy.com)
* Login
* Select **Domains** 
* Select **Manage DNS** for the domain (like foresoft.com)
* Edit **Type A** record
- Enter `IPv4 address` in **Points to** box
- Save

3 Test
* Wait an hour for the servers to update
* Test by typing the IPv4 address in your browser (like www.fioresoft.com)
* Success if page of IPv4 address appears
