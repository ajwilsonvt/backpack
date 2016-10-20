$(function () {
    $.ajax({
        url: "/getNotes",
        type: "GET",
        success: function (message) {
            //always called with 200 status, even with error message

            //print message to console
            console.log(message);

            if (message.startsWith("error")) {
                //display error message
                $(".jumbotron").empty();
                $(".jumbotron").html("<h2 class=text-danger>"+message+"</h2>");
            }
            else {
                var noteObj = JSON.parse(message);
                var $note = null;

                $.each(noteObj, function (index, value) {
                    $note = $(".list-group:first").clone();
                    $note.find("h4").text(value.title);
                    $note.find("p").text(value.post);
                    $(".jumbotron").append($note);
                });
                //remove empty first parent
                $(".list-group:first").empty();

                //print success message to console
                console.log("successfully retrieved notes");
            }
        },
        error: function (message) {
            console.log(message);
        }
    });
});
