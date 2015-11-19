# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['ProofMethod', 'QualitativeTemplateLine',
    'QuantitativeTemplateLine', 'QualitativeTestLine', 'QuantitativeTestLine']
__metaclass__ = PoolMeta


class ProofMethod:
    __name__ = 'quality.proof.method'
    equipments = fields.Many2Many('asset-quality.proof.method',
        'proof_method', 'asset', 'Equipments', domain=[
            ('type', '=', 'quality_control_equipment'),
            ],
        help='The Equipments that can be used to do this proof.')


class QualitativeTemplateLine:
    __name__ = 'quality.qualitative.template.line'
    equipment = fields.Many2One('asset', 'Equipment', domain=[
            ('type', '=', 'quality_control_equipment'),
            ('proof_methods', 'in', [Eval('method', -1)]),
            ], depends=['method'])


class QuantitativeTemplateLine:
    __name__ = 'quality.quantitative.template.line'
    equipment = fields.Many2One('asset', 'Equipment', domain=[
            ('type', '=', 'quality_control_equipment'),
            ('proof_methods', 'in', [Eval('method', -1)]),
            ], depends=['method'])


class QualitativeTestLine:
    __name__ = 'quality.qualitative.test.line'
    equipment = fields.Many2One('asset', 'Equipment', domain=[
            ('type', '=', 'quality_control_equipment'),
            ('proof_methods', 'in', [Eval('method', -1)]),
            ], depends=['method'])


class QuantitativeTestLine:
    __name__ = 'quality.quantitative.test.line'
    equipment = fields.Many2One('asset', 'Equipment', domain=[
            ('type', '=', 'quality_control_equipment'),
            ('proof_methods', 'in', [Eval('method', -1)]),
            ], depends=['method'])
