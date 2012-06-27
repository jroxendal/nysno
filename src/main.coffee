
c = console ? log : $.noop

$ ->
    c.log "starting up"
    $("#content form").submit(false)
    $("#content input.send").click ->
        $(this).val(":-(").prop("disabled", true)
        false
    
    $("body").bind "keydown", (event) =>
        if event.which == 27 then $("#flip").removeClass("flipped")        
    
    $("#get_article").click ->
        $("#flip").addClass("flipped") 
        
    $("iframe").load ->
        c.log("iframe load")
        $("#mainnews p:first", $("iframe").get(0).contentDocument).bind( "mouseenter", 
            -> $(this).css("background-color", "lightblue"))
        .bind("mouseleave", 
            -> $(this).css("background-color", "white"))
        .click ->
            $("#content textarea").val($(this).text())
            $("#flip").removeClass("flipped")
      
    
            
    $(".corner").load("img/arrow.svg")
    .click ->
        $("#flip").removeClass("flipped")
    
            
        
    # makeRequest()
    
    