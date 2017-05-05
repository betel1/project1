
function GenreRecommendation() {
    $("#rec_genres").empty();
    var tab = $("<table>").append($("<thead>"));
    var tbody = $("<tbody>");
        tbody.append(
        $("<tr>").append($("<td>").text($("#gen1").val())),
        $("<tr>").append($("<td>").text($("#gen2").val()))
    );   
    tab.append(tbody);
    $("#rec_genres").append(tab);
}


function results_table(json) {
  
    var tab = $("<table>").attr("class","table table-hover");
    var tbody = $("<tbody>");
    tbody.append($("<tr>").append(
                $("<td>").text("Show ID"),
                $("<td>").text("Show Name"),
                $("<td>").text("Language"),
                $("<td>").text("Genres")));
    for(i in json['data']){    
        tbody.append(
            $("<tr>").append(
                $("<td>").text(json['data'][i]['show_id']),
                $("<td>").text(json['data'][i]['name']),
                $("<td>").text(json['data'][i]['language']),
                $("<td>").text(json['data'][i]['genres'])

            ).attr("data-battle-id", json['data'][i]['show_id']).click(function(){
                  
                  get_details($(this).attr("data-battle-id"));
            })

        );
        
    }
    tab.append(tbody);
    $("#result").empty();
    $("#result").append(tab);  
}


function start_search() {

    gen1 = $("#gen1").val();
    gen2 = $("#gen2").val();
    $.get("/search",{"genre1":gen1,"genre2":gen2},results_table);
     
}

function display_details(json) {

   
    var descrip = $("<div>").html(json['data']['summary']); 
    var table = $("<div>");
    $("#detail_body").empty();
    $("#detail_body").append(descrip);
    table.append($("<table>").attr("class","table table-hover").append(
    $("<tr>").append(
        $("<th>").text("name"),
        $("<th>").text(json['data']['name'])),
    $("<tr>").append(
        $("<th>").text("URL"),
        $("<th>").text(json['data']['url'])),
    $("<tr>").append(
        $("<th>").text("show_id"),
        $("<th>").text(json['data']['show_id']))));
    $("#detail_body").append(table);
    $("#detail_body").append(
    $("<img>").attr("src",json['data']['img']));
   
   $("#detail_header").empty();
   $("#detail_header").text(json['data']['name']);

   $("#details").modal();
}


function get_details(id) {

    $.get("/detail",{"show_id":id},display_details);
}


$(document).ready(function(){

      start_search();
      GenreRecommendation();
})