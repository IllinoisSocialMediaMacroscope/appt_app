$(document).ready(function(){
    $.ajax({
        url: "my-appointment",
        type: "GET",
        success: function (data) {
           if ("claimed_slot" in data){
               $(".highlight").show();
                displayMyAppointment(data.claimed_slot)
            }
        },
        error: function (jqXHR, exception) {
            alert(jqXHR.responseText);
        }
    });

    $.ajax({
        url: "list",
        type: "GET",
        success: function (data) {
           if ("available_slots" in data){
                updateAppointmentTable(data.available_slots)
            }
        },
        error: function (jqXHR, exception) {
            alert(jqXHR.responseText);
        }
    });
});

$("#location-select").on("change", function () {
    filterOnChange();
});

$("#date-select").on("change", function () {
    filterOnChange();
});

$("#timeslot-select").on("change", function () {
    filterOnChange();
});

$("#submit-appointment").on("click", function() {
    // check if ONE appointment has been selected
    var selectedElement = $("#available-appointments").find('tbody').find("input:checked");
    if (selectedElement.length === 1){
        var appt_id = $(selectedElement[0]).val();
        $.ajax({
            url: "submit",
            type: "POST",
            contentType: 'application/json',
            data:JSON.stringify({
                "appt_id":appt_id
            }),
            success: function (data) {
                alert("your appointment:" + JSON.stringify(data) + "has successfully been booked!")
                displayMyAppointment(data.claimed_slot);
            },
            error: function (jqXHR, exception) {
                alert(jqXHR.responseText);
            }
        });
    }
    else{
        alert("You have to select ONE available appointment!");
    }

});

$("#cancel-appointment").on("click", function() {
    $.ajax({
        url: "cancel",
        type: "DELETE",
        success: function (data) {
            alert("your appointment:" + JSON.stringify(data) + "has successfully been canceled!")
            displayMyAppointment({});
        },
        error: function (jqXHR, exception) {
            alert(jqXHR.responseText);
        }
    });
});

function filterOnChange() {
    var location = $("#location-select option:selected").val();
    if ($("#date-select").val() !== "" && $("#date-select").val() !== undefined) {
        var date = $("#date-select").val();
    } else {
        var date = "";
    }

    var time = $("#timeslot-select option:selected").val();
    $.ajax({
        url: "list",
        type: "GET",
        data: {
            "location": location,
            "date": date,
            "time": time,
        },
        success: function (data) {
            if ("available_slots" in data) {
                updateAppointmentTable(data.available_slots)
            }
        },
        error: function (jqXHR, exception) {
            alert(jqXHR.responseText);
        }
    });
}

function updateAppointmentTable(available_slots) {
    $("#available-appointments").find('tbody').empty();
    $.each(available_slots, function (i, item) {
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

function displayMyAppointment(claimed_slot) {
    $("#my-appointment").find('tbody').empty();
    if (!$.isEmptyObject(claimed_slot)){
        $("#my-appointment").find('tbody').append(
        "<tr>" +
            "<td>" + claimed_slot.location + "</td>" +
            "<td>" + claimed_slot.date + "</td>" +
            "<td>" + claimed_slot.time + "</td>" +
        "</tr>");
    }
}