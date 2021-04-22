# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest

from trytond.exceptions import UserError
from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
import trytond.tests.test_tryton
from trytond.exceptions import UserError
from trytond.modules.company.tests import create_company, set_company


class TestCase(ModuleTestCase):
    'Test module'
    module = 'asset_quality_control_equipment'

    @with_transaction()
    def test0010depends(self):
        'Test Asset.delete'
        pool = Pool()
        Asset = pool.get('asset')
        Model = pool.get('ir.model')
        QualityProof = pool.get('quality.proof')
        CualityConfiguration = pool.get('quality.configuration')
        QualityTemplate = pool.get('quality.template')
        QualitytTest = pool.get('quality.test')
        Sequence = pool.get('ir.sequence')
        Uom = pool.get('product.uom')

        # Create Company
        company = create_company()
        with set_company(company):

            # Create Asset
            asset, = Asset.create([{
                        'name': 'Asset',
                        }])

            # Create Equipments
            used_equipment, unused_equipment = Asset.create([{
                        'type': 'quality_control_equipment',
                        'name': 'Used Equipment',
                        }, {
                        'type': 'quality_control_equipment',
                        'name': 'Unused Equipment',
                        }])

            # Configure Quality Control
            sequence, = Sequence.search([('name', '=', 'Quality Control')])
            allowed_doc, = Model.search([('model', '=', 'asset')])
            CualityConfiguration.create([{
                        'allowed_documents': [('create', [{
                                            'quality_sequence': sequence.id,
                                            'document': allowed_doc.id,
                                            }])],
                        }])

            # Create Qualitative Proof
            qualitative_proof, = QualityProof.create([{
                        'name': 'Qualitative Proof',
                        'type': 'qualitative',
                        'methods': [('create', [{
                                            'name': 'Qualitative Method',
                                            'possible_values': [('create', [{
                                                            'name': 'Value 1',
                                                            }, {
                                                            'name': 'Value 2',
                                                            }])],
                                            'equipments': [('add', [
                                                        used_equipment.id,
                                                        unused_equipment.id,
                                                        ])]
                                            }])],
                        }])

            unit, = Uom.search([('name', '=', 'Unit')])

            # Create Quality Template
            quality_template, = QualityTemplate.create([{
                        'name': 'Template 1',
                        'internal_description': 'Internal description',
                        'external_description': 'External description',
                        'qualitative_lines': [('create', [{
                                        'name': 'Line 1',
                                        'proof': qualitative_proof.id,
                                        'method': (qualitative_proof.methods[0]
                                                .id),
                                        'valid_value': (qualitative_proof
                                            .methods[0].possible_values[0].id),
                                        }])],
                        'equipments': [('add', [used_equipment.id])],
                        }])

            # Create And assing template to Test
            test, = QualitytTest.create([{
                        'number': 'TEST/',
                        'document': str(asset),
                        'templates': [('add', [quality_template.id])],
                        }])
            test.apply_template_values()

            Asset.delete([unused_equipment])

            QualityTemplate.delete([quality_template])
            with self.assertRaises(UserError):
                Asset.delete([used_equipment])


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    return suite
