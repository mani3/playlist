
variable "spotify_api_key" {
  type        = string
  description = "API key for Spotify"
}

locals {
  yml = yamldecode(file("./playlist.yml"))
}
