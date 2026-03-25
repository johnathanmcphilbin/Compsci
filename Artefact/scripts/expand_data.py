#!/usr/bin/env python3
"""
Expand `ireland_sample_points.csv` by adding N extra points near each existing county point.
This creates extra coverage for the demo (small offsets only, stays inside Ireland bbox).
"""
import csv, os, random
BASE = os.path.dirname(__file__)
CSV = os.path.join(BASE, 'ireland_sample_points.csv')

LAT_MIN, LAT_MAX = 51.3, 55.4
LON_MIN, LON_MAX = -10.7, -5.3
EXTRA_PER_COUNTY = 3

# read existing
rows = []
with open(CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for r in reader:
        rows.append(r)

# build map of counts
counts = {}
max_id = {}
for r in rows:
    c = r['county']
    counts[c] = counts.get(c, 0) + 1
    pid = r.get('point_id','')
    if pid and '-' in pid:
        try:
            n = int(pid.split('-')[-1])
            max_id[c] = max(max_id.get(c,0), n)
        except:
            pass

new_rows = []
for r in rows:
    county = r['county']
    base_lat = float(r['lat'])
    base_lon = float(r['lon'])
    start = max_id.get(county,0) + 1
    for i in range(EXTRA_PER_COUNTY):
        # small random offsets (~0.01-0.05 degrees)
        lat = base_lat + random.uniform(-0.035, 0.035)
        lon = base_lon + random.uniform(-0.05, 0.05)
        # clamp to Ireland bbox
        lat = min(max(lat, LAT_MIN), LAT_MAX)
        lon = min(max(lon, LON_MIN), LON_MAX)
        elev = max(0, float(r.get('elevation_m',0)) + random.uniform(-30,30))
        soil = min(0.95, max(0.05, float(r.get('soil_moisture_index_0_1',0)) + random.uniform(-0.07,0.07)))
        rain = max(0, float(r.get('annual_rainfall_mm',0)) + random.uniform(-80,80))
        flood = min(0.99, max(0.01, float(r.get('flood_susceptibility_0_1',0)) + random.uniform(-0.06,0.06)))
        soil_type = r.get('soil_type','Podzol')
        sop = float(r.get('suitability_oak') or 0) + random.uniform(-0.06,0.06)
        sal = float(r.get('suitability_alder') or 0) + random.uniform(-0.06,0.06)
        ssp = float(r.get('suitability_scots_pine') or 0) + random.uniform(-0.06,0.06)
        sb = float(r.get('suitability_birch') or 0) + random.uniform(-0.06,0.06)
        recommended = r.get('recommended_species','Oak')
        constraints = r.get('constraints','')
        pid = f"{county[:3].upper()}-{start+i:02d}"
        new = {
            'county': county,
            'point_id': pid,
            'lat': f"{lat:.6f}",
            'lon': f"{lon:.6f}",
            'elevation_m': f"{elev:.1f}",
            'soil_moisture_index_0_1': f"{soil:.3f}",
            'annual_rainfall_mm': f"{rain:.1f}",
            'flood_susceptibility_0_1': f"{flood:.3f}",
            'soil_type': soil_type,
            'suitability_oak': f"{max(0,min(1,sop)):.3f}",
            'suitability_alder': f"{max(0,min(1,sal)):.3f}",
            'suitability_scots_pine': f"{max(0,min(1,ssp)):.3f}",
            'suitability_birch': f"{max(0,min(1,sb)):.3f}",
            'recommended_species': recommended,
            'constraints': constraints,
        }
        new_rows.append(new)
    max_id[county] = start + EXTRA_PER_COUNTY - 1

# append to CSV
with open(CSV, 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    for nr in new_rows:
        writer.writerow(nr)

print(f"Appended {len(new_rows)} generated points ({EXTRA_PER_COUNTY} per existing point).")
