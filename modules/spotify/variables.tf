variable "name" {
  type        = string
  description = "Name of the Spotify playlist"
}

variable "description" {
  type        = string
  description = "Description of the Spotify playlist"
}

variable "playlist" {
  type = list(object({
    title  = string
    artist = string
  }))

  description = "List of playlists to be created"
  default = [
    {
      title  = "playlist1"
      artist = "This is playlist1"
    },
    {
      title  = "playlist2"
      artist = "This is playlist2"
    }
  ]
}
