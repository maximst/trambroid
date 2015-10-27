quote = (e) ->
  $quote_link = $(e.target)
  $parent_form_field = $('input#id_parent')
  $body_form_field = $('textarea#id_body')
  parent_id = $quote_link.data('quoted-comment-id')
  author = $quote_link.data('author')
  $parent_comment_body = $("[data-comment-body=#{parent_id}]")
  old_body = $body_form_field.val()

  regex_quote = /<\s*blockquote[^>]*>((?!<\s*\/\s*blockquote\s*>)(.|\n))*<\s*\/\s*blockquote\s*>/igm
  quoted_text = $parent_comment_body.html().replace(regex_quote, '')
  quoted_text = quoted_text.replace(/<\s*br[^>]*>/ig, '\n')
  quoted_text = quoted_text.replace(/(<\s*[^>]*>|<\s*\/\s*[^>]*>)/ig, '').trim()

  quote = "[quote comment=#{parent_id} author=\"#{author}\"]\n#{quoted_text}\n[/quote]"

  if old_body
    old_body = "#{old_body}\n"

  $parent_form_field.val(parent_id)
  if old_body.indexOf(quoted_text) == -1
    $body_form_field.val("#{old_body}#{quote}\n")
  $body_form_field[0].focus()
  $body_form_field[0].scrollIntoView()

$ () =>
  $('[data-comment-quote]').click(quote)