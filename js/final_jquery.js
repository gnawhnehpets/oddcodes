/*
  ###################################################################
  ###This function executes our initial BLAST search via an AJAX call
  ###################################################################
*/
function runSearch( term ) {
    // hide and clear the previous results, if any
    $('#results').hide();
    $('tbody').empty();
    // transforms all the form parameters into a string we can send to the server
    var frmStr = $('#search_term').serialize();
    if(frmStr == 'search_term='){
	alert('Please enter in DNA or protein sequence in form');
    }else{
	alert('Please wait for BLAST results');
	$.ajax({
		url: './final.cgi',
		    dataType: 'json',
		    data: frmStr,
		    success: function(data, textStatus, jqXHR) {
		    processJSON(data);
		},
		    error: function(jqXHR, textStatus, errorThrown){
		    alert("Failed to perform BLAST search! textStatus: (" + textStatus +
			  ") and errorThrown: (" + errorThrown + ")");
		}
	    });
    }
}
/* 
   #####################################################################################################
   ###This processes a passed JSON structure representing BLAST results and draws it to the result table
   #####################################################################################################
*/
function processJSON( data ) {    
    // set the span that lists the match count
    $('#match_count').text( data.match_count );
    // set the span that lists the BLAST program used
    $('#program').text( data.program );
    // this will be used to keep track of row identifiers
    var next_row_num = 1;
    // iterate over each match and add a row to the result table for each
    $.each( data.matches, function(i, item) {
	    var this_row_id = 'result_row_' + next_row_num++;	    
	    // create a row and append it to the body of the table
	    $('<tr/>', { "id" : this_row_id } ).appendTo('#results tbody');
	    $('<td><input type="checkbox" name="items[]" value="' + this_row_id + '" /></td>').appendTo('#' + this_row_id);
	    $('<td/>', { "text" : item.database } ).appendTo('#' + this_row_id);	    
	    $('<td/>', { "text" : item.accession } ).appendTo('#' + this_row_id);	    
	    $('<td/>', { "text" : item.description } ).appendTo('#' + this_row_id); 
	    $('<td/>', { "text" : item.score } ).appendTo('#' + this_row_id);
	    $('<td/>', { "text" : item.evalue } ).appendTo('#' + this_row_id);
	    $('<td/>', { "text" : item.start } ).appendTo('#' + this_row_id);
	    $('<td/>', { "text" : item.stop } ).appendTo('#' + this_row_id);
	});    
    // now show the result section that was previously hidden
    $('#results').show();
}
/*
  ########################################################################
  ###This function executes a query to the MySQL database via an AJAX call
  ########################################################################
*/
function databaseSearch( term ) {
    $('#dbresults').hide();
    //    $('tbody').empty();
    var dbStr = $('#db_term').serialize();
    if(dbStr == 'db_term='){
        alert('Please enter accession number in form');
    }else{
        $.ajax({
                url: './query.cgi',
                    dataType: 'json',
                    data: dbStr,
                    success: function(data, textStatus, jqXHR) {
                    processJSON_db(data);
                },
                    error: function(jqXHR, textStatus, errorThrown){
                    alert("Failed to search database! textStatus: (" + textStatus +
                          ") and errorThrown: (" + errorThrown + ")");
                }
            });
    }
}
/*
   ##################################################################################################################
   ###This processes a passed JSON structure representing a database query and draws results to the 'dbresults' table
   ##################################################################################################################
*/
function processJSON_db( data ) {
    $('#db_count').text( data.db_count );
    $('#dbresults tbody').empty();
    $('#dbresults thead').empty()
    var counter = 1;
    $.each( data.bioperl, function(i, item){
 	    $('#dbresults thead').append("<tr><td>"+item.intro+"</td><td>Structural  : "+item.structural+
                                         "<br>Chemical    : "+item.chemical+
                                         "<br>Functional  : "+item.functional+
                                         "<br>Charge      : "+item.charge+
                                         "<br>Hydrophobic : "+item.hydrophobic+
                                         "<br>Dayhoff     : "+item.dayhoff+
                                         "<br>Sneath      : "+item.sneath+
                                         "</td></tr>");	    
	});
    
    $.each( data.dbmatches, function(i, item) {
	    var this_hit = counter++;
	    $('#dbresults tbody').append('<tr><td><b>Match #'+this_hit+'</b></td><td></td></tr>');
	    $('#dbresults tbody').append('<tr><td>Description</td><td>'+item.description+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Species</td><td>'+item.species+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Accession</td><td>'+item.accession+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Length</td><td>'+item.length+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Keywords</td><td>'+item.keywords+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Region of alignment</td><td>aa'+item.start_pos+' - aa'+item.stop_pos+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Original</td><td>'+item.original+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Structural</td><td>'+item.structural+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Chemical</td><td>'+item.chemical+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Functional</td><td>'+item.functional+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Charge</td><td>'+item.charge+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Hydrophobic</td><td>'+item.hydrophobic+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Dayhoff</td><td>'+item.dayhoff+'</td></tr>');
	    $('#dbresults tbody').append('<tr><td>Sneath</td><td>'+item.sneath+'</td></tr>');
	});
    $('#dbresults').show();
}
/*
  ##################################################
  ###This function saves our selected times to MySQL
  ##################################################
*/
function saveSelectedItems (){
    alert('Saving selection...');
    //Clear old text file
    $.get("newfile.cgi");
    $('tbody tr').has(':checkbox:checked').map(function(index, el){
	    var jdatabase =  $(this).find('td:eq(1)').text();
            var jaccession =  $(this).find('td:eq(2)').text();
            var jdescription =  $(this).find('td:eq(3)').text();
            var jscore =  $(this).find('td:eq(4)').text();
            var jevalue =  $(this).find('td:eq(5)').text();
	    var jstart = $(this).find('td:eq(6)').text();
	    var jstop = $(this).find('td:eq(7)').text();
	    //Save BLAST stats to text file
	    $.get("selected.cgi", { 
		    'myDatabase' : jdatabase,
			'myAccession' : jaccession,
			'myDescription' : jdescription,
			'myScore' : jscore,
			'myEvalue' : jevalue,
			'myStart' : jstart,
			'myStop' : jstop
			});
	});
    alert('Saving sequence information in MySQL...');
    //Add BLAST results to MySQL
    $.post("add2db.cgi");
    $('#results').empty();
}
/*
  ############################################
  ###Run our javascript once the page is ready
  ############################################
*/
$(document).ready( function() {
	$('#dbresults').hide();
	//BLAST search
	$('#submit').click( function() {
		runSearch();
		return false;  // prevents 'normal' form submission
	    });
	//Save selected items
	$('#resubmit').click( function() {
                saveSelectedItems();
                return false;  // prevents 'normal' form submission
            });
	//Search database
	$('#db_search').click( function() {
                databaseSearch();
                return false;  // prevents 'normal' form submission
            });
	
    });
