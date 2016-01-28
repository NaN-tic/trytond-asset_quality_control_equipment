# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['ProofMethod', 'EquipmentTemplate', 'Template', 'EquipmentTest',
    'Test']
__metaclass__ = PoolMeta


class ProofMethod:
    __name__ = 'quality.proof.method'
    equipments = fields.Many2Many('asset-quality.proof.method',
        'proof_method', 'asset', 'Equipments', domain=[
            ('type', '=', 'quality_control_equipment'),
            ],
        help='The Equipments that can be used to do this proof.')


class EquipmentTemplate(ModelSQL):
    'Equipment - Quality Template'
    __name__ = 'asset-quality.template'

    equipment = fields.Many2One('asset', 'Equipment', required=True,
        select=True, ondelete='CASCADE')
    template = fields.Many2One('quality.template', 'Template', required=True,
        select=True, ondelete='CASCADE')


class Template:
    __name__ = 'quality.template'
    equipments = fields.Many2Many('asset-quality.template', 'template',
        'equipment', 'Equipments',
        domain=[
            ('type', '=', 'quality_control_equipment'),
            ('proof_methods', 'in', Eval('methods', [])),
            ],
        depends=['methods'])
    methods = fields.Function(fields.One2Many('quality.proof.method', None,
            'Proof Methods'), 'on_change_with_methods')

    @fields.depends('quantitative_lines', 'qualitative_lines')
    def on_change_with_methods(self, name=None):
        methods = set([])
        for line in self.quantitative_lines + self.qualitative_lines:
            if line.method:
                methods.add(line.method.id)
        return list(methods)


class EquipmentTest(ModelSQL):
    'Equipment - Quality Test'
    __name__ = 'asset-quality.test'

    equipment = fields.Many2One('asset', 'Equipment', required=True,
        select=True, ondelete='CASCADE')
    test = fields.Many2One('quality.test', 'Test', required=True,
        select=True, ondelete='CASCADE')


class Test:
    __name__ = 'quality.test'
    equipments = fields.Many2Many('asset-quality.test', 'test', 'equipment',
        'Equipments',
        domain=[
            ('type', '=', 'quality_control_equipment'),
            ('proof_methods', 'in', Eval('methods', [])),
            ],
        depends=['methods'])
    methods = fields.Function(fields.One2Many('quality.proof.method', None,
            'Proof Methods'), 'on_change_with_methods')

    @fields.depends('quantitative_lines', 'qualitative_lines')
    def on_change_with_methods(self, name=None):
        methods = set([])
        for line in self.quantitative_lines + self.qualitative_lines:
            if line.method:
                methods.add(line.method.id)
        return list(methods)

    def set_template_vals(self):
        super(Test, self).set_template_vals()
        self.equipments = self.template.equipments
