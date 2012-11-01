c = console ? log : $.noop

korp_url = "http://mac12.svenska.gu.se:8000"

$ ->
    c.log "starting up"
    $("#content form").submit(false)
    $("#content input.send").click( ->
        $.getJSON korp_url, text:$("#content textarea").val(), (data)->
            window.data = data
            sents = _.flatten _.pluck data.kwic, "tokens"
            $("#wordTmpl").tmpl(sents).appendTo "#result" 
        ).click()
        
        
    
    $("body").bind "keydown", (event) =>
        if event.which == 27 then $("#flip").removeClass("flipped")        
    
    $("#get_article").click ->
        $("#flip").addClass("flipped") 
        
    $("iframe").load ->
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
     
            
         
f = "lollllhadrar"
