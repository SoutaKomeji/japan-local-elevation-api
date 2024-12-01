# 各種ディレクトリ設定
BASE_DIR=$(pwd) # スクリプト実行ディレクトリ
CAB_DIR="$BASE_DIR/cab" # CABファイルの格納ディレクトリ
DEST_DIR="$BASE_DIR/xml_output" # XMLファイルを移動する先のディレクトリ
TEMP_DIR="$BASE_DIR/temp_extract" # 一時ディレクトリ

# JGDフォルダの作成
JGD2000_DIR="$BASE_DIR/xml_jgd2000"
JGD2011_DIR="$BASE_DIR/xml_jgd2011"
mkdir -p "$CAB_DIR" "$TEMP_DIR" "$DEST_DIR" "$JGD2000_DIR" "$JGD2011_DIR"

# プログレスバーの関数
print_progress_bar() {
    local progress=$1
    local total=$2
    local percent=$((progress * 100 / total))
    local bars=$((percent / 2)) # プログレスバーの長さを50にする
    local spaces=$((50 - bars)) # 残りのスペース
    printf "\r[%-50s] %d%%" "$(printf '#%.0s' $(seq 1 $bars))$(printf ' %.0s' $(seq 1 $spaces))" "$percent"
}

# CABファイルのリスト取得
CAB_FILES=("$CAB_DIR"/*.cab)
TOTAL_CAB=${#CAB_FILES[@]}
CURRENT_CAB=0

# CABファイルの処理
echo "Step 1: Extracting CAB files..."
if [ "$TOTAL_CAB" -eq 0 ]; then
    echo "No CAB files found in $CAB_DIR."
else
    for CAB_FILE in "${CAB_FILES[@]}"; do
        CURRENT_CAB=$((CURRENT_CAB + 1))
        print_progress_bar "$CURRENT_CAB" "$TOTAL_CAB"
        
        cabextract -d "$TEMP_DIR" "$CAB_FILE" > /dev/null 2>&1
    done
fi
echo ""

# ZIPファイルのリスト取得
ZIP_FILES=($(find "$TEMP_DIR" -name "*.zip"))
TOTAL_ZIP=${#ZIP_FILES[@]}
CURRENT_ZIP=0

# ZIPファイルの処理
echo "Step 2: Extracting ZIP files..."
if [ "$TOTAL_ZIP" -eq 0 ]; then
    echo "No ZIP files found in $TEMP_DIR."
else
    for ZIP_FILE in "${ZIP_FILES[@]}"; do
        CURRENT_ZIP=$((CURRENT_ZIP + 1))
        print_progress_bar "$CURRENT_ZIP" "$TOTAL_ZIP"
        
        unzip -d "$TEMP_DIR" "$ZIP_FILE" > /dev/null 2>&1
    done
fi
echo ""

# XMLファイルの移動
echo "Step 3: Moving XML files..."
XML_FILES=($(find "$TEMP_DIR" -name "*.xml"))
TOTAL_XML=${#XML_FILES[@]}
CURRENT_XML=0

if [ "$TOTAL_XML" -eq 0 ]; then
    echo "No XML files found in $TEMP_DIR."
else
    for XML_FILE in "${XML_FILES[@]}"; do
        CURRENT_XML=$((CURRENT_XML + 1))
        print_progress_bar "$CURRENT_XML" "$TOTAL_XML"
        
        mv "$XML_FILE" "$DEST_DIR"
    done
fi
echo ""

# XMLファイルの分別
echo "Step 4: Sorting XML files into JGD2000 and JGD2011..."
cd "$DEST_DIR" || exit
TOTAL_XML_SORT=$(find . -name "*.xml" | wc -l)
CURRENT_XML_SORT=0

if [ "$TOTAL_XML_SORT" -eq 0 ]; then
    echo "No XML files to sort."
else
    for FILE in *.xml; do
        CURRENT_XML_SORT=$((CURRENT_XML_SORT + 1))
        print_progress_bar "$CURRENT_XML_SORT" "$TOTAL_XML_SORT"

        if grep -q '<gml:Envelope srsName="fguuid:jgd2011.bl">' "$FILE"; then
            mv "$FILE" "$JGD2011_DIR"
        elif grep -q '<gml:Envelope srsName="fguuid:jgd2000.bl">' "$FILE"; then
            mv "$FILE" "$JGD2000_DIR"
        fi
    done
fi
echo ""

# 一時ディレクトリの削除
echo "Step 5: Cleaning up..."
rm -rf "$TEMP_DIR"
echo "Cleanup complete!"

echo "All steps completed successfully!"
