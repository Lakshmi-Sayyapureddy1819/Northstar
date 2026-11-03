/**
 * The seven Hyderabad tech localities the seed dataset (Slice 2,
 * apps/api/scripts/data/hyderabad_companies.json) is distributed across.
 *
 * A small frontend constant, not a backend concept — `geo` has no
 * "Locality" entity for seven well-known, unchanging landmarks (see
 * docs/features/phase1/slice-3-map-experience.md, "Search by location").
 * If the seed data's localities ever change, update this list to match.
 */
export interface Locality {
  name: string;
  latitude: number;
  longitude: number;
}

export const LOCALITIES: Locality[] = [
  { name: "Madhapur", latitude: 17.4483, longitude: 78.3915 },
  { name: "Hitech City", latitude: 17.4435, longitude: 78.3772 },
  { name: "Gachibowli", latitude: 17.4401, longitude: 78.3489 },
  { name: "Financial District", latitude: 17.4126, longitude: 78.3425 },
  { name: "Kondapur", latitude: 17.4615, longitude: 78.3636 },
  { name: "Raidurg", latitude: 17.4344, longitude: 78.3699 },
  { name: "Nanakramguda", latitude: 17.418, longitude: 78.3407 },
];

/** Default map center: the geographic middle of the seven localities. */
export const HYDERABAD_CENTER: Locality = {
  name: "Hyderabad",
  latitude: 17.4326,
  longitude: 78.3577,
};

export const DEFAULT_RADIUS_KM = 10;
