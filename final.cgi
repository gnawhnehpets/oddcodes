#!/usr/bin/env perl
use strict;
use warnings;
use Bio::Tools::Run::RemoteBlast;
use Bio::Root::Exception;
use Error qw(:try);
use CGI ':standard';
#use CGI::Carp qw/fatalsToBrowser/;
use finalpackage('parse');
use JSON;
use IO::Handle;
STDOUT->autoflush(1);
STDERR->autoflush(1);

#create our CGI and TMPL objects
my $cgi = new CGI;
my $json = JSON->new->allow_nonref;

###JSON-HTML
my $query = $cgi-> param('search_term');

###TESTING
#my $query = 'tattggggcagcggcgcggg';
#my $query = 'LLLKNYYISSALYLYKNGELDEREYNFSMNALNRSD';
chomp($query);

open (FASTA, ">", "/var/www/shwang26/final/input.fasta") || die "Could not open: $!";
print FASTA ">input_fasta\n".$query."\n";
close FASTA;

#Determine which program to run depending on sequence composition
my $db ='';
if($query =~ /^[AGCT]+$/i){
    $db = 'blastn'
}elsif($query =~ /^[GAVLIMFWPSTCYNQDEKRH]+$/i){
    $db = 'blastp';
}else{
}

#Create remoteblast object
my $factory = Bio::Tools::Run::RemoteBlast->new( -prog       => $db ,
                                                 -data       => 'nr' ,
                                                 -expect     => '100' ,
                                                 -readmethod => 'SearchIO' );

#Create SeqIO object
my $str = Bio::SeqIO->new( -file    => 'input.fasta' ,
                           -format  => 'fasta'   );

#Submit to BLAST
while( my $seq = $str->next_seq() ) {
    $factory->submit_blast( $seq );
    sleep 5;
}

#Save results to file
while( my @rids = $factory->each_rid ) {
    foreach my $rid ( @rids ) {
	my $result = $factory->retrieve_blast( $rid );
	if( ref( $result )) {
	    my $output   = $result->next_result();
	    my $filename = $output->query_name().".blastoutput";
	    $factory->save_output( $filename );
	    $factory->remove_rid( $rid );
	}elsif( $result < 0 ) {
	    # some error occurred
	    $factory->remove_rid( $rid );
	}else {
	    sleep 5;
	}
    }
}

#Parse results for key terms
my($first, $second, $third, $fourth, $fifth, $sixth, $seventh) = parse();
my @db = @$first;
my @acc = @$second;
my @desc = @$third;
my @score = @$fourth;
my @evalue = @$fifth;
my @start = @$sixth;
my @stop = @$seventh;
my $count = scalar(@db);

#array_ref to store hash refs href
my $matches=[];

#Store parsed results as hashref in arrayref
for(my $i=0; $i < scalar(@db); $i++){
    my $href = {};
    $href->{'database'}=$db[$i];
    $href->{'accession'}=$acc[$i];
    $href->{'description'}=$desc[$i];
    $href->{'score'}=$score[$i];
    $href->{'evalue'}=$evalue[$i];
    $href->{'start'}=$start[$i];
    $href->{'stop'}=$stop[$i];
    push(@$matches, $href);
}
print $cgi->header('application/json');
print $json->encode(
    { match_count => $count, matches => $matches, program => $db }
    );

