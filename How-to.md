# Odoo

## Ubuntu Desktop

* Set up VirtualBox

```sudo /etc/init.d/vboxadd setup```


* Enable clipboard

```sudo /usr/bin/VBoxClient --clipboard```

* Display the port on which openerp server is in running state.

```sudo ps aux | grep openerp```

* Kill specific process (id)


```sudo kill -9 id```

## Install Odoo in Ubuntu Desktop

* Go to Ubuntu directory where you want to install the software. For example: ```cd /opt```
* Place install script in the directory
```
Odoo 10 Community
sudo wget https://raw.githubusercontent.com/luigisison/moxylus/master/Odoo10Community/odoo_install.sh


Odoo 9 Enterprise
sudo wget https://raw.githubusercontent.com/luigisison/moxylus/master/Odoo9Enterprise/odoo-install.sh

Odoo 9 Community
sudo wget https://raw.githubusercontent.com/luigisison/moxylus/master/Odoo9Community/install-odoo9c.sh

Odoo 8
sudo wget https://raw.githubusercontent.com/luigisison/moxylus/master/Odoo8/odoo-install.sh
```

* (Optional) Edit the file to change parameters: ```sudo nano odoo-install.sh```
* Save changes and then make the file executable: ```sudo chmod +x odoo-install.sh```
* Execute the script to install Odoo: ```./odoo-install.sh```
* When prompted, enter your GitHub username and password to download the enterprise package.

## Update Odoo, Thank you, [Yenthe](http://www.odoo.yenthevg.com/update-odoo-environment-github/)

* Go to directory where Odoo is installed
```
cd /odoo/odoo-server

```
* Fetch latest Odoo version from GitHub
```
sudo git fetch origin 9.0
```
* Apply changes
```
sudo git reset --hard origin/9.0
```

* Update databases
```
sudo service odoo-server restart -u all -d FHIR-DEV
```
## Install Times Roman Font

* create **fonts** folder in `/usr/lib/python2.7/dist-packages/reportlab/`
```
cd /usr/lib/python2.7/dist-packages/reportlab/
sudo mkdir fonts

```

* download [pfbfer.zip](http://www.reportlab.com/ftp/fonts/pfbfer.zip) to download folder
* extract it
* Put all files in `/usr/lib/python2.7/dist-packages/reportlab/fonts/`

```
sudo mv _abi____.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/_abi____.pfb
sudo mv _ab_____.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/_ab_____.pfb
sudo mv _ai_____.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/_ai_____.pfb

sudo mv _a______.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/_a______.pfb
sudo mv cobo____.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/cobo____.pfb
sudo mv cob_____.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/cob_____.pfb
sudo mv com_____.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/com_____.pfb
sudo mv coo_____.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/coo_____.pfb
sudo mv _ebi____.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/_ebi____.pfb
sudo mv _eb_____.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/_eb_____.pfb
sudo mv _ei_____.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/_ei_____.pfb
sudo mv _er_____.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/_er_____.pfb
sudo mv sy______.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/sy______.pfb

sudo mv zd______.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/zd______.pfb
sudo mv zx______.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/zx______.pfb
sudo mv zy______.pfb /usr/lib/python2.7/dist-packages/reportlab/fonts/zy______.pfb
```
# Linux

## Cheatsheet

```
sudo mkdir mydir --create directory

sudo rm -rf mydir --delete directory
clear --clear the terminal screen
sudo touch /odoo/odoo-fhir/addons/hc_allergy_intolerance/views/hc_route_codes_views.xml --create file
sudo wget http://url -- download to current location
```
* Remember commands
```
sudo chown $USER:$USER $HOME/.bash_history
sudo chmod u+w $HOME/.bash_history
```

* Update GIT
```
sudo apt-get upgrade
sudo apt-get install git
sudo git --version
```

# GitHub


* Reference: [How to Install Git on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-14-04)
* Reference: [Git - Installng Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* Reference: [Ubuntu Server Guide](https://help.ubuntu.com/lts/serverguide/git.html)

## Setup - Do once

### Install Git dependencies
```
sudo apt-get install build-essential libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip
```


### Install Git
* [Check latest version](https://github.com/git/git/tree/master/Documentation)
```
cd /opt
sudo wget https://github.com/git/git/archive/v2.9.2.zip -O git.zip
sudo unzip git.zip
cd git-*
sudo make prefix=/usr/local install
```

### Register GitHub account
```
git config --list
git config --global user.name "Luigi Sison"
git config --global user.email lsison@moxylus.com
```

# Odoo Server

## Initial


### Initialize odoo-fhir with content from GitHub
```
cd /odoo
sudo git clone --depth 1 https://github.com/luigisison/odoo-fhir.git
```

### Setup addons directory /odoo/odoo-fhir/addons
```
sudo nano /etc/odoo-server.conf

addons_path=/odoo/odoo-server/openerp/addons,/odoo/odoo-server/addons,/odoo/odoo-fhir/addons,/odoo/odoo-server/addons/web_kanban
```
## Create database

* In browser, go to `http://localhost:8069/web/database/manager#action=database_manager`

```
cd /odoo/odoo-server
createdb FHIR-DEV
./odoo.py -d FHIR-DEV --addons-path /odoo/odoo-fhir/addons

```
## Install database GUI, pgAdminIII


`sudo apt-get install pgadmin3`

Run pgAdminIII

Change psql password

```psql

alter user <username> with password '<password>';

```
control-z

In pgadmin3, Add a connection (first icon in upper left corner)
```
Name: localhost
Host: localhost
Port: 5432 (already entered)
Service: leave blank
Maintenance DB: postgress (already entered)
Username: <username> (already entered)
Password: <password>
Password: odoo
```

## Do every time a change occurs

### Upload changes

```
cd /odoo/odoo-fhir
sudo git add .
sudo git status

sudo git commit -m "Initial Commit" -a
sudo git push origin master
```

### Update local repository 

When remote repository changes or when error "! [rejected] master -> master (fetch first) error" occurs

```

cd /odoo/odoo-fhir
sudo git fetch origin
sudo git pull origin master
```

## Update Changes

syntax: `./odoo.py -d <database> --addons-path <directories> -i <modules>**

```

cd /odoo/odoo-server
sudo service odoo-server stop
./odoo.py -d FHIR-DEV --addons-path /odoo/odoo-fhir/addons,/odoo/odoo-server/addons -u hc_base
```

## Ongoing

### Save terminal output to a file

* Start a ```script``` session and save output to ```output.txt``` in the current directory.

```
script output.txt
```

* End a script session
```
exit
```
## Error


### ERROR ? openerp.service.server: Failed to load server-wide module `web_kanban`
```
opt/openerp/server$ ./openerp-server --addons-path=web/addons
```

now you can assign multiple addons path,
```
opt/openerp/server$ ./openerp-server --addons-path=web/addons,../addons1,../addons2
```


## Synching fork with master

* Go to local repository (e.g., /odoo/odoo-fhir)
```
cd /odoo/odoo-fhir
```
* Add master repository to upstream and check if added
```
sudo git remote add upstream https://github.com/luigisison/odoo-fhir.git
sudo git remote -v

```
* Fetch master repository and then checkout local master
```
sudo git fetch upstream
sudo git checkout master
```
* Combine the changes from the master repository with your local one, then push the changes
```
sudo git merge upstream/master
sudo git push origin master

```

## Create Data Set

* Create model file `sudo nano /odoo/odoo-fhir/addons/hc_base/models/hc_participation_type.py`
* Add model file to `__openerp__.py/data` `'data/hc_vs_participation_type_type.xml',`
* Create view file `sudo nano /odoo/odoo-fhir/addons/hc_base/views/hc_participation_type_views.xml`

## Create Module


* Create scaffold
```
cd /odoo/odoo-server
./odoo.py scaffold hc_location addons
cd addons
sudo mv hc_location /odoo/odoo-fhir/addons/hc_location

```
* Rename files
```

cd /odoo/odoo-fhir/addons/hc_location
sudo mv models/models.py models/hc_res_location.py
sudo mv views/views.xml views/hc_res_location_views.xml
sudo mv views/templates.xml views/hc_res_location_templates.xml
```
* Modify manifest files
```
#models/__init__.py
from . import hc_res_location


#hc_location/__openerp__.py
'name': "Location"
'summary': """
'description': """
        **Scope and Usage**
        
        * Bullet
"""
'author': "Luigi Sison",
'website': "https://hl7-fhir.github.io/location.html",

'category': 'Health Care',
'depends': ['hc_base'],
'data': [
        'security/ir.model.access.csv',
        'views/hc_res_location_views.xml',
        'views/hc_res_location_templates.xml',
],
# only loaded in demonstration mode
'demo': [

'demo/demo.xml',
],
    'installable': 'True',
    'auto-install': 'True',
}
```
## Create module icons
```
sudo mkdir /odoo/odoo-fhir/addons/hc_healthcare_service/static
sudo mkdir /odoo/odoo-fhir/addons/hc_healthcare_service/static/description
sudo mv /home/odoo/Downloads/healthcare_service.png /odoo/odoo-fhir/addons/hc_healthcare_service/static/description/icon.png

```
* Add ```web_icon``` to view
```
    menuitem id="hc_allergy_intolerance.menu_allergy" 
      name="Allergy Intolerances"
      web_icon="hc_healthcare_service,static/description/icon.png"
``` 

## Create demo data

* Create sample data in Odoo
* Export file to ```/home/odoo/Downloads```

* Transfer file to demo directory ```/odoo/odoo-fhir/addons/hc_base/demo/```

```
sudo mv /home/odoo/Downloads/hc.human.name.csv /odoo/odoo-fhir/addons/hc_base/demo/hc.human.name.csv
sudo mv /home/odoo/Downloads/hc.human.name.term.csv /odoo/odoo-fhir/addons/hc_base/demo/hc.human.name.term.csv
sudo mv /home/odoo/Downloads/hc.res.person.csv /odoo/odoo-fhir/addons/hc_base/demo/hc.res.person.csv
```
## Create data

* Base Module
```
sudo mv /home/odoo/Downloads/hc.human.name.suffix.csv /odoo/odoo-fhir/addons/hc_base/data/hc.human.name.suffix.csv
```
### Odoo Coding Guidelines

* [Odoo Guidelines](https://www.odoo.com/documentation/9.0/reference/guidelines.html)
* [OCA Guidelines](https://github.com/OCA/maintainer-tools/blob/master/CONTRIBUTING.mdo)

## Views

### [How to Adjust Column Widths in Tree Views](http://107.167.187.43/index.php/topics/view/view-column-widths)

* Create CSS definition file `yourmodule.css` in `yourmodule/static/src/css/yourmodule.css`. For example,
```
sudo mkdir /odoo/odoo-fhir/addons/hc_medication/static
sudo mkdir /odoo/odoo-fhir/addons/hc_medication/static/src
sudo mkdir /odoo/odoo-fhir/addons/hc_medication/static/src/css

sudo touch /odoo/odoo-fhir/addons/hc_medication/static/src/css/hc_medication.css
```
* Create CSS definition in `yourmodule.css`. For example,
```
.code_name { 
  width: 80%; 
}
```
* Add CSS class in `<div>` definition. For example,
```
<div class="code_name">
...
</div>
```

* Add to `css: []` part of `__openerp__.py`. For example, in `/odoo-fhir/addons/hc_medication/__openerp__.py`,
```
'css': [
        'static/src/css/hc_medication.css',
    ],
```

# Install custom modules

Clone module

Transfer

```
sudo mv <module> /odoo/custom/addons
```
Restart

In Odoo, 
* Activate Developer Mode
* Update Module List in ```Apps>Update Apps List```
* Locate installed app
* Install

# Display schema in database

```
psql FHIR-DEV
\d hc_res_allergy_intolerance
```
ctrl-z to quit

# Editing Tools

* [Remove trailing spaces in Python code](http://www.mefancy.com/addremove/remove-leading-text.php)
* [Remove/replace non ASCII characters](http://utils.paranoiaworks.org/diacriticsremover/) to fix `UnicodeWarning: Unicode unequal comparison failed to convert both arguments to Unicode - interpreting them as being unequalif cols[k][key] != vals[key]`

# Optimize server

* Watch: [Live Webinar- Intro to Customizing Odoo](https://youtu.be/E9u_Dpu2X1k)
* [Tune PostgreSQL](http://pgtune.leopard.in.ua)
* [Performance Tips](https://www.odoo.com/slides/slide/performance-tips-tricks-399)

#Sublime Text How To

* Find and Replace special characters
  
  - Enable regex in the find panel. Then use **\t** for tabs, **\r** for carriage returns, **\n** for newlines.