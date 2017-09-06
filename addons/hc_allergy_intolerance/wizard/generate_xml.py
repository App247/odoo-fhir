# -*- coding: utf-8 -*-

from openerp import api, fields, models
import base64, tempfile

class generate_xml(models.TransientModel):
    _name = "generate.xml"

    name = fields.Char('Name')
    xml_file = fields.Binary('XML File', readonly=True)

    @api.model
    def default_generate(self):
        tgz_xml_filename = tempfile.mktemp('.' + "xml")
        xml_file = False
        xml_foramt = ""
        try:
            xml_file = open(tgz_xml_filename, "wr")
            xml_data = '''
        <record model="ir.ui.view" id="view_generate_xml_wizard_form">
            <field name="name">generate.xml.form</field>
            <field name="model">generate.xml</field>
            <field name="arch" type="xml">
                <form string="XML File" version="9.0">
                    <group>
                        <field name="name" invisible="1"/>
                        <field name="xml_file"/>
                    </group>
                    <footer>
                        <button string="Cancel" class="btn-default" special="cancel"/>
                    </footer>
                </form>
            </field>
        </record>
            '''
            xml_file.write(xml_data)
        finally:
            xml_file.close()
        file = open(tgz_xml_filename, "rb")
        out = file.read()
        file.close()
        return {'name': tgz_xml_filename, 'xml_file': base64.b64encode(out)}
