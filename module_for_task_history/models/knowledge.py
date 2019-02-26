from odoo import api, fields, models
from odoo.tools.translate import _
import pytz
from datetime import datetime, timedelta

class Knowledge(models.Model):
    _name = 'dila.knowledge'

    name = fields.Char('Title', required=True)
    narration = fields.Text('Narration')
