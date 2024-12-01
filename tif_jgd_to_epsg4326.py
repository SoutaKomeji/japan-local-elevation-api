import os
from osgeo import gdal

# 入力・出力ディレクトリの設定（上書きするため同じディレクトリを使用）
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

def reproject_tiff(input_tiff, src_epsg, dst_epsg):
    """TIFF ファイルを再投影し、同じ場所に上書き保存する"""
    # 入力ファイルを開く
    src_ds = gdal.Open(input_tiff)
    if src_ds is None:
        print(f"Unable to open {input_tiff}")
        return

    # 出力ファイル名（同じ場所に上書き）
    temp_output_tiff = input_tiff + ".tmp"

    # 再投影を実行
    dst_wkt = f'EPSG:{dst_epsg}'
    gdal.Warp(temp_output_tiff, src_ds, dstSRS=dst_wkt, srcSRS=f'EPSG:{src_epsg}')
    os.replace(temp_output_tiff, input_tiff)  # 一時ファイルを元のファイルに上書き
    print(f"Reprojected {input_tiff} to EPSG:{dst_epsg}")

def batch_reproject_tiffs(input_dir, src_epsg, dst_epsg):
    """ディレクトリ内のすべての TIFF ファイルを再投影して上書きする"""
    # 入力ディレクトリ内のすべての TIFF ファイルをループ処理
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.tif') or filename.lower().endswith('.tiff'):
            input_tiff = os.path.join(input_dir, filename)
            reproject_tiff(input_tiff, src_epsg, dst_epsg)

# このファイルが直接実行されたときにのみ main を呼び出す
if __name__ == "__main__":
    main()
