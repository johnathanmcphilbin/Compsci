import csv
import json
import math
import statistics

# File paths for data input and results
SAMPLE_POINTS_CSV = 'data/ireland_sample_points.csv'
COUNTY_SUMMARY_CSV = 'data/ireland_county_landscape_summary.csv'
OUTPUT_JSON = 'forest_model/results.json'
OUTPUT_CSV = 'forest_model/results_summary.csv'

def load_sample_points(path):
    # Reads the CSV points and converts numeric strings to floats
    pts = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['lat'] = float(row['lat']) if row.get('lat') else None
            row['lon'] = float(row['lon']) if row.get('lon') else None
            row['elevation_m'] = float(row.get('elevation_m') or 0)
            row['soil_moisture'] = float(row.get('soil_moisture_index_0_1') or 0)
            row['annual_rainfall_mm'] = float(row.get('annual_rainfall_mm') or 0)
            pts.append(row)
    return pts

def load_microbit_data(path):
    # This loads the CSV that comes from the microbit serial link
    out = []
    try:
        with open(path, newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            # Coordinates for France bounding box (to keep origin ambiguous)
            minLat, maxLat = 43.0, 50.0
            minLon, maxLon = -1.0, 7.0
            
            for idx, row in enumerate(rows, start=1):
                # skip rows that repeat the header if the microbit restarted
                if row.get('Temperature') == 'Temperature':
                    continue
                    
                temp = float(row.get('Temperature') or row.get('temperature') or 0)
                moist_raw = float(row.get('Moisture') or row.get('moisture') or 0)
                light = float(row.get('Light') or row.get('light') or 0)
                sound = float(row.get('Sound') or row.get('sound') or 0)
                
                soil_moist = max(0.0, min(1.0, moist_raw / 700.0))
                annual_rain = 900.0
                flood = max(0.0, min(1.0, (soil_moist * (annual_rain / 1200.0))))
                
                # generate deterministic coords for France
                lat_i = minLat + (abs(math.sin(idx + 3)) % 1) * (maxLat - minLat)
                lon_i = minLon + (abs(math.sin(idx + 13)) % 1) * (maxLon - minLon)
                
                out.append({
                    'point_id': f'microbit_{idx}',
                    'county': 'Field Test (Ambiguous)',
                    'lat': lat_i,
                    'lon': lon_i,
                    'elevation_m': 45.0,
                    'soil_moisture': soil_moist,
                    'annual_rainfall_mm': annual_rain,
                    'flood_susceptibility': flood,
                    'temperature_c_sensor': temp,
                    'light_sensor': light,
                    'sound_sensor': sound,
                    'raw_status': row.get('Status') or row.get('status') or ''
                })
    except FileNotFoundError:
        return []
    return out

def compute_point_risk(point, temp_anomaly=0.0, rain_factor=1.0):
    # Main algorithm to compute wildfire risk score (0-1)
    soil_moisture = float(point.get('soil_moisture') or 0.0)
    annual_rainfall = float(point.get('annual_rainfall_mm') or 0.0) * rain_factor
    elevation = float(point.get('elevation_m') or 0.0)

    # Use sensor temperature if available, otherwise estimate from elevation
    if 'temperature_c_sensor' in point:
        temp = point['temperature_c_sensor'] + temp_anomaly
    else:
        base_temp = 12.0 - (elevation / 200.0) - ((annual_rainfall - 900.0) / 1500.0)
        temp = base_temp + temp_anomaly

    # Adjustment for soil dryness based on heat
    soil_moisture_adj = soil_moisture - (temp_anomaly * 0.02)
    if rain_factor != 1.0 and soil_moisture > 0:
        soil_moisture_adj *= rain_factor
    
    # clamp values between 0 and 1
    soil_moisture_adj = max(0.02, min(0.9, soil_moisture_adj))
    rain_norm = max(0.0, min(1.0, (annual_rainfall - 600.0) / 1900.0))
    temp_index = max(0.0, min(1.0, (temp + 5.0) / 30.0))

    # Incorporate light sensor (if available) as a proxy for drying/sun exposure
    # higher light = slightly higher risk
    light_adj = 0.0
    if 'light_sensor' in point:
        light_adj = (float(point['light_sensor']) / 255.0) * 0.05

    # Incorporate sound sensor (if available) as a proxy for immediate rainfall/wind
    # higher sound = slightly lower wildfire risk (assuming rain)
    sound_adj = 0.0
    if 'sound_sensor' in point:
        sound_adj = (float(point['sound_sensor']) / 255.0) * 0.05

    # Tree metrics (fake density for the model)
    h = abs(hash(point.get('point_id', '')))
    tree_density = 50 + (h % 551)
    density_index = max(0.0, min(1.0, (tree_density - 50) / 550.0))

    # Weighting factors for the final risk index
    risk = (
        0.50 * (1.0 - soil_moisture_adj) + 
        0.25 * (1.0 - rain_norm) +          
        0.15 * temp_index +                 
        0.10 * density_index +
        light_adj -
        sound_adj
    )
    return {
        'point_id': point.get('point_id'),
        'county': point.get('county'),
        'lat': point.get('lat'),
        'lon': point.get('lon'),
        'risk': round(max(0.0, min(1.0, risk)), 4),
        'temperature_c': round(temp, 2),
        'soil_moisture_adj': round(soil_moisture_adj, 4),
        'annual_rainfall_mm': round(annual_rainfall, 1),
    }

def run_model():
    pts = load_sample_points(SAMPLE_POINTS_CSV)
    micro_pts = load_microbit_data('data/microbit_sensor_data.csv')
    if micro_pts:
        pts.extend(micro_pts)

    scenarios = {
        'baseline': {'temp_anomaly': 0.0, 'rain_factor': 1.0},
        'scenario_temp_plus_3C': {'temp_anomaly': 3.0, 'rain_factor': 1.0},
        'scenario_rain_minus_30pct': {'temp_anomaly': 0.0, 'rain_factor': 0.7},
    }

    results = {'details': {}, 'points': {}}
    for name, cfg in scenarios.items():
        pts_out = [compute_point_risk(p, cfg['temp_anomaly'], cfg['rain_factor']) for p in pts]
        results['points'][name] = pts_out
        
        # summary stats
        risks = [p['risk'] for p in pts_out]
        results['details'][name] = {
            'n_points': len(risks),
            'mean_risk': round(statistics.mean(risks), 4) if risks else 0,
            'high_risk_count': sum(1 for r in risks if r >= 0.75)
        }

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(results, f, indent=2)

    # CSV summary per county
    csv_rows = []
    for name in scenarios:
        per_county = {}
        for p in results['points'][name]:
            per_county.setdefault(p['county'], []).append(p['risk'])
        for county, vals in per_county.items():
            csv_rows.append({'scenario': name, 'county': county, 'mean_risk': round(statistics.mean(vals), 4)})

    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['scenario', 'county', 'mean_risk'])
        writer.writeheader()
        writer.writerows(csv_rows)
    return results

if __name__ == '__main__':
    print('Starting the disaster risk model processing...')
    run_model()
    print('Done. Results saved to JSON and CSV.')
