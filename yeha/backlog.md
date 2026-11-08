# DumpCheck backlog

One item per night. Season sweeps jump the line.

## Next up

1. **Guide: "Tennessee State Park dump stations."** Ready now: 17 stations at 16 parks. Lead with the two that are open (Rock Island, Old Stone Fort), explain "call first" (parks rarely post campground dates or say whether non-campers can dump), group by region, and add a short "checked, no dump listed" list (Fall Creek Falls, Henry Horton, Montgomery Bell) plus the parks closed for renovations (Standing Stone, Pickett, Cove Lake, Norris Dam).
2. **More Tennessee State Parks** (current tnstateparks.com `/parks/<park>/camping` pages first). Confirm on a current camping page: Panther Creek (listed from its brochure, printed 2021; camping page returns a client error) and Warriors' Path (listed from the park's amenities list; its current camping page didn't show up in search, so the fetcher refused it). No official dump mention found yet: Bledsoe Creek and Mousetail Landing (camping pages error; reservation pages describe sites only; try their brochure PDFs), Davy Crockett Birthplace (only the legacy page loaded, no dump listed; find the current camping page), Fall Creek Falls (camping page, reservation page and FAQ PDF list no dump; brochure PDF errored). Not checked yet: Harrison Bay, Cumberland Mountain, Big Ridge, Indian Mountain, Pickwick Landing, Big Hill Pond, Fort Pillow, Hiwassee/Ocoee, and any other park with an RV campground. Record non-camper access and fees only if the park states them. Checked, not listed: Montgomery Bell and Norris Dam (2026-11-07); Fall Creek Falls and Henry Horton (current camping pages list no dump), Pickett and Cove Lake (campgrounds closed for renovations) (2026-11-08).
3. **Rest of the I-40 truck stops (Pilot / Flying J, Dandridge).** Pilot store pages now redirect to pilotcompany.com, and those redirects were refused on 2026-11-06. Still to check from each store's own page: Lebanon (921 Murfreesboro Rd), Dickson Pilot #409 (2320 TN-46), Knoxville Pilot #219 (7210 Strawberry Plains Pike) and store 4597 (redirects to a Gordonsville page). Already checked on 2026-11-06, no RV dump listed: Pilot #366 Jackson, ONE9 #1366 Holladay, Pilot #722 and #270 Knoxville. Dandridge (I-40 Exit 417): no Love's store page found; look for any other official truck-stop page there.
4. **More Corps campgrounds:** Cages Bend and Cedar Creek (Old Hickory; Recreation.gov pages don't mention a dump station, so find an official source or skip), Lock A (Cheatham), Defeated Creek and Salt Lick Creek (Cordell Hull), Floating Mill, Ragland Bottom and Long Branch (Center Hill), Dale Hollow campgrounds, Bumpus Mills.
5. **Land Between the Lakes South Welcome Station (Dover).** Crowd lists say it has a free dump. The official LBL rates sheet doesn't mention one, so find an official source before listing.
6. **TVA campgrounds** (Cherokee Dam, Douglas Dam, Melton Hill Dam, Loyston Point) from tva.com.
7. **West Tennessee truck stops** (Memphis, Jackson). State parks there are done (Meeman-Shelby, T.O. Fuller, Chickasaw, Natchez Trace, Reelfoot Lake South), and so is Love's #244 Jackson. Lead: a crowd listing (Campendium) for a Love's in Memphis; check Love's own store page.
8. **Guide: "Free RV dump stations in Tennessee (and the catch)"** once there are enough verified free stations.
9. **Season sweep in spring 2027:** Cosby, Look Rock and the Percy Priest campgrounds (post 2027 dates when NPS and the Corps publish them); David Crockett Campground 1 (posted season starts Mar 1); Roan Mountain (off-season ends Apr 15).

## Watch

- **Love's #330 Baxter:** the newest crowd review (Mar 30, 2026) said the dump was closed for construction. Love's page listed RV Dump Service with no notice on 2026-11-06, so it's listed as open. Re-check it first in the next re-check sweep. (Campendium on 2026-11-08: the Mar 30 review is still the newest.)
- **Standing Stone:** listed as closed (campground renovation since July 7, 2025; park expects it to last until late 2026). Re-check the camping page every week or so and flip it back once the park says the campground is open.
- **Norris Dam:** both campgrounds closed for renovation with a 2026 reopening planned. When they reopen, check whether the current camping page lists a dump station before adding it.
- **Roan Mountain:** off-season Nov 1 – Apr 15 (most bathhouses closed; dump hours not stated), and the upper campground is closed after Hurricane Helene. Listed as "call first."
- **Pickett:** the park page says the campground is closed for renovations to the bathhouse and campground (no dates). When it reopens, check the camping page for a dump station.
- **Cove Lake:** the park page says a newly renovated campground opens in 2027. Check its camping page then.
- **Natchez Trace:** Cub Lake Campground 2 and the Wrangler Campground both have dump stations but are closed for renovations. Add them when the park says they've reopened.
- **Old Stone Fort:** listed as open (the park says its dump is open year-round), but a bridge at the park is closed for construction and the notice doesn't name it. Re-check in the next sweep.
- **Percy Priest (Seven Points, Anderson Road, Poole Knobs):** re-checked 2026-11-07 (dump and drinking water on all three Recreation.gov pages). The Corps' lake page (lrd.usace.army.mil) still shows only 2024 seasons; no 2026 dates posted anywhere we found.
- **Fetch tip:** the page fetcher refused URLs that hadn't shown up in a search result that run (PROVENANCE_REQUIRED). Search for the exact page first, then fetch it.
- **Fetch tip (state parks):** tnstateparks.com still serves old `/parks/campground/<park>` pages next to the current `/parks/<park>/camping` pages. Use the current ones; old ones can be stale (Norris Dam's old page lists dump stations and no closure). Reelfoot's old URL is the exception: it serves the current page (canonical `/parks/reelfoot-lake/camping`). The statewide camping brochure PDF returned a client error.
- **Fetch tip (state parks, 2026-11-08):** current camping pages for Pickett, Bledsoe Creek, Panther Creek, Cove Lake and Mousetail Landing return a client error. The reservation site (`reserve.tnstateparks.com/<park>/camping`) loads, but it describes sites, not dump stations. Edgar Evins's older `/parks/campground/` URL serves the current page (canonical `/parks/edgar-evins/camping`); the older URLs for Warriors' Path and Davy Crockett Birthplace return legacy plain-text pages with stale notices.

## Site to-dos (need Micaiah)

- **Amazon Associates** tag → `config.json` `amazon_tag` (gear links in the how-to guide turn into affiliate links).
- **Suggestion form** (Tally) URL → `config.json` `suggest_form_url`. (No DumpCheck form exists in the connected Tally account yet.)
- **Google Search Console** verification → `config.json` `search_console_verification`.
- Optional RV programs to apply to later: Good Sam, Harvest Hosts, RV gear brands. Paste approved links in chat; Yeha never adds them on its own.

## Done

- 2026-11-05: Launched DumpCheck: 11 verified stations (4 Smokies NPS, 3 Corps on J. Percy Priest Lake, 4 Love's), a statewide directory with status filters, and 4 guides (rest areas, Smokies, Nashville, how to use a dump station).
- 2026-11-06: I-40 Love's: 4 verified (Jackson #244, Holladay #791, Baxter #330, Newport #796), plus an I-40 section in the rest-area guide. Love's #369 Dickson lists no RV dump, so it isn't listed.
- 2026-11-07: Tennessee State Parks: 7 verified stations at 6 parks (Rock Island open; Cedars of Lebanon, Tims Ford Main and Fairview, Reelfoot Lake South and Roan Mountain call first; Standing Stone closed for renovations). Nashville guide gets Cedars of Lebanon and a "skip Montgomery Bell" note; home page shows a Closed count.
- 2026-11-08: Tennessee State Parks, round 2: 10 verified (Old Stone Fort open; Meeman-Shelby, T.O. Fuller, Chickasaw, Natchez Trace Cub Lake 1, Paris Landing, David Crockett, Edgar Evins, Warriors' Path and Panther Creek call first). Now 17 stations at 16 parks, which unlocks the state park guide.
