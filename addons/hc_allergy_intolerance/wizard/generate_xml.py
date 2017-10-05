# -*- coding: utf-8 -*-

from openerp import api, fields, models
import base64, tempfile

class generate_xml(models.TransientModel):
    _name = "generate.xml"

    name = fields.Char('Name')
    xml_file = fields.Binary('XML File', readonly=True)

    @api.model
    def default_generate(self):
        context = dict(self._context) or {}
        tgz_xml_filename = tempfile.mktemp('.' + "xml")
        xml_file = False
        xml_data = ""
        parent_id = self.env['hc.res.allergy.intolerance'].browse(context.get('intolerance_id'))

        # Format suffixes
        suffix_str = False
        for suffix in parent_id.recorder_practitioner_id.person_id.name_id.suffix_ids:
            if not suffix_str:
                suffix_str = suffix.name
            else:
                suffix_str = suffix_str + ',' + suffix.name

        try:
            xml_file = open(tgz_xml_filename, "wr")
            xml_data = '''
                <author>
                    <templateId root="2.16.840.1.113883.10.20.22.4.119" />
                    <time value="201308011235-0800" />
                    <assignedAuthor>
                        <id root="%s" />
                        <code
                            code="%s"
                            codeSystem="2.16.840.1.113883.5.53"
                            codeSystemName="Health Care Provider Taxonomy"
                            displayName="%s" />
                        <assignedPerson>
                            <name>
                                <given>%s</given>
                                <family>%s</family>
                                <suffix>%s</suffix>
                            </name>
                        </assignedPerson>
                </author>
            '''%(parent_id.id,
                 parent_id.recorder_practitioner_id.specialty_id.code,
                 parent_id.recorder_practitioner_id.specialty_id.name,
                 parent_id.recorder_practitioner_id.person_id.name_id.first_id.name,
                 parent_id.recorder_practitioner_id.person_id.name_id.surname_id.name,
                 suffix_str)

            xml_file.write(xml_data)
        finally:
            xml_file.close()
        file = open(tgz_xml_filename, "rb")
        out = file.read()
        file.close()
        return {'name': tgz_xml_filename, 'xml_file': base64.b64encode(out)}
