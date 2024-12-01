import os
from osgeo import gdal

jgd2000_tif_path = './tif_jgd2000'
jgd2011_tif_path = './tif_jgd2011'

def main():
    # EPSGコードの定義
    jgd2000_epsg = 4612
    jgd2011_epsg = 6668
    dst_epsg = 4326

    # jgd2000 の処理
    if os.path.exists(jgd2000_tif_path):
        print(f"Processing files in {jgd2000_tif_path}...")
        batch_reproject_tiffs(jgd2000_tif_path, jgd2000_epsg, dst_epsg)

    # jgd2011 の処理
    if os.path.exists(jgd2011_tif_path):
        print(f"Processing files in {jgd2011_tif_path}...")
        batch_reproject_tiffs(jgd2011_tif_path, jgd2011_epsg, dst_epsg)

def reproject_tiff(input_tiff, output_tiff, src_epsg, dst_epsg):
    src_ds = gdal.Open(input_tiff)
    if src_ds is None:
        print(f"Unable to open {input_tiff}")
        return

    dst_wkt = f'EPSG:{dst_epsg}'
    gdal.Warp(output_tiff, src_ds, dstSRS=dst_wkt, srcSRS=f'EPSG:{src_epsg}')
    print(f"Reprojected {input_tiff} to {output_tiff} with EPSG:{dst_epsg}")

def batch_reproject_tiffs(input_dir, src_epsg, dst_epsg):
    # 入力ディレクトリ内のすべての TIFF ファイルをループ処理
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.tif') or filename.lower().endswith('.tiff'):
            input_tiff = os.path.join(input_dir, filename)
            output_tiff = os.path.join(input_dir, filename)
            reproject_tiff(input_tiff, output_tiff, src_epsg, dst_epsg)

# このファイルが直接実行されたときにのみ main を呼び出す
if __name__ == "__main__":
    main()
