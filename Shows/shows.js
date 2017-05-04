# -*- coding: utf-8 -*-
"""
Created on Thu May 04 16:57:19 2017

@author: Eric
"""

function GenreRecommendation() {
    $("#rec_genres").empty();
    var tab = $("<table>").append($("<thead>"));
    var tbody = $("<tbody>");
        tbody.append(
        $("<tr>").append($("<td>").text($("#gen1").val())),
        $("<tr>").append($("<td>").text($("#gen2").val())),
    );   
    tab.append(tbody);
    $("#rec_genres").append(tab);
}


function results_table(json) {
    alert(json.data.length)
    var tab = $("<table>").attr("class","table table-hover");
    var tbody = $("<tbody>");
    tbody.append($("<tr>").append(
                $("<td>").text("Show ID"),
                $("<td>").text("Show Name"),
                $("<td>").text("Language")));
    for(i in json['data']){    
        tbody.append(
            $("<tr>").append(
                $("<td>").text(json['data'][i]['show_id']),
                $("<td>").text(json['data'][i]['name']),
                $("<td>").text(json['data'][i]['languae'])

            )
        );
        
    }
    tab.append(tbody);
    $("#result").empty();
    $("#result").append(tab);  
}


function start_search() {
   /*
      Initiates a search
   */
   // TODO: get the values of #state and #battle
    gen1 = $("#gen1").val();
    gen2 = $("#gen2").val();
    $.get("/search",{"gen1":gen,"name":},results_table);
   // TODO: do a `$.get()`, 
   //   - request `/search`
   //   - pass the user params
   //   - attach results_table as the callback   
}

function display_details(json) {
   /* 
      display the details of a single battle in the #details modal
   */
   
   // TODO: create an upper div for the description, lower one for a table
    var descrip = $("<div>").text(json['data']['description']); 
    var table = $("<div>");
    $("#details").empty();
    $("#details").append(descrip);
    table.append($("<table>").attr("class","table table-hover").append(
    $("<tr>").append(
        $("<th>").text("name"),
        $("<th>").text(json['data']['name'])),
    $("<tr>").append(
        $("<th>").text("state"),
        $("<th>").text(json['data']['state'])),
    $("<tr>").append(
        $("<th>").text("result"),
        $("<th>").text(json['data']['result']))));
    $("#details").append(table);
   // TODO: build the table to display your choice of record fields
       
   // TODO: set the `#detail_header` to the battle name
   $("#detail_header").empty();
   $("#detail_header").text(json['data']['name']);
   // show the modal
   $("#details").modal();
}


function get_details(id) {
   // TODO: request details json, trigger display_details
    $.get("/detail",{"battle_id":id},display_details);
}


$(document).ready(function(){
   /*
      Document Ready Handler
   */

   // TODO: build the #state dropdown
   $.get("/states",{},states_list);
  
   $("#form1").submit(function(event){
      event.preventDefault();
      start_search();
   })
   // TODO: hook up start_search function to the form's submit event
})