###Study
* [New API Guidelines](http://odoo-new-api-guide-line.readthedocs.io/en/latest/index.html)

* Views: [odoo/openerp/addons/base/res/res_partner_view.xml](https://github.com/odoo/odoo/blob/9.0/openerp/addons/base/res/res_partner_view.xml)

* Fonts [Source](http://stackoverflow.com/questions/29701948/path-for-icon-used-in-smart-button)

  Odoo smart button uses http://fortawesome.github.io/Font-Awesome/

  It is a font icon more than a image defined inside a css class. But you can change whatever as you did in css image class.

  For simple idea about font awesome go through [this page](http://fortawesome.github.io/Font-Awesome/get-started/)

  For more information regarding odoo smart button look http://www.slideshare.net/openobject/odoo-smart-buttons

  This package is located in Odoo as a library in `addons/web/static/lib/fontawesome/fonts`

  Example: `fa-flask` icon and a simple example to use it, is available at http://fortawesome.github.io/Font-Awesome/icon/flask/

###CDA to FHIR

##CDA Sample
* [J Mandel @ GitHub](https://github.com/jmandel/sample_ccdas)
* [Amida Tech FHIR to CCDA](https://github.com/jmandel/sample_ccdas)
* [Amida Tech CCDA to FHIR](https://github.com/amida-tech/cda-fhir)
* [FHIR CDA Examples to FHIR](https://github.com/FHIR/cda-examples-to-fhir), Contacts: [Brett Esler](mailto:info@oridashi.com.au) @ [Oridashi](http://www.oridashi.com.au); Nikolay Ryzhikov <niquola@gmail.com>

##Applications

#Graham Grieve
* Mapping between CCDA and FHIR, [Blog](http://www.healthintersections.com.au/?p=2506)
* named org.hl7.fhir.dstu3.utils.StructureMapUtilities [Repo](https://github.com/hl7-fhir/fhir-svn)

#HAPI

  * HAPI (HL7 application programming interface; pronounced "happy") is an open-source, object-oriented parser for Java. [HAPI](http://hl7api.sourceforge.net/)
  * Contact: James Agnew, jamesagnew@gmail.com, University Health Network
  * [HAPI-FHIR](http://hapifhir.io/)
  * [HAPI Code](https://github.com/jamesagnew/hapi-fhir)
  * Test

	```
	http://fhirtest.uhn.ca/baseDstu3/Patient?_id=179986&_format=json
	http://fhirtest.uhn.ca/baseDstu3/Patient?_id=179986&_format=html
	http://fhirtest.uhn.ca/baseDstu3/Patient?_id=179986&_format=xml
	```
mirthconnect demo [Video](https://youtu.be/rktoj_nlsB8)

#CDA Shredder, Matt Spielman, Senior Product Manager, Healthshare, Intersystems [Video Presentation](http://www.intersystems.com/library/library-item/healthshare-cda-shredder-fhir-application-roundtable-presentation/)

#Fhirbase (data storage)
* Main contributors: Danil Kutkevich(danil@kutkevich.org), [URL](http://danil.kutkevich.org); Nikolay Ryzhikov <niquola@gmail.com>
* [Code @ GitHub](https://github.com/fhirbase/fhirbase-plv8)

#cda2fhir
* [cda2fhir](https://github.com/srdc/cda2fhir) is a Java library to transform HL7 CDA R2 instances to HL7 FHIR resources. 
* [SRDC Software](http://www.srdc.com.tr/en/)
