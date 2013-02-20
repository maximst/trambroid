###function vote() {
    $.get($(this).attr("href"), function(data) {
        var score_votes = $("#score_votes");
        var vote_block = $("#vote_block");
        score_votes.html(data["score"]);
        if (data["score"] < 0) {
            score_votes.removeClass();
            score_votes.addClass("text-error");
        }
        else if (data["score"] > 0) {
            score_votes.removeClass();
            score_votes.addClass("text-success");
        }
        else {
            score_votes.removeClass();
        }
        vote_block.attr("title", "Score: " + data["score"] + " / Votes: " + data["num_votes"]);
        $("#success_alert").show(300, function() { setTimeout('$("#success_alert").hide(300)', 5000) });
    });
}

function hide_div(event) {
    if ($(event.target).closest("#success_alert").length) return;
    $("#success_alert").hide(300);
    event.stopPropagation();
}

$(function() {
    $(document).click(hide_div);
    $("#down_vote").click(vote);
    $("#up_vote").click(vote);
});###
