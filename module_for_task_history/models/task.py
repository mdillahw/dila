from odoo import api, fields, models
from odoo.tools.translate import _
import pytz
from datetime import datetime, timedelta

class Task(models.Model):
    _inherit = 'project.task'

    day_todo = fields.Integer(string="Day Todo", default=1)
    #module_id = fields.Many2one('dila.module','Module Name (Folder)')

    module_ids = fields.One2many('dila.module.revisi','task_id','List Of Module Todo')

class ModuleName(models.Model):
    _name = 'dila.module'

    name = fields.Char(string="Module Name (folder)")
    module_name = fields.Char(string="Module Name (at Odoo)")
    list_version = fields.One2many('dila.module.revisi','module_id', 'List Version', order="id desc")
    last_version = fields.Char(string="Last Version", compute="last_v")
    last_desc = fields.Char(string="Last Change", compute="last_v")

    @api.multi
    def last_v(self):
        for rec in self:
            last = self.env['dila.module.revisi'].search([('module_id','=',rec.id)],limit=1, order='id desc')
            if last:
                rec.last_version = last.name
                rec.last_desc = last.description
            else:
                rec.last_version = "1.0.0"
                rec.last_desc = ''

    def mengcopy(self):
        tz = pytz.utc
        if self.env.user.tz:
            tz = pytz.timezone(self.env.user.tz)

        strdata = "===============================================================================\n"
        strdata +='Module Name (folder) : ' + self.name + '\n'
        strdata +='Module Name (at Odoo) : ' + self.module_name + '\n'
        strdata +='Version : ' + self.last_version + '\n'
        last = self.env['dila.module.revisi'].search([('module_id','=',self.id)],limit=1, order='id desc')
        if last:
            start_todo = pytz.utc.localize(datetime.strptime(last.start_todo, "%Y-%m-%d %H:%M:%S")).astimezone(tz)
            strdata +='Start Todo : ' + str(start_todo) + '\n'
            date_release = pytz.utc.localize(datetime.strptime(last.date_release, "%Y-%m-%d %H:%M:%S")).astimezone(tz)
            strdata +='Date Release : ' + str(date_release) + '\n'
            strdata +='Description : ' + last.description + '\n'
        strdata += "===============================================================================\n"
        #import pyperclip
        #pyperclip.copy(strdata)
        #import os 
        #os.system("echo '%s' | clipboard" % strdata)
    



class Revisi(models.Model):
    _name = 'dila.module.revisi'

    name = fields.Char(string="Version", required=True)
    start_todo = fields.Datetime('Start Todo')
    date_release = fields.Datetime('Date Release')
    description = fields.Text(string="Description", compute="get_desc")
    module_id = fields.Many2one('dila.module','Module Name', required=True)
    task_id = fields.Many2one('project.task','Task ID')
    desc_ids = fields.One2many('dila.module.revisi.list','revisi_id','Desc Todo')


    @api.multi
    def get_desc(self):
        for rec in self:
            str_desc = ''
            i = 0
            for ln in rec.desc_ids:
                i += 1
                str_desc += str(i) +'. '+ ln.name + ("\n" if not ln.reason else (ln.reason + '\n'))
            rec.description = str_desc

    def open_list_todo(self):
        self.ensure_one()
        view = self.env.ref('module_for_task_history.dila_list_revisi_view')

        result = {
            'name': _('List Todo'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'dila.module.revisi',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
        }
        return result

    @api.multi
    def save(self):
        return True

    _sql_constraints = [('name_uniq', 'unique(name, module_id)', _('Versi ini sudah pernah digunakan'))]    

class Revisi_list(models.Model):
    _name = 'dila.module.revisi.list'

    revisi_id = fields.Many2one('dila.module.revisi')
    name = fields.Char(string="Description", required=True)
    reason = fields.Char(string="Reason")

