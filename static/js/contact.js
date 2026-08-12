$(document).ready(function () {
  $("#contact-form").on("submit", function (e) {
    e.preventDefault();

    const data = {
      name: $("#name").val(),
      email: $("#email").val(),
      message: $("#message").val()
    };

    $.ajax({
      url: "/api/contact",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function (res) {
        $("#form-status").removeClass("text-danger").addClass("text-success").text(res.message);
        $("#contact-form")[0].reset();
      },
      error: function (xhr) {
        const msg = xhr.responseJSON ? xhr.responseJSON.error : "Something went wrong";
        $("#form-status").removeClass("text-success").addClass("text-danger").text(msg);
      }
    });
  });
});
