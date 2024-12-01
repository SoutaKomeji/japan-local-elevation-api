import os
from osgeo import gdal

def find_tiff_files(directories):
    """複数のディレクトリからTIFFファイルを収集"""
    tiff_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.tif') or file.endswith('.tiff'):
                    tiff_files.append(os.path.join(root, file))
    return tiff_files

def create_vrt(input_files, vrt_file):
    """入力ファイルのリストをVRTに変換"""
    gdal.BuildVRT(vrt_file, input_files)

def convert_vrt_to_tiff(vrt_file, output_file):
    """VRTを最終的なTIFFファイルに変換"""
    gdal.Translate(output_file, vrt_file)

def main(input_directories, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 複数のディレクトリからTIFFファイルを収集
    tiff_files = find_tiff_files(input_directories)
    if not tiff_files:
        print("No TIFF files found in the specified directories.")
        return
    
    vrt_file = os.path.join(output_directory, 'temporary.vrt')
    output_file = os.path.join(output_directory, 'merged_all.tif')
    
    # VRT作成とTIFFへの変換
    create_vrt(tiff_files, vrt_file)
    convert_vrt_to_tiff(vrt_file, output_file)
    
    # 一時的なVRTファイルを削除
    os.remove(vrt_file)
    
    print(f"All TIFF files from {len(input_directories)} directories have been merged into {output_file}")

input_directories = [
    './tif_jgd2000',
    './tif_jgd2011'
]
output_directory = './tif_merged'

main(input_directories, output_directory)
