// Generated by CoffeeScript 1.4.0
(function() {
  var backend_url, c, convertJSON;

  c = typeof console !== "undefined" && console !== null ? console : {
    log: $.noop
  };

  backend_url = "nysno.wsgi";

  $(function() {
    var _this = this;
    c.log("starting up");
    $("#content form").submit(false);
    $("#content input.send").click(function() {
      return get();
    });
    $("body").bind("keydown", function(event) {
      if (event.which === 27) {
        return $("#flip").removeClass("flipped");
      }
    });
    $("#get_article").click(function() {
      return $("#flip").addClass("flipped");
    });
    $("iframe").load(function() {
      return $("#mainnews p:first", $("iframe").get(0).contentDocument).bind("mouseenter", function() {
        return $(this).css("background-color", "lightblue");
      }).bind("mouseleave", function() {
        return $(this).css("background-color", "white");
      }).click(function() {
        $("#content textarea").val($(this).text());
        return $("#flip").removeClass("flipped");
      });
    });
    return $(".corner").load("img/arrow.svg").click(function() {
      return $("#flip").removeClass("flipped");
    });
  });

  convertJSON = function(obj) {
    var out, sent, sentence, wd, x, _i, _j, _len, _len1, _ref;
    out = {
      kwic: []
    };
    sent = _.isArray(obj.sentence) ? obj.sentence : [obj.sentence];
    for (_i = 0, _len = sent.length; _i < _len; _i++) {
      wd = sent[_i];
      sentence = {
        tokens: []
      };
      _ref = wd.w;
      for (_j = 0, _len1 = _ref.length; _j < _len1; _j++) {
        x = _ref[_j];
        sentence.tokens.push($.extend({}, x));
      }
      out.kwic.push(sentence);
    }
    return JSON.stringify(out);
  };

  window.get = function() {
    $("body").addClass("loading");
    return $.ajax({
      url: "http://demo.spraakdata.gu.se/dan/backend/",
      dataType: "text",
      timeout: 300000,
      type: "GET",
      data: {
        text: $("#content textarea").val(),
        settings: JSON.stringify({
          attributes: "word,pos,prefix,suffix,lex".split(",")
        })
      },
      success: function(xml, textStatus, xhr) {
        var korpJson;
        c.log("xml2json", $.xml2json(xml));
        window.xml = $.xml2json(xml);
        korpJson = convertJSON($.xml2json(xml));
        return $.ajax({
          url: backend_url,
          data: korpJson,
          type: "POST",
          dataType: "json",
          success: function(data) {
            var sents;
            window.data = data;
            sents = _.flatten(_.pluck(data.kwic, "tokens"));
            $("#result").html($("#wordTmpl").tmpl(sents));
            return $("body").removeClass("loading");
          }
        });
      },
      error: function(jqXHR, textStatus, errorThrown) {
        return c.log("error", jqXHR, textStatus, errorThrown);
      }
    });
  };

}).call(this);
