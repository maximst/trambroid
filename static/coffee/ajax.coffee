vote = () ->
  $.get $(this).attr('href'), (data) =>
    score_votes = $ '#score_votes'
    vote_block = $ '#vote_block'
    score_votes.html data.score

    score_votes.removeClass()
    if data.score < 0
      score_votes.addClass 'text-error'
    else if data.score > 0
      score_votes.addClass 'text-success'

    vote_block.attr 'title', "Score: #{data['score']} / Votes: #{data['num_votes']}"
    $('#success_alert').show 300, () =>
      setTimeout '$("#success_alert").hide(300)', 5000

hide_div = (event) ->
  if $(event.target).closest('#success_alert').length
    return
  $('#success_alert').hide 300
  event.stopPropagation()

$ () =>
  $(document).click hide_div
  $('#down_vote').click vote
  $('#up_vote').click vote
