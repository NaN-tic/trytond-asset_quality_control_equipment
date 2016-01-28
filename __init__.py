# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .asset import *
from .quality_control import *


def register():
    Pool.register(
        Asset,
        AssetProofMethod,
        ProofMethod,
        EquipmentTemplate,
        Template,
        EquipmentTest,
        Test,
        module='asset_quality_control_equipment', type_='model')
