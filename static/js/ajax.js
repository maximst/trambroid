function vote() {
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
        $("#success_alert").show("slow", function() { setTimeout('$("#success_alert").hide("slow")', 4000) });
    });
}

$(function() {
    $("#down_vote").click(vote);
    $("#up_vote").click(vote);
});
