# Recovery Map artwork is the Commons "Muscles front and back" SVG, kept as a separate CC BY-SA file

Status: proposed (draft awaiting Liam's approval)

The Recovery Map is drawn from Wikimedia Commons "Muscles front and back.svg" by OpenStax, Tomáš Kebert & umimeto.org, licensed CC BY-SA 4.0. It was the only openly licensed candidate that is true vector anatomy with one path per muscle (see `docs/research/anatomical-svg.md`). We split and recolour it and give its regions Muscle IDs, and the result stays a standalone SVG file licensed CC BY-SA 4.0. That keeps share-alike limited to the artwork and leaves the repo's code licence alone. The credit (creators, link, licence, "modified") goes in the file, the README and the app's About screen. Muscles the superficial drawing cannot show (e.g. triceps medial head, erector spinae) are handled in the Muscle taxonomy. If this artwork has to be dropped, the fallback is the MIT-licensed path data from react-native-body-highlighter.
