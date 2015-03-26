#!/usr/bin/env perl
use strict;
use warnings;
use CGI ':standard';
use DBI;
use Config::IniFiles;
use JSON;
my $json = JSON->new->allow_nonref;
my $cgi = new CGI;
#HTML FORM
my $acc = $cgi->param('db_term');
my $cfg = Config::IniFiles->new(-file=> "/var/www/shwang26/final/data.ini");
my $db = $cfg->val('Database','DB');
my $host = $cfg->val('Host','loc');
my $user = $cfg->val('User','name');
my $pass = $cfg->val('Password','pw');
my $dsn = "DBI:mysql:database=".$db.";host=localhost";
my $dbh = DBI->connect($dsn, $user, $pass, { RaiseError => 1, PrintError => 1 });

#Query
my $qry = qq{
SELECT h.accession, h.description, h.length, h.keywords, h.species, h.start_pos, h.stop_pos, o.org_sequence, s.str_sequence, c.che_sequence, f.fun_sequence, ch.cha_sequence, hy.hyd_sequence, d.day_sequence, sn.sne_sequence
FROM hits h, original o, structural s, chemical c, functional f, charge ch, hydrophobic hy, dayhoff d, sneath sn
WHERE h.id=o.id
AND o.id=s.id
AND s.id=c.id
AND c.id=f.id
AND f.id=ch.id
AND ch.id=hy.id
AND hy.id=d.id
AND d.id=sn.id
AND sn.id=h.id
AND h.description like ?;
};
my $sth = $dbh->prepare($qry);
$sth->execute("%$acc%");

my @data;
my @id;
my @accession;
my @description;
my @length;
my @keywords;
my @species;
my @start_pos;
my @stop_pos;
my @original;
my @structural;
my @chemical;
my @functional;
my @charge;
my @hydrophobic;
my @dayhoff;
my @sneath;
my $counter=0;

#Fetch results of query
while ( my $row = $sth->fetchrow_hashref ) {
    $id[$counter]=$$row{id};
    $accession[$counter]=$$row{accession};
    $description[$counter]=$$row{description};
    $species[$counter]=$$row{species};
    $length[$counter]=$$row{length};
    $keywords[$counter]=$$row{keywords};
    $start_pos[$counter]=$$row{start_pos};
    $stop_pos[$counter]=$$row{stop_pos};
    $original[$counter]=$$row{org_sequence};
    $structural[$counter]=$$row{str_sequence};
    $chemical[$counter]=$$row{che_sequence};
    $functional[$counter]=$$row{fun_sequence};
    $charge[$counter]=$$row{cha_sequence};
    $hydrophobic[$counter]=$$row{hyd_sequence};
    $dayhoff[$counter]=$$row{day_sequence};
    $sneath[$counter]=$$row{sne_sequence};
    $counter++;
}
$sth->finish();
$dbh->disconnect;
my $count = scalar(@accession);
my $dbmatches=[];
#Store parsed results as hashref in arrayref
for(my $i=0; $i < scalar(@accession); $i++){
    #hash ref:  $href->{ $key } = $value;
    my $href = {};
    $href->{'accession'}=$accession[$i];
    $href->{'description'}=$description[$i];
    $href->{'species'}=$species[$i];
    $href->{'length'}=$length[$i];
    $href->{'keywords'}=$keywords[$i];
    $href->{'start_pos'}=$start_pos[$i]+1;
    $href->{'stop_pos'}=$stop_pos[$i]+1;
    $href->{'original'}=$original[$i];
    $href->{'structural'}=$structural[$i];
    $href->{'chemical'}=$chemical[$i];
    $href->{'functional'}=$functional[$i];
    $href->{'charge'}=$charge[$i];
    $href->{'hydrophobic'}=$hydrophobic[$i];
    $href->{'dayhoff'}=$dayhoff[$i];
    $href->{'sneath'}=$sneath[$i];
    push(@$dbmatches, $href);
}

#Store explanation of oddcode as hashref in arrayref $bioperl
my $bioperl=[];
my $bp_href = {};
$bp_href->{'intro'}='The following explains each oddcode';
$bp_href->{'structural'}='Structural: A (ambivalent), E (external), I (internal)';
$bp_href->{'chemical'}='Chemical: A (acidic), L (aliphatic), M (amide), R (aromatic), C (basic),  H (hydroxyl),  I (imino), S (sulphur)';
$bp_href->{'functional'}='Functional: A (acidic), C (basic), H (hydrophobic), P (polar)';
$bp_href->{'charge'}='Charge: A (negative; NOT anode), C (positive; NOT cathode), N (neutral)';
$bp_href->{'hydrophobic'}='O (hydrophobic), I (hydrophilic)';
$bp_href->{'dayhoff'}='Dayhoff: turns amino acid sequence into 6-letter Dayhoff alphabet:
A (=C), C (=AGPST), D (=DENQ), E (=HKR), F (=ILMV), G (=FWY)';
$bp_href->{'sneath'}='Sneath: turns amino acid sequence into 7-letter Sneath alphabet:
A (=ILV), C (=AGP), D (=MNQ), E (=CST), F (=DE), G (=KR), H (=FHWY)';
push(@$bioperl, $bp_href);

print $cgi->header('application/json');
print $json->encode(
    { db_count => $count, dbmatches => $dbmatches, bioperl => $bioperl }
    );
