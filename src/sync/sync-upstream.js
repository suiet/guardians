import { fetchUpstreamList as fetchFromMystenLabs } from "../sources/mystenlabs/loader.js"

async function run() {
  const mystenLabsData = await fetchFromMystenLabs()

  // fetchFromMystenLabs().catch(console.error);
}

run()