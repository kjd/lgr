import argparse
import sys

import idntables.tables


def load_table(filename):
	
	try:
		table = idntables.load(filename)
	except idntables.tables.InvalidIDNTable, e:
		print "Table Error: %s" % e
		sys.exit(2)
	
	return table


def table_list(tables, fh):
	
	for filename in tables:
		table = load_table(filename)
		
		for entry in table.entries():
			fh.write("%s\n" % (str(entry)))


def table_info(tables, fh):
	
	raise NotImplementedError


def table_validate(tables, fh, verbose=True):

	for filename in tables:
		try:
			table = idntables.load(filename, validate=True)
		except idntables.tables.XMLValidationError, e:
			if verbose:
				print "Table %s Error: %s" % (filename, e)
			sys.exit(2)
		if verbose:
			print "Table %s OK" % filename


def table_merge(tables, fh):
	
	merged_table = idntables.tables.IDNTable()
	for table in tables:
		merged_table += load_table(table)
	xml = merged_table.xml()
	fh.write(xml)


def table_diff(table1, table2, fh):
	
	raise NotImplementedError


def table_test(idn, tables, fh, verbose=True):

	success = True
	
	for filename in tables:
		table = load_table(filename)

		try:
			if table.contains(idn, exceptions=True):
				if verbose:
					print "Matches table %s" % filename
				sys.exit(0)
		except idntables.tables.InvalidDomain, e:
			success = False
			if verbose:
				print "Does not match table %s: %s" % (filename, e)
	
	if not success:
		sys.exit(2)
	sys.exit(0)


def table_variants(idn, table, fh, verbose=True):
	
	table = load_table(table)
	
	try:
		for variant in table.variants(idn):
			print variant.alabel
	except idntables.tables.InvalidDomain, e:
		if verbose:
			print e
		sys.exit(2)
		
	
	
def main(args=None):
	
	interactive = sys.stdout.isatty()
	
	parser = argparse.ArgumentParser(description="Perform operations on IDN Tables.")
	subparsers = parser.add_subparsers(help="function help", dest='action')
	
	subparser = subparsers.add_parser('list', help="list codepoints in a table as text")
	subparser.add_argument('table', nargs='+', help="table file")
	
	subparser = subparsers.add_parser('info', help="show table metadata as text")
	subparser.add_argument('table', nargs='+', help="table file")
	
	subparser = subparsers.add_parser('validate', help="validate if table is correctly formatted")
	subparser.add_argument('table', nargs='+', help="table file")

	subparser = subparsers.add_parser('diff', help="compare two tables and show the differences")
	subparser.add_argument('table1', help="first table file")
	subparser.add_argument('table2', help="second table file")
	
	subparser = subparsers.add_parser('merge', help="merge two more more tables into a single table")
	subparser.add_argument('table', nargs='+', help="table file")

	subparser = subparsers.add_parser('test', help="test is a string qualifies in a specific table")
	subparser.add_argument('idn', help="idn string to test")
	subparser.add_argument('table', nargs='+', help="table file")
	
	subparser = subparsers.add_parser('variants', help="generate list of variant strings from a table")
	subparser.add_argument('idn', help="idn string to test")
	subparser.add_argument('table', help="table file")
	
	parser.add_argument('-o', '--output', dest="output", help="send output to file")
	if interactive:
		parser.add_argument('-q', '--quiet', dest="quiet", action='store_true', help="suppress discretionary output to stdout")
		parser.add_argument('-v', '--verbose', dest="verbose", action='store_true', help="information output to stdout (default)")
	else:
		parser.add_argument('-q', '--quiet', dest="quiet", action='store_true', help="suppress discretionary output to stdout (default)")
		parser.add_argument('-v', '--verbose', dest="verbose", action='store_true', help="information output to stdout")
		
	args = parser.parse_args()
	
	if args.output:
		fh = open(args.output, 'wb')
	else:
		fh = sys.stdout
	
	verbose = interactive
	if args.quiet:
		verbose = False
	if args.verbose:
		verbose = True
		
	if args.action == 'list':
		table_list(args.table, fh)

	if args.action == 'info':
		table_info(args.table, fh)

	if args.action == 'validate':
		table_validate(args.table, fh, verbose=verbose)
		
	if args.action == 'diff':
		table_diff(args.table1, args.table2, fh)
		
	if args.action == 'merge':
		table_merge(args.table, fh)
		
	if args.action == 'test':
		table_test(args.idn, args.table, fh, verbose=verbose)
	
	if args.action == 'variants':
		table_variants(args.idn, args.table, fh, verbose=verbose)

if __name__ == '__main__':
	main()
