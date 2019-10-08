$(document).ready(function() {
  var transitionDelay1 = 300;
  var transitionDelay2 = 600;

  $.post("/init", function(data) {
    update(data);
  });

  $("#buttonAbout").click(function() {
    $("#welcomeContent").css("opacity", "0");

    setTimeout(function() {
      $("#welcomeContent").addClass("hidden");
      $(".overlay-white").addClass("expanded-medium overlay-whiter");
      $("#aboutContent").removeClass("hidden");
    }, transitionDelay1);

    setTimeout(function() {
      $("#aboutContent").css("opacity", "1");
    }, transitionDelay2);
  });

  $("#buttonStart").click(function() {
    $("#welcomeContent").css("opacity", "0");

    setTimeout(function() {
      $("#welcomeContent").addClass("hidden");
      $(".overlay-white").addClass("expanded-full");
      $("#sofaContent").removeClass("hidden");
    }, transitionDelay1);

    setTimeout(function() {
      $("#sofaContent").css("opacity", "1");
    }, transitionDelay2);
  });

  $(".btn-back").click(function() {
    $("#aboutContent").css("opacity", "0");
    $("#sofaContent").css("opacity", "0");

    setTimeout(function() {
      $("#aboutContent").addClass("hidden");
      $("#sofaContent").addClass("hidden");
      $(".overlay-white").removeClass(
        "expanded-medium expanded-full overlay-whiter"
      );
      $("#welcomeContent").removeClass("hidden");
    }, transitionDelay1);

    setTimeout(function() {
      $("#welcomeContent").css("opacity", "1");
    }, transitionDelay2);
  });

  $(".star-rating").click(function(e) {
    $.post("/submission/" + $(this).attr("value"), function(result) {
      $(":input").prop("checked", false);
      update(result);
    });
  });

  function update(str) {
    var data = JSON.parse(str);
    console.log(data["img-link"]);
    $("#sofaImage").attr("src", data["img-link"]);
    $("#viewProd").attr("href", data.link);
  }
});
