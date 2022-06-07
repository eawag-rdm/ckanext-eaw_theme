$("li.resource-item").click(function(e) {
    var url = $(this).children("a.heading").first().attr("href");
    if ($(e.target).is("li.resource-item")) {
        window.location = url;
    }
});
