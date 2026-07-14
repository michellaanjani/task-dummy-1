from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'reference'
    _order = 'doctor_id, age, name'
    # default adalah ascending, jika ingin descending tambahkan desc setelah fieldnya contoh 'doctor_id desc'

    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,default=lambda self: _('New'))
    state = fields.Selection([
    ('draft', 'Draft'),
    ('confirm', 'Confirmed'),
    ('done', 'Done'),
    ('cancel', 'Cancelled'), ],
    string='Status', default='draft', tracking=True)
    name = fields.Char(string='Name', related='patient_id.name', required=True, tracking=True)
    
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, tracking=True)
    patient_name_id = fields.Many2one('hospital.patient', string='Patient Name', required=False, tracking=True)
    
    age = fields.Integer(string='Age', related='patient_id.age', tracking=True)   
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    
    date_appointment = fields.Date(string='Appointment Date', default=fields.Datetime.now, tracking=True, required=True)
    date_checkup = fields.Datetime(string='Checkup Time', tracking=True)
    
    prescription = fields.Text(string='Prescription')
    prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id', string='Prescription Lines')
    
    def action_confirm(self):
        self.state = 'confirm'
        
    def action_done(self):
        self.state = 'done'
        
    def action_draft(self):
        self.state = 'draft'  
        
    def action_cancel(self):
        self.state = 'cancel'
        
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Appointment'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New') 
        result = super(HospitalAppointment, self).create(vals)
        return result
    
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.gender = ''
            self.note = ''  

    def unlink(self):
            print("Deleting the record")
            for record in self:
                if record.state == 'done':
                    raise ValidationError(_('You cannot delete %s as it is in Done state' %record.name))
            return super(HospitalAppointment, self).unlink()
        
    def action_url(self):
        test_name = 'tentang-kami'
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.hashmicro.com/id/%s' % (test_name),
            'target': 'new', #kalau self, bakal kebuka di tab yang sama. Kalau new, di tab baru
        }
        
    