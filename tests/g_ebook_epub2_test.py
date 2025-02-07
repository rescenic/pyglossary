import sys
from os.path import dirname, abspath
import unittest
import re

rootDir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, rootDir)

from tests.glossary_test import TestGlossaryBase
from pyglossary.glossary import Glossary


class TestGlossaryEPUB2(TestGlossaryBase):
	def __init__(self, *args, **kwargs):
		TestGlossaryBase.__init__(self, *args, **kwargs)

		self.dataFileCRC32.update({
			"100-en-fa-res.slob": "0216d006",
			"100-en-fa-res-slob.epub": "30506767",
			"100-en-fa-prefix3.epub": "af8ee89d",
			"300-rand-en-fa-prefix3.epub": "c0308c97",
		})

	def remove_toc_uid(self, data):
		return re.sub(
			b'<meta name="dtb:uid" content="[0-9a-f]{32}" />',
			b'<meta name="dtb:uid" content="" />',
			data,
		)

	def remove_content_extra(self, data):
		data = re.sub(
			b'<dc:identifier id="uid" opf:scheme="uuid">[0-9a-f]{32}</dc:identifier>',
			b'<dc:identifier id="uid" opf:scheme="uuid"></dc:identifier>',
			data,
		)
		data = re.sub(
			b'<dc:date opf:event="creation">[0-9-]{10}</dc:date>',
			b'<dc:date opf:event="creation"></dc:date>',
			data,
		)
		return data

	def convert_to_epub(
		self,
		inputFname,
		outputFname,
		testId,
		**convertArgs
	):
		inputFilename = self.downloadFile(f"{inputFname}")
		outputFilename = self.newTempFilePath(
			f"{inputFname.replace('.', '_')}-{testId}.epub"
		)

		expectedFilename = self.downloadFile(f"{outputFname}.epub")
		glos = self.glos = Glossary()
		res = glos.convert(
			inputFilename=inputFilename,
			outputFilename=outputFilename,
			**convertArgs
		)
		self.assertEqual(outputFilename, res)

		self.compareZipFiles(
			outputFilename,
			expectedFilename,
			{
				"OEBPS/toc.ncx": self.remove_toc_uid,
				"OEBPS/content.opf": self.remove_content_extra,
			},
		)

	def test_convert_to_epub_1(self):
		self.convert_to_epub(
			"100-en-fa-res.slob",
			"100-en-fa-res-slob",
			"1",
		)

	def test_convert_to_epub_2(self):
		for sort in (True, False):
			self.convert_to_epub(
				"100-en-fa-res.slob",
				"100-en-fa-res-slob",
				"2",
				sort=sort,
			)

	def test_convert_to_epub_3(self):
		for sqlite in (True, False):
			self.convert_to_epub(
				"100-en-fa-res.slob",
				"100-en-fa-res-slob",
				"3",
				sqlite=sqlite,
			)

	def test_convert_to_epub_4(self):
		for direct in (True, False):
			self.convert_to_epub(
				"100-en-fa-res.slob",
				"100-en-fa-res-slob",
				"4",
				direct=direct,
			)

	def test_convert_to_epub_5(self):
		for sqlite in (True, False):
			self.convert_to_epub(
				"100-en-fa.txt",
				"100-en-fa-prefix3",
				"5",
				sqlite=sqlite,
				writeOptions={"group_by_prefix_length": 3},
			)

	def test_convert_to_epub_6(self):
		self.convert_to_epub(
			"300-rand-en-fa.txt",
			"300-rand-en-fa-prefix3",
			"6",
			sqlite=True,
			writeOptions={"group_by_prefix_length": 3},
		)

	def test_convert_to_epub_7(self):
		self.convert_to_epub(
			"300-rand-en-fa.txt",
			"300-rand-en-fa-prefix3",
			"7",
			sqlite=False,
			writeOptions={"group_by_prefix_length": 3},
		)


if __name__ == "__main__":
	unittest.main()
