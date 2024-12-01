import elevation_service as elevation_service
import os

tif_path = f"{os.path.dirname(os.path.abspath(__file__))}/tool/tif_merged/merged_all.tif"
elevation_service_ins = elevation_service.ElevationService(tif_path)

lat = 35.6895
lon = 139.6917
elevation = elevation_service_ins.get_elevation(lat, lon)
print(f"lat: {lat}, lon: {lon}, elevation: {elevation}")