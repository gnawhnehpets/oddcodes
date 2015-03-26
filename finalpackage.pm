#!usr/bin/perl
package finalpackage;
use Exporter 'import';
our @EXPORT_OK = ("parse");

=d
                                                                   Score     E
Sequences producing significant alignments:                       (Bits)  Value

gb|CP003179.1|  Sulfobacillus acidophilus DSM 10332, complete ...  35.6    9.5
gb|CP002901.1|  Sulfobacillus acidophilus TPY, complete genome     35.6    9.5
gb|CP003785.1|  Klebsiella pneumoniae subsp. pneumoniae 1084, ...  33.7       33
gb|CP003200.1|  Klebsiella pneumoniae subsp. pneumoniae HS1128...  33.7       33
emb|FR799623.2|  Leishmania donovani BPK282A1 complete genome,...  33.7       33
ref|XM_003407810.1|  PREDICTED: Loxodonta africana sushi, von ...  33.7       33
gb|CP002910.1|  Klebsiella pneumoniae KCTC 2242, complete genome   33.7       33
emb|FR796468.1|  Leishmania infantum JPCM5 genome chromosome 36    33.7       33
gb|CP000154.1|  Paenibacillus polymyxa E681, complete genome       33.7       33
ref|XM_002980639.1|  Selaginella moellendorffii hypothetical p...  33.7       33
ref|XM_002976895.1|  Selaginella moellendorffii hypothetical p...  33.7       33
ref|XM_002795133.1|  Paracoccidioides brasiliensis Pb01 nucleo...  33.7       33
dbj|AK350504.1|  Sus scrofa mRNA, clone:SPL010081A11, expresse...  33.7       33
ref|XM_002617814.1|  Clavispora lusitaniae ATCC 42720 hypothet...  33.7       33
gb|CP001785.1|  Ammonifex degensii KC4, complete genome            33.7       33
ref|XM_002544946.1|  Uncinocarpus reesii 1704 conserved hypoth...  33.7       33
dbj|AP006725.1|  Klebsiella pneumoniae subsp. pneumoniae NTUH-...  33.7       33
gb|CP000964.1|  Klebsiella pneumoniae 342, complete genome         33.7       33
gb|CP000792.1|  Campylobacter concisus 13826, complete genome      33.7       33
gb|CP000647.1|  Klebsiella pneumoniae subsp. pneumoniae MGH 78...  33.7       33
emb|BX537141.17|  Zebrafish DNA sequence from clone DKEY-9E8 i...  33.7       33

ALIGNMENTS
=cut
sub parse{
    open (FILE, '/var/www/shwang26/final/input_fasta.blastoutput');
    my $marker = 0;
    my @one;
    my @acc;
    my @desc;
    my @score;
    my @evalue;
    my @start;
    my @stop;
    my $counter = 0;
    my $countertwo = 0;
    while(<FILE>){
	chomp;
	if($marker == 1){
	    if (/^([^|]++)\|([^|]++)\|\s++(.*?)\s(\d++(?>\.\d++)?)\s++(\d++(?>\.\d++)?(?>e[+-]?\d++)?)\s*+$/) {
		$one[$counter] = $1;
		$acc[$counter] = $2;
		$desc[$counter] = $3;
		$score[$counter] = $4;
		$evalue[$counter] = $5;
		$counter++;
	    }
	}elsif($marker==0){
	    if(/^Sbjct +(\d+) +(\D+) +(\d+)/){
#               print $1."\t".$3."\n";
		$start[$countertwo]=$1;
		$stop[$countertwo]=$3;
		$countertwo++;
	    }
	}
	if(/Sequences producing significant alignments/){
	    $marker = 1;
	}elsif(/ALIGNMENTS/){
	    $marker = 0;
	}elsif(/No significant similarity found/){
	    last;
	}
    }
    for(my $i=0; $i < scalar(@one); $i++){
#	print "$one[$i] | $acc[$i] | $desc[$i] | $score[$i] | $evalue[$i]\n";
    }
    close FILE;
    return (\@one, \@acc, \@desc, \@score, \@evalue, \@start, \@stop);
}

1;
