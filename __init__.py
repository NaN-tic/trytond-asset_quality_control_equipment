# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import asset
from . import quality_control


def register():
    Pool.register(
        asset.Asset,
        asset.AssetProofMethod,
        quality_control.ProofMethod,
        quality_control.EquipmentTemplate,
        quality_control.Template,
        quality_control.EquipmentTest,
        quality_control.Test,
        module='asset_quality_control_equipment', type_='model')
