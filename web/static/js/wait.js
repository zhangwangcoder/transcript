$(document).ready(function () {
    setInterval(ajaxd, 5000);
});

function ajaxd() {
    var audio_id = $("h6").attr("audio_id");
    $.ajax({
        url: '/check-status/',
        method: "POST",
        data: {"transcript_id": audio_id},
        dataType: 'json',
        success:
            function (data) {
                if (data.completed) {
                    window.location.replace("/result/?task_id="+data.task_id)
                }
            }
    })
    ;
}