window.onresize=displayGraph;

function displayGraph() {
    $("#main li").each((i, dom)=>{
        var lh=$(dom).find(".left button").css("height");
        var ph=$(dom).css("height");
        ph=parseInt(ph);
        lh=parseInt(lh);
        var rn=$(dom).find(".right button").length;
        var mw=$(dom).find(".mid").css("width");
        var mh=$(dom).find(".mid").css("height");
        mw=parseInt(mw);
        mh=parseInt(mh);
        mw-=20;
        var x1=0, y1=parseInt(ph/2);
        $(dom).find(".mid").text("");
        for(var i=0; i<rn; i++)
            $(dom).find(".mid").append(paintLine(x1, y1, mw, parseInt(ph/rn)*i+33, mh));
        var val=ph/2-lh/2;
        if(val <= 0) return;
        $(dom).find(".left").css({
            marginTop: val
        });
    });
}

function paintLine(x1, y1, x2, y2, h) {
    return $(`<svg width='${x2}' height='${h}' xmlns="http://www.w3.org/2000/svg" version="1.1">
    <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"
    style="stroke:rgb(0,0,0);stroke-width:1"/>
  </svg>`);
}

