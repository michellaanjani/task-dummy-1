from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'reference desc'
    # _rec_name = 'reference'
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,default=lambda self: _('New'))
    state = fields.Selection([
    ('draft', 'Draft'),
    ('confirm', 'Confirmed'),
    ('done', 'Done'),
    ('cancel', 'Cancelled'), ],
    string='Status', default='draft', tracking=True)
    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', required=True, tracking=True)   
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description')
    responsible_id = fields.Many2one('res.partner', string='Responsible')
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')
    image = fields.Binary(string='PatientImage')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    active = fields.Boolean(string='Active', default=True)
    
    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', record.id)])
    
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
            vals['note'] = 'New Patient'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New') 
        result = super(HospitalPatient, self).create(vals)
        return result
    
    @api.model
    def default_get(self, fields):
        result = super(HospitalPatient, self).default_get(fields)
        print("value result", result)
        result['gender'] = 'female'
        return result
    
    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(_('Name %s Already Exists' %rec.name))
    
    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(_('Age cannot be zero'))
            
    def name_get(self):
        result = []
        print("context is", self.env.context)
        for rec in self:
            if self.env.context.get('hide_code'):
                name = rec.name
            else:
                name = '[' + rec.reference + '] ' + rec.name 
            result.append((rec.id, name))
        return result
    
    def action_open_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'target': 'current',
        }