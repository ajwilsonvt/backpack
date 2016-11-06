$(function () {

    getNotes();

    $("#btnUpdate").click(function () {
        $.ajax({
            url: "/updateNote",
            data: {title:$("editTitle").val(),
                post: $("editPost").val(),
                id: localStorage.getItem("editID")},
            type: "POST",
            success: function (message) {
                $("#editModal").modal("hide");

                //repopulate the list
                getNotes();
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});

function getNotes() {
    $.ajax({
        url: "/getNotes",
        type: "GET",
        success: function (message) {
            //always called with 200 status, even with error message

            //print message to console
            console.log(message);

            if (message.startsWith("error")) {
                console.log(message);
            }
            else {
                var noteObj = JSON.parse(message);

                //empty and append the title of each note to ulist id in userhome.html
                $("#ulist").empty();
                $("#listTemplate").tmpl(noteObj).appendTo("#ulist");

                //print success message to console
                console.log("successfully retrieved notes");
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
};

function edit(element) {
    localStorage.setItem("editID", $(element).attr("data-id"));
    $.ajax({
        url: "/getNoteByID",
        data: {id: $(element).attr("data-id")},
        type: "POST",
        success: function (message) {
            var data = JSON.parse(message);

            $("#editTitle").val(data[0]["title"]);
            $("#editPost").val(data[0]["post"]);
            $("#editModal").modal();
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function confirmDelete(element) {
    localStorage.setItem("deleteID", $(element).attr("data-id"));
    $("#deleteModal").modal();
}

function deleteNote() {
    $.ajax({
        url: "/deleteNote",
        data: {id: localStorage.getItem("deleteID")},
        type: "POST",
        success: function (message) {
            var result = JSON.parse(message);

            if (result.status == "OK") {
                $("#deleteModal").modal("hide");
                getNotes();
            }
            else {
                alert(result.status);
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}
