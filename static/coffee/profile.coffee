readURL = (e) ->
  input = e.target
  if input.files && input.files[0]
    reader = new FileReader()
    reader.onload = (e) ->
      $avatar = $('#profile-avatar')
      $avatar.attr('src', e.target.result)

    reader.readAsDataURL(input.files[0])

$ () =>
  $("#id_avatar").change(readURL)