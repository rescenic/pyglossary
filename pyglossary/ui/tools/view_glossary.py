#!/usr/bin/env python

import sys
import os
import signal
from subprocess import Popen, PIPE

from pyglossary import Glossary
from pyglossary.ui.tools.format_entry import formatEntry
from pyglossary.ui.tools.colors import *


Glossary.init()


def viewGlossary(filename, format=None):
	glos = Glossary(ui=None)

	if not glos.read(filename, format=format, direct=True):
		return

	proc = Popen(
		[
			"less",
			"-R",
		],
		stdin=PIPE,
	)
	index = 0

	def handleEntry(entry):
		nonlocal index
		str = (
			f"{yellow}#{index}{reset} " +
			formatEntry(entry) +
			"\n______________________________________________\n\n"
		)
		proc.stdin.write(str.encode("utf-8"))
		if (index + 1) % 50 == 0:
			sys.stdout.flush()
		index += 1

	try:
		for entry in glos:
			try:
				handleEntry(entry)
			except (BrokenPipeError, IOError):
				break
	except (BrokenPipeError, IOError):
		pass
	except Exception as e:
		print(e)
	finally:
		proc.communicate()
		# proc.wait()
		# proc.terminate()
		sys.stdin.flush()
		sys.stdout.flush()


def main():
	filename = sys.argv[1]
	format = None
	if len(sys.argv) > 2:
		format = sys.argv[2]
	viewGlossary(filename, format=format)


if __name__ == "__main__":
	main()
