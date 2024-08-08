
variable "spotify_api_key" {
  type        = string
  description = "API key for Spotify"
}

locals {
  yml_memodis = yamldecode(file("./playlist_memodis.yml"))
  yml_anisong = yamldecode(file("./playlist_anisong.yml"))
}
