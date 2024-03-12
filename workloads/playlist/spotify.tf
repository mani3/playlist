module "playlist" {
  source = "../../modules/spotify"

  for_each = { for i, v in local.yml : v.date => v }

  name        = each.value.date
  description = each.value.playlist_name
  playlist    = each.value.song_list
}
