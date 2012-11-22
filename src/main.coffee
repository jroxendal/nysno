c = console ? log : $.noop
c.log("location", location.host)
if location.host == "localhost"
    backend_url = "http://localhost:8000"
else
    backend_url = "nysno.wsgi"

$ ->
    c.log "starting up"
    $("#content form").submit(false)
    $("#content input.send").click ->
        get()


    $("body").bind "keydown", (event) =>
        if event.which == 27 then $("#flip").removeClass("flipped")

    $("#get_article").click ->
        $("#flip").addClass("flipped")

    $("iframe").load ->
        $("#mainnews p:first", $("iframe").get(0).contentDocument
        ).bind( "mouseenter", ->
            $(this).css("background-color", "lightblue")
        ).bind("mouseleave", ->
            $(this).css("background-color", "white")
        ).click ->
            $("#content textarea").val($(this).text())
            $("#flip").removeClass("flipped")



    $(".corner").load("img/arrow.svg")
    .click ->
        $("#flip").removeClass("flipped")



convertJSON = (obj)->
    out = {kwic : []}
    sent = if _.isArray(obj.sentence) then obj.sentence else [obj.sentence]
    for wd in sent
        sentence = {tokens : []}
        sentence.tokens.push($.extend({}, x)) for x in wd.w
        out.kwic.push(sentence)

    return JSON.stringify(out)

window.get = ->
    $("body").addClass("loading")
    $.ajax
        url: "http://demo.spraakdata.gu.se/dan/backend/"
        dataType: "text"
        timeout: 300000
        type: "GET"
        data:
            text: $("#content textarea").val()
            settings : JSON.stringify(
                attributes: "word,pos,prefix,suffix,lex".split(","))
            # fmt: "xml"
            # incremental: false

        success: (xml, textStatus, xhr) ->
            c.log("xml2json", $.xml2json(xml))
            window.xml = $.xml2json(xml)
            korpJson = convertJSON($.xml2json(xml))

            $.ajax
                url : backend_url,
                data: korpJson,
                type : "POST",
                dataType : "json",
                success: (data) ->
                    window.data = data
                    sents = _.flatten _.pluck data.kwic, "tokens"
                    $("#result").html(
                      $("#wordTmpl").tmpl(sents)
                      )
                    $("body").removeClass("loading")



        # progress: (data, e) ->
        #     c.log "progress", data


        error: (jqXHR, textStatus, errorThrown) ->
            c.log "error", jqXHR, textStatus, errorThrown






