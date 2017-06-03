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
