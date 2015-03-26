#!/usr/bin/env perl
=d
Write selected items to file
=cut
use strict;
use warnings;
use CGI ':standard';

my $cgi = new CGI;
my $database = $cgi->param('myDatabase');
my $accession = $cgi->param('myAccession');
my $description = $cgi->param('myDescription');
my $score = $cgi->param('myScore');
my $evalue = $cgi->param('myEvalue');
my $start = $cgi->param('myStart');
my $stop = $cgi->param('myStop');

open (SELECTED, ">>", "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";
print SELECTED "$database|$accession|$description|$score|$evalue|$start|$stop\n";
close SELECTED;

exit;
