$(function() {
  $('.create-playlist').click(function(e) {
    e.preventDefault();
    var data,
      artists = [];

    $('.artist').map(function() {
      artists.push($(this).text());
    })

    data = {
      'artists': artists,
      'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
    };

    $.ajax({
      type: 'POST',
      url: '/create_playlist/',
      data: data,
      dataType: 'json',
      success: function (data) {
        //Update iframe to show new playlist
        var src = 'https://open.spotify.com/embed/user/ymqtwb9gcigva8pi2m32o9v0q/playlist/';
        src += data.playlist_id;
        $('iframe').attr('src', src);
      },
    })
  })

  $('.search-form').submit(function(event) {
    var listItem, $date, $listItem, $venue, $form;

    event.preventDefault();
    $form = $(this);

    if ($form.find('.city-query').val()) {
      $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.find('.city-query').serialize(),
        success: function(res) {
          //Clear data on new search
          $('.artist-list').html('');
          $('iframe').attr('src', '');
          //Create artist list for city
          createArtistList(res.concerts);
        },
        error: function(res) {
          alert('City not found');
        }

      })
    }
  })


  //Helper to create artist list after successful ajax response
  function createArtistList(concerts) {
    var listItem, $date, $listItem, $venue, $form

    _.map(concerts, function(concert) {
      $listItem = $('<li class="list-group-item"></li>')
      $date = $("<p class='concert-date'></p>").text(concert.start.date);
      $listItem.append($date);
      _.map(concert.performance, function(artist) {
        $artistItem = $('<p class="artist"></p>');
        $artistItem.text(artist.displayName).attr('name', artist.displayName);
        $listItem.append($artistItem);
      })
      $venue = $("<p class='venue-name'></p>").text(concert.venue.displayName + ', ' + concert.venue.metroArea.displayName);
      $listItem.append($venue);
      $('.artist-list').append($listItem);
    });
  }
})