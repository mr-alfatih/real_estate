from odoo import _, api, Command, fields, models
from odoo.exceptions import UserError

class CBTDocumentFolder(models.Model):
    _name = 'cbt.documents.folder'
    _description = 'Documents Workspace'
    _parent_name = 'parent_folder_id'
    _parent_store = True
    _rec_name = 'name'
    # _order = 'sequence, create_date DESC, id'


    @api.model
    def default_get(self, fields):
        res = super(CBTDocumentFolder, self).default_get(fields)
        if 'parent_folder_id' in fields and self._context.get('folder_id') and not res.get('parent_folder_id'):
            res['parent_folder_id'] = self._context.get('folder_id')

        return res

    @api.depends('parent_folder_id')
    @api.depends_context('hierarchical_naming')
    def _compute_display_name(self):
        hierarchical_naming = self.env.context.get('hierarchical_naming', True)
        for record in self:
            if hierarchical_naming and record.parent_folder_id:
                record.display_name = f"{record.parent_folder_id.sudo().name} / {record.name}"
            else:
                record.display_name = record.name

    active = fields.Boolean(string="Active", default=True)
    company_id = fields.Many2one('res.company', 'Company',
                                 help="This workspace will only be available to the selected company")
    parent_folder_id = fields.Many2one('cbt.documents.folder',
                                       string="Parent Workspace",
                                       ondelete="cascade",
                                       help="A workspace will inherit the tags of its parent workspace")
    parent_path = fields.Char(index=True, unaccent=False)
    name = fields.Char(required=True, translate=True)
    children_folder_ids = fields.One2many('cbt.documents.folder', 'parent_folder_id', string="Sub workspaces")