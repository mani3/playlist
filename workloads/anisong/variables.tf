
variable "spotify_api_key" {
  type        = string
  description = "API key for Spotify"
}

locals {
  yml_anisong = yamldecode(file("./playlist_anisong.yml"))
}
