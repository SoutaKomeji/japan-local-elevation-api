import elevation_service as elevation_service
import os

tif_path = f"{os.path.dirname(os.path.abspath(__file__))}/tool/tif_merged/merged_all.tif"
elevation_service_ins = elevation_service.ElevationService(tif_path)

# # 函館駅
# lat = 41.7736
# lon = 140.7266

# ロープウェイ山麓駅
lat = 41.760851
lon = 140.714151

# # 旧函館区公会堂 
# lat = 41.765174
# lon = 140.7091088
elevation = elevation_service_ins.get_elevation(lat, lon)
print(f"lat: {lat}, lon: {lon}, elevation: {elevation}")