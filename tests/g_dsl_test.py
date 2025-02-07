import sys
from os.path import dirname, abspath
import unittest

rootDir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, rootDir)

from tests.glossary_test import TestGlossaryBase
from pyglossary.glossary import Glossary


class TestGlossaryDSL(TestGlossaryBase):
	def __init__(self, *args, **kwargs):
		TestGlossaryBase.__init__(self, *args, **kwargs)

		self.dataFileCRC32.update({
			"100-RussianAmericanEnglish-ru-en.dsl": "c24491e0",
			"100-RussianAmericanEnglish-ru-en.txt": "e11e084e",
		})

	def convert_dsl_txt(self, fname, fname2, **convertArgs):
		self.convert(
			f"{fname}.dsl",
			f"{fname}-2.txt",
			compareText=f"{fname2}.txt",
			**convertArgs
		)

	def test_convert_dsl_txt_1(self):
		self.convert_dsl_txt(
			"100-RussianAmericanEnglish-ru-en",
			"100-RussianAmericanEnglish-ru-en",
		)
