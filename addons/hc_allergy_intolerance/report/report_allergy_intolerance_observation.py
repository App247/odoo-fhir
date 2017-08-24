from openerp import api, fields, models

class allergy_intolerance_observation(models.AbstractModel):
    _name = 'report.hc_allergy_intolerance.report_allergy_observation'

    @api.multi
    def get_manifestation(self, manifestation_ids):
        manifestation_list = ''
        for manifestation in manifestation_ids:
            if not manifestation_list:
                manifestation_list = manifestation.name
            else:
                manifestation_list = manifestation_list +', '+ manifestation.name
        return manifestation_list

    @api.multi
    def render_html(self, data):
        docs = self.env['hc.res.allergy.intolerance'].browse(self.id)
        data = docs.read([])[0]
        docargs = {'doc_ids': self._ids,
                   'doc_model': 'hc.res.allergy.intolerance',
                   'data': data,
                   'docs': docs,
                   'get_manifestation': self.get_manifestation,
                   }
        return self.env['report'].render('hc_allergy_intolerance.report_allergy_observation', docargs)
