$(document).ready(function(){
    $("#available-appointments").find('tbody').empty();
    $.ajax({
        url: "list",
        type: "GET",
        success: function (data) {
           if ("available_slots" in data){
                updateAppointmentTable(data.available_slots)
            }
        },
        error: function (jqXHR, exception) {
            console.log(jqXHR.responseText);
        }
    });
});

$("#location-select").on("change", function(){
    $("#available-appointments").find('tbody').empty();
    var location = $("#location-select option:selected").val();
    $.ajax({
        url: "list",
        type: "GET",
        data: {
            "location":location
        },
        success: function (data) {
            if ("available_slots" in data){
                updateAppointmentTable(data.available_slots)
            }
        },
        error: function (jqXHR, exception) {
            console.log(jqXHR.responseText);
        }
    });
});

function updateAppointmentTable(available_slots){
    $.each(available_slots, function(i, item){
        $("#available-appointments").find('tbody').append(
            "<tr>" +
                "<td>" +
                    "<input type=\"checkbox\" id=\"" + item.id + "\" name=\"submit\" value=\"" + item.id + "\">" +
                "</td>" +
                "<td>" + item.location + "</td>" +
                "<td>" + item.date + "</td>" +
                "<td>" + item.time + "</td>"
            + "</tr>");
    })
}