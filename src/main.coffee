
hej = ""
c = console ? log : $.noop


nameIdentifier = (text) ->
    re = ///
    ([A-ZÅÖÄ]
    \w+
    (\s 
        ([A-ZÅÖÄ])*
        (\.)*
        (\s)*   
        [A-ZÅÖÄ] 
        \w+
    )*)
    ///g 
    textArray = text.split("")
    modify = (match) ->
        start = match.index
        end = start + match[0].length - 1
        newWord = match[0].replace(/\s/g, '_')
        textArray[start..end] = ["<#{newWord}>"]
        
    matches = while match = re.exec(text)
        match
    
    for match in matches.reverse()
        modify match
        
    
    
    return textArray.join("") 


makeRequest = ->
    $.ajax 
        url : "http://spraakbanken.gu.se/ws/korp"
        data :
            corpus : "ATTASIDOR"
            cqp : "<sentence> []"
            start : 0
            end : 999
            show : "pos,lex"

    
$ ->
    c.log "starting up"
    
    $("#content form").submit ->
        c.log "submit"
        false
    
    $("body").bind "keydown", (event) =>
        if event.which == 27 then $("#flip").removeClass("flipped")        
    
    $("#get_article").click ->
        $("#flip").addClass("flipped")
        
    makeRequest()
    
    c.log(nameIdentifier "this is a test for Finding Some words That Are Names.")
    
    