// Generated by CoffeeScript 1.6.2
(function() {
  var backend_url, c, convertJSON;

  c = typeof console !== "undefined" && console !== null ? console : {
    log: $.noop
  };

  c.log("location", location.host);

  if (location.host === "localhost") {
    backend_url = "http://localhost:8000";
  } else {
    backend_url = "nysno.wsgi";
  }

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

  convertJSON = function(xml) {
    var elem, out, sentence, x, _i, _j, _len, _len1, _ref, _ref1;

    out = {
      kwic: []
    };
    _ref = $("sentence", xml);
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      elem = _ref[_i];
      sentence = {
        tokens: []
      };
      _ref1 = $.xml2json(elem).w;
      for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
        x = _ref1[_j];
        sentence.tokens.push($.extend({}, x));
      }
      out.kwic.push(sentence);
    }
    return JSON.stringify(out);
  };

  window.get = function() {
    $("body").addClass("loading");
    return $.ajax({
      url: "http://spraakbanken.gu.se/ws/korp/annotate",
      dataType: "xml",
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

        c.log("success", xml);
        korpJson = convertJSON(xml);
        return $.ajax({
          url: backend_url,
          data: {
            text: korpJson,
            lang: $("#lang_select").val() || "bliss"
          },
          type: "POST",
          dataType: "json",
          success: function(data) {
            var sents;

            window.data = data;
            sents = _.flatten(_.pluck(data.kwic, "tokens"));
            $("#result").html($("#wordTmpl").tmpl(sents, {
              lang: $("#lang_select").val() || "bliss"
            }));
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
