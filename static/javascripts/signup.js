$(function () {
    $("#btnSignUp").click(function () {
        $.ajax({
            url: "/signUp",
            data: $("form").serialize(),
            type: "POST",
            success: function (message) {
                //always called with 200 status, even with error message
                
                //print message to console
                console.log(message);

                if (message == "user created") {
                    //display success message to user
                    $("#errorMessage").empty();
                    $("form").empty();
                    $("#successMessage").html("success!");

                    //redirect to sign in page
                    window.setTimeout("window.location.replace('/showSignIn')", 2500);
                }
                else {
                    //display error message to user below form
                    $("#errorMessage").html(message);
                }
            },
            error: function (message) {
                //handle other error
                console.log(message);
            }
        });
    });
});
