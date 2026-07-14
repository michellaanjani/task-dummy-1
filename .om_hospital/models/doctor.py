from odoo import api, fields, models, _

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Doctor"
    _rec_name = 'doctor_name'
    

    doctor_name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', required=True, tracking=True)
    gender = fields.Selection([
        ('male', '  Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', default='male', required=True, tracking=True)
    note = fields.Text(string='Description')
    image = fields.Binary(string='Doctor Image', copy=False)
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')
    active = fields.Boolean(string='Active', default=True)
    
    def copy(self, default=None):
            print("Successfully Copied")
            if default is None:
                default = {}
            if not default.get('doctor_name'):
                default['doctor_name'] = _("%s (Copy)", self.doctor_name)
            default['note'] = "Copied Record"
            return super(HospitalDoctor, self).copy(default)
        
    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', record.id)])
           