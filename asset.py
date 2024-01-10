# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['Asset', 'AssetProofMethod']


class Asset(metaclass=PoolMeta):
    __name__ = 'asset'

    proof_methods = fields.Many2Many('asset-quality.proof.method', 'asset',
        'proof_method', 'Quality Proof Methods', states={
            'invisible': Eval('type', '') != 'quality_control_equipment',
            },
        help='The Quality Proof Methods that can be done with this equipment.')

    @classmethod
    def __setup__(cls):
        super(Asset, cls).__setup__()
        qc_equipment = (
            'quality_control_equipment',
            'Quality Control Equipment')
        if qc_equipment not in cls.type.selection:
            cls.type.selection.append(qc_equipment)

    @classmethod
    def delete(cls, assets):
        pool = Pool()
        Test = pool.get('quality.test')
        Template = pool.get('quality.template')

        to_check = [a for a in assets if a.type == 'quality_control_equipment']
        if to_check:
            n_test_lines = Test.search([
                    ('equipments', 'in', [a.id for a in to_check]),
                    ], count=True)
            if n_test_lines:
                raise UserError(gettext(
                    'asset_quality_control_equipment.msg_equipment_used_in_test',
                    test=", ".join([a.rec_name for a in to_check])))
            n_template_lines = Template.search([
                    ('equipments', 'in', [a.id for a in to_check]),
                    ], count=True)
            if n_template_lines:
                raise UserError(gettext(
                    'asset_quality_control_equipment.msg_equipment_used_in_template',
                    template=", ".join([a.rec_name for a in to_check])))
        super(Asset, cls).delete(assets)


class AssetProofMethod(ModelSQL):
    'Asset - Quality Proof Method'
    __name__ = 'asset-quality.proof.method'
    asset = fields.Many2One('asset', 'Asset', domain=[
            ('type', '=', 'quality_control_equipment'),
            ], ondelete='CASCADE', required=True)
    proof_method = fields.Many2One('quality.proof.method',
        'Quality Proof Method', ondelete='CASCADE', required=True)
