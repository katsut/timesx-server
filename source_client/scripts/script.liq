settings.log.file.path.set("/var/log/liquidsoap/<script>.log")

settings.server.timeout.set(-1.)
settings.init.allow_root.set(true)
settings.log.stdout.set(true)

settings.init.force_start.set(true)
settings.server.telnet.set(true)
settings.server.telnet.port.set(8002)

# First, we create a list referencing the dynamic sources:
dyn_sources = ref([ ])


out = output.icecast(%mp3,
                     host="$SERVER_HOST",
                     port=8000,
                     password="hackme",
                     fallible=true)

# Now we write a function to create
# a playlist source and output it.
def append_playlist(uri) =
  # The playlist source
  blank = audio_to_stereo(single("/var/data/liquidsoap/blank.mp3")) #
  playlist = request.queue(id="#{uri}")
  playlist = fallback([playlist, blank])
  output = out(mount=uri, playlist)
  element = { uri = uri, playlist = playlist, output = output }
  dyn_sources := list.append([element], !dyn_sources)
  "Done!"
end

# And a function to destroy a dynamic source
def destroy_playlist(target_uri) =
  # Now we execute the function:
  target = list.find(fun (e) -> e.uri == target_uri, !dyn_sources)
  target.output.shutdown()
  dyn_sources = list.filter(fun (e) -> e.uri != target_uri, !dyn_sources)
  "Done!"
end
 
server.register(namespace="uirou",
                usage="start <uri>",
                "start",
                append_playlist)

server.register(namespace="uirou",
                usage="stop <uri>",
                "stop",
                destroy_playlist)

output.dummy(blank())
