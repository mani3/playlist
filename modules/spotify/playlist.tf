data "spotify_search_track" "by_name" {
  for_each = { for i, track in toset(var.playlist) : "${track.title}/${track.artist}" => track }

  name  = each.value.title
  limit = 1
}

resource "spotify_playlist" "playlist" {
  name        = var.name
  description = var.description
  public      = false

  tracks = flatten([for track in data.spotify_search_track.by_name : track.tracks[*].id])
}
