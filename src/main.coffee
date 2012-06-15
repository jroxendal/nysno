
# hack for my editor.
$ = window.$


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
	
	
$ ->
	c.log "starting"
	
	$("#content form").submit ->
		c.log "submit"
		false
	
	c.log(nameIdentifier "this is a test for Finding Some words That Are Names.")
	
	