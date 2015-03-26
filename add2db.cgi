#!/usr/bin/env perl
use strict;
use warnings;
#use CGI(':standard');
#use HTML::Template;
use Bio::Perl;
use Bio::DB::GenBank;
use Bio::SeqIO;
use Bio::Tools::OddCodes;
use DBI;
use Config::IniFiles;

#Grab selected stats
my @acc;
my @start;
my @stop;
my @descr;
open (REFINED, "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";

while(<REFINED>){
#gb|AAA85196.1|CNF1 [Escherichia coli]                           |75.9|7e-15|157|192
    if(/^(\D+)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(\d+)\|(\d+) *$/){
	push(@descr, $3);
	push(@acc, $2);
	push(@start, $6);
	push(@stop, $7);
    }
}
close REFINED;

my $dbe  = 'genbank';
my $i=0;

my $cfg = Config::IniFiles->new(-file=> "./data.ini");
my $db = $cfg->val('Database','DB');
my $host = $cfg->val('Host','loc');
my $user = $cfg->val('User','name');
my $pass = $cfg->val('Password','pw');

my $dsn = "DBI:mysql:database=".$db.";host=localhost";
my $dbh = DBI->connect($dsn, $user, $pass, { RaiseError => 1, PrintError => 1 });

#Reset database
my $sth = $dbh->prepare("DROP TABLE IF EXISTS hits");
$sth->execute();
$sth = $dbh->prepare("DROP TABLE IF EXISTS original");
$sth->execute();
$sth = $dbh->prepare("DROP TABLE IF EXISTS structural");
$sth->execute();
$sth = $dbh->prepare("DROP TABLE IF EXISTS functional");
$sth->execute();
$sth = $dbh->prepare("DROP TABLE IF EXISTS chemical");
$sth->execute();
$sth = $dbh->prepare("DROP TABLE IF EXISTS charge");
$sth->execute();
$sth = $dbh->prepare("DROP TABLE IF EXISTS hydrophobic");
$sth->execute();
$sth = $dbh->prepare("DROP TABLE IF EXISTS dayhoff");
$sth->execute();
$sth = $dbh->prepare("DROP TABLE IF EXISTS sneath");
$sth->execute();

#Create tables
$sth = $dbh->prepare("create table hits(
id integer not null primary key auto_increment,
accession varchar(20) not null,
description varchar(30) not null,
length int(10) not null,
keywords varchar(50) null,
species varchar(25) not null,
type varchar(10) null,
version int(5) null,
primary_id int(20) null,
num_of_features int(5) null,
start_pos int(5) not null, 
stop_pos int(5) not null
);");
$sth->execute();
$sth = $dbh->prepare("create table original(id integer not null primary key auto_increment, org_sequence text);");
$sth->execute();
$sth = $dbh->prepare("create table structural(id integer not null primary key auto_increment, str_sequence text);");
$sth->execute();
$sth = $dbh->prepare("create table chemical(id integer not null primary key auto_increment, che_sequence text);");
$sth->execute();
$sth = $dbh->prepare("create table functional(id integer not null primary key auto_increment, fun_sequence text);");
$sth->execute();
$sth = $dbh->prepare("create table charge(id integer not null primary key auto_increment, cha_sequence text);");
$sth->execute();
$sth = $dbh->prepare("create table hydrophobic(id integer not null primary key auto_increment, hyd_sequence text);");
$sth->execute();
$sth = $dbh->prepare("create table dayhoff(id integer not null primary key auto_increment, day_sequence text);");
$sth->execute();
$sth = $dbh->prepare("create table sneath(id integer not null primary key auto_increment, sne_sequence text);");
$sth->execute();

#Insert values into tables
foreach my $accession(@acc){
    my $seq = get_sequence( $dbe , $accession );
    my $feature_count = $seq -> feature_count;
    my $accession = $seq->accession_number;
    my $sequence  = $seq->seq;
    my $length = $seq->length;
#    my $description = $seq-> desc(); #incomplete description
    my $description = $descr[$i]; 
    my $keywords = $seq -> keywords;
    if($keywords eq ''){
	$keywords = 'none available';
    }
    my $species = $seq->species->binomial();
    my $alpha = $seq->alphabet;             # 'dna', 'rna', 'protein'
    my $version = $seq->seq_version;
    my $primary = $seq->primary_id;
    my $start ='';
    my $end = '';

#Oddcode object
    my $oddcode = Bio::Tools::OddCodes->new(-seq => $seq);

#Determine length of alignment for substr method
    my $start_pos = $start[$i]-1;
    my $stop_pos = $stop[$i];
    $i++;
    my $align_length = $stop_pos-$start_pos+1;
#Original sequence
    $sth = $dbh->prepare ("insert into original(id, org_sequence) values(?,?);");
    $sth->execute('null', $sequence);
    $sth->finish();

#Oddcode: Structural
    my $structural = ${$oddcode->structural};
    $structural = lowercase($structural, $start_pos, $align_length);
#Populate database
    $sth = $dbh->prepare ("insert into structural(id, str_sequence) values(?,?);");
    $sth->execute('null', $structural);
    $sth->finish();
#Oddcode: Chemical 
    my $chemical = ${$oddcode->chemical};
    $chemical = lowercase($chemical, $start_pos, $align_length);
    $sth = $dbh->prepare ("insert into chemical(id, che_sequence) values(?,?);");
    $sth->execute('null', $chemical);
    $sth->finish();
#Oddcode: Functional
    my $functional = ${$oddcode->functional};
    $functional = lowercase($functional, $start_pos, $align_length);
    $sth = $dbh->prepare ("insert into functional(id, fun_sequence) values(?,?);");
    $sth->execute('null', $functional);
    $sth->finish();
#Oddcode: Charge
    my $charge = ${$oddcode->charge};
    $charge = lowercase($charge, $start_pos, $align_length);
    $sth = $dbh->prepare ("insert into charge(id, cha_sequence) values(?,?);");
    $sth->execute('null', $charge);
    $sth->finish();
#Oddcode: Hydrophobic
    my $hydrophobic = ${$oddcode->hydrophobic};
    $hydrophobic = lowercase($hydrophobic, $start_pos, $align_length);
    $sth = $dbh->prepare ("insert into hydrophobic(id, hyd_sequence) values(?,?);");
    $sth->execute('null', $hydrophobic);
    $sth->finish();
#Oddcode: Dayhoff
    my $dayhoff = ${$oddcode->Dayhoff};
    $dayhoff = lowercase($dayhoff, $start_pos, $align_length);
    $sth = $dbh->prepare ("insert into dayhoff(id, day_sequence) values(?,?);");
    $sth->execute('null', $dayhoff);
    $sth->finish();
#Oddcode: Sneath
    my $sneath = ${$oddcode->Sneath};
    $sneath = lowercase($sneath, $start_pos, $align_length);
    $sth = $dbh->prepare ("insert into sneath(id, sne_sequence) values(?,?);");
    $sth->execute('null', $sneath);
    $sth->finish();

#Insert values for hits    
    $sth = $dbh->prepare( "insert into hits(id, accession, description, length, keywords, species, type, version, primary_id, num_of_features, start_pos, stop_pos) values(?,?,?,?,?,?,?,?,?,?,?,?)");
    $sth->execute('null', $accession, $description, $length, $keywords, $species, $alpha, $version, $primary, $feature_count, $start_pos, $stop_pos);
    $sth->finish();
}

$dbh->disconnect();

sub lowercase{
    my ($string, $start, $length) = (@_);
    my $substring = substr($string, $start, $length);
    my $lower = lc($substring);
    $string =~ s/$substring/$lower/g;
    return $string;
}
