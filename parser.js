$(".upload").click(function(){
  window.location.href = "browse.html";
});

function parser(data){
    $("#Heading").html(data.Title);
    $("#taskDescription").html(data.TaskDescription);
    for (var i=0; i<data.NeedHelp.length; i++){
      $("#needHelp").append('<h4 id="step'+(i+1)+'" class="well">'+data.NeedHelp[i].Title+'</h4><div class="well-sm"><span id="content'+(i+1)+'">'+data.NeedHelp[i].TaskDescription+'</span><br><button class="btn btn-success upload">Submit the Solution of Step '+(i+1)+'</button></div>');
    }
    $('#collapsible-panels div').hide();
    $('#collapsible-panels a').click(function(e) {
        $(this).parent().next('#collapsible-panels div').slideToggle('slow');
        $(this).parent().toggleClass('active');
        e.preventDefault();
    });
};