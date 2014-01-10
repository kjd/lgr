import argparse
import sys

import .rulesets as rulesets

def load_ruleset(filename):
	
	try:
		ruleset = lgr.load(filename)
	except lgr.rulesets.InvalidRuleset, e:
		print "Ruleset Error: %s" % e
		sys.exit(2)
	
	return ruleset


def ruleset_list(rulesets, fh):
	
	for filename in rulesets:
		ruleset = load_ruleset(filename)
		
		for entry in ruleset.entries():
			fh.write("%s\n" % (str(entry)))


def ruleset_info(rulesets, fh):
	
	raise NotImplementedError


def ruleset_validate(rulesets, fh, verbose=True):

	for filename in rulesets:
		try:
			ruleset = rulesets.load(filename, validate=True)
		except rulesets.XMLValidationError, e:
			if verbose:
				print "Ruleset %s Error: %s" % (filename, e)
			sys.exit(2)
		if verbose:
			print "Ruleset %s OK" % filename


def ruleset_merge(rulesets, fh):
	
	merged_ruleset = rulesets.Ruleset()
	for ruleset in rulesets:
		merged_ruleset += load_ruleset(ruleset)
	xml = merged_ruleset.xml()
	fh.write(xml)


def ruleset_diff(ruleset1, ruleset2, fh):
	
	raise NotImplementedError


def ruleset_test(idn, rulesets, fh, verbose=True):

	success = True
	
	for filename in rulesets:
		ruleset = load_ruleset(filename)

		try:
			if ruleset.contains(idn, exceptions=True):
				if verbose:
					print "Matches ruleset %s" % filename
				sys.exit(0)
		except rulesets.InvalidDomain, e:
			success = False
			if verbose:
				print "Does not match ruleset %s: %s" % (filename, e)
	
	if not success:
		sys.exit(2)
	sys.exit(0)


def ruleset_variants(idn, ruleset, fh, verbose=True):
	
	ruleset = load_ruleset(ruleset)
	
	try:
		for variant in ruleset.variants(idn):
			print variant.alabel
	except rulesets.InvalidDomain, e:
		if verbose:
			print e
		sys.exit(2)
		
	
	
def main(args=None):
	
	interactive = sys.stdout.isatty()
	
	parser = argparse.ArgumentParser(description="Perform operations on Label Generation Rulesets.")
	subparsers = parser.add_subparsers(help="function help", dest='action')
	
	subparser = subparsers.add_parser('list', help="list codepoints in a ruleset as text")
	subparser.add_argument('ruleset', nargs='+', help="lgr file")
	
	subparser = subparsers.add_parser('info', help="show ruleset metadata as text")
	subparser.add_argument('ruleset', nargs='+', help="lgr file")
	
	subparser = subparsers.add_parser('validate', help="validate if ruleset is correctly formatted")
	subparser.add_argument('ruleset', nargs='+', help="lgr file")

	subparser = subparsers.add_parser('diff', help="compare two rulesets and show the differences")
	subparser.add_argument('ruleset1', help="first lgr file")
	subparser.add_argument('ruleset2', help="second lgr file")
	
	subparser = subparsers.add_parser('merge', help="merge two more more rulesets into a single ruleset")
	subparser.add_argument('ruleset', nargs='+', help="lgr file")

	subparser = subparsers.add_parser('test', help="test is a string qualifies in a specific ruleset")
	subparser.add_argument('dstring', help="domain string to test")
	subparser.add_argument('ruleset', nargs='+', help="lgr file")
	
	subparser = subparsers.add_parser('variants', help="generate list of variant strings from a ruleset")
	subparser.add_argument('dstring', help="domain string to test")
	subparser.add_argument('ruleset', help="lgr file")
	
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
		ruleset_list(args.ruleset, fh)

	if args.action == 'info':
		ruleset_info(args.ruleset, fh)

	if args.action == 'validate':
		ruleset_validate(args.ruleset, fh, verbose=verbose)
		
	if args.action == 'diff':
		ruleset_diff(args.ruleset1, args.ruleset2, fh)
		
	if args.action == 'merge':
		ruleset_merge(args.ruleset, fh)
		
	if args.action == 'test':
		ruleset_test(args.dstring, args.ruleset, fh, verbose=verbose)
	
	if args.action == 'variants':
		ruleset_variants(args.dstring, args.ruleset, fh, verbose=verbose)

if __name__ == '__main__':
	main()
