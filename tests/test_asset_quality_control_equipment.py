# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import doctest
import unittest

from trytond.exceptions import UserError
import trytond.tests.test_tryton
from trytond.tests.test_tryton import (POOL, DB_NAME, USER, CONTEXT, test_view,
    test_depends)
from trytond.transaction import Transaction


class TestCase(unittest.TestCase):
    'Test module'

    def setUp(self):
        trytond.tests.test_tryton.install_module(
            'asset_quality_control_equipment')
        self.asset = POOL.get('asset')
        self.company = POOL.get('company.company')
        self.model = POOL.get('ir.model')
        self.proof = POOL.get('quality.proof')
        self.proof_method = POOL.get('quality.proof.method')
        self.qualitative_value = POOL.get('quality.qualitative.value')
        self.qualitative_template_line = POOL.get(
            'quality.qualitative.template.line')
        self.quantitative_template_line = POOL.get(
            'quality.quantitative.template.line')
        self.quality_configuration = POOL.get('quality.configuration')
        self.quality_configuration_line = POOL.get(
            'quality.configuration.line')
        self.template = POOL.get('quality.template')
        self.test = POOL.get('quality.test')
        self.sequence = POOL.get('ir.sequence')
        self.uom = POOL.get('product.uom')
        self.user = POOL.get('res.user')

    def test0005views(self):
        'Test views'
        test_view('asset_quality_control_equipment')

    def test0006depends(self):
        'Test depends'
        test_depends()

    def test0010depends(self):
        'Test Asset.delete'
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            company, = self.company.search([
                    ('rec_name', '=', 'Dunder Mifflin'),
                    ])
            self.user.write([self.user(USER)], {
                'main_company': company.id,
                'company': company.id,
                })

            quality_test_sequence, = self.sequence.search([
                    ('code', '=', 'quality.test'),
                    ])
            asset_model, = self.model.search([('model', '=', 'asset')])

            configuration = self.quality_configuration()
            configuration.allowed_documents = []
            config_line = self.quality_configuration_line()
            configuration.allowed_documents.append(config_line)
            config_line.company = company
            config_line.quality_sequence = quality_test_sequence
            config_line.document = asset_model
            configuration.save()

            other_asset = self.asset(name='Asset')
            other_asset.save()

            used_equipment = self.asset(type='quality_control_equipment')
            used_equipment.name = 'Used Equipment'
            used_equipment.save()

            unused_equipment = self.asset(type='quality_control_equipment')
            unused_equipment.name = 'Unused Equipment'
            unused_equipment.save()

            qualitative_proof = self.proof(type='qualitative')
            qualitative_proof.company = company
            qualitative_proof.name = 'Qualitative Proof'
            qualitative_proof.methods = []
            qualitative_proof_method = self.proof_method(
                name='Qualitative Method')
            qualitative_proof.methods.append(qualitative_proof_method)
            qualitative_proof_method.possible_values = []
            val1 = self.qualitative_value(name='Value 1')
            qualitative_proof_method.possible_values.append(val1)
            val2 = self.qualitative_value(name='Value 2')
            qualitative_proof_method.possible_values.append(val2)
            qualitative_proof_method.equipments = []
            qualitative_proof_method.equipments.append(used_equipment)
            qualitative_proof_method.equipments.append(unused_equipment)
            qualitative_proof.save()

            quantitative_proof = self.proof(type='quantitative')
            quantitative_proof.company = company
            quantitative_proof.name = 'Quantitative Proof'
            quantitative_proof.methods = []
            quantitative_proof_method = self.proof_method(
                name='Quantitative Method')
            quantitative_proof.methods.append(quantitative_proof_method)
            quantitative_proof_method.equipments = []
            quantitative_proof_method.equipments.append(used_equipment)
            quantitative_proof_method.equipments.append(unused_equipment)
            quantitative_proof.save()

            unit, = self.uom.search([('name', '=', 'Unit')])

            template = self.template()
            template.company = company
            template.name = 'Template 1'
            template.qualitative_lines = []
            qualitative_tmpl_line = self.qualitative_template_line()
            template.qualitative_lines.append(qualitative_tmpl_line)
            qualitative_tmpl_line.name = 'Line 1'
            qualitative_tmpl_line.proof = qualitative_proof
            qualitative_tmpl_line.method = qualitative_proof.methods[0]
            qualitative_tmpl_line.valid_value = (
                qualitative_proof.methods[0].possible_values[0])
            template.equipments = [used_equipment]
            template.save()

            test = self.test()
            test.company = company
            test.name = 'TEST/'
            test.document = other_asset
            test.template = template
            test.save()
            self.test.set_template([test])

            self.asset.delete([unused_equipment])

            self.assertRaises(UserError, self.asset.delete, [used_equipment])

            self.test.delete([test])
            self.assertRaises(UserError, self.asset.delete, [used_equipment])

            self.template.delete([template])
            self.asset.delete([used_equipment])


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite and not isinstance(test, doctest.DocTestCase):
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    return suite
