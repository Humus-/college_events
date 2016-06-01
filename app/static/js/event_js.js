$(document).ready(function() {
    $.getJSON({url: $SCRIPT_ROOT + '/getevents', success: function(result) {
        content = '<div class="ui divided items">';
        $.each(result.events, function(i,event) {
            content += '<div class="item"><div class="ui small image"><img src="/abc"></div><div class="content"><div class="header">' + event.name +'</div><div class="meta">'+ event.start_date + ' to ' + event.end_date +'</div><div class="description">' + event.description + '</div></div></div>';

        });
        content +='</div>'
        $(content).appendTo("#event_list");
    }});
});
