# kuams🐧

KUAMS (Kansai University Autonomous Measurement System) ROS 2パッケージ

<img src="./docs/kuams.png" style="width: 500px; height: auto;">

## 目次
<!-- TOC -->

- [概要](#概要)
- [ハードウェア & 開発環境](#ハードウェア--開発環境)
- [パッケージ構成](#パッケージ構成)
- [インストール方法](#インストール方法)
- [使用方法](#使用方法)

<!-- /TOC -->

## 概要
ROS 2とNavigation2を用いてナビゲーションを行うためのパッケージを提供します。
実機には関西大学 計測システム研究室が制作するKUAMSを使用します。

## ハードウェア & 開発環境
- ハードウェア
    - WHILL Model CR
        - 製品ページ: [https://whill.inc/jp/model-cr](https://whill.inc/jp/model-cr)
    - Livox Mid-360:
        - 製品ページ: [https://www.livoxtech.com/jp/mid-360](https://www.livoxtech.com/jp/mid-360)

- 開発環境
    - Ubuntu Linux - Jammy Jellyfish (22.04)
    - ROS 2 Humble Hawksbill

## パッケージ構成
- `kuams` : KUAMSのメタパッケージ
- `kuams_bringup` : KUAMS、各種センサの起動を行うためのlaunchファイルを提供するパッケージです。
- `kuams_description` : KUAMSの物理モデルやURDFモデル、Meshファイルを含むパッケージです。
- `kuams_navigation` : Nav2の起動を行うためのlaunchファイルを提供するパッケージです。
- `kuams_slam` : slam_toolboxを起動するためのlaunchファイルを提供するパッケージです。
- `kuams_teleop` : Joyコントローラを使用してKUAMS3を操作するためのコード、launchファイルを提供するパッケージです。

## インストール方法  
以下の手順に沿って各パッケージのインストールを行ってください  
1. **ROS 2 Humble**のセットアップ:  
   [こちら](https://docs.ros.org/en/humble/Installation.html)の手順に従って、ROS 2 Humbleをインストールしてください。

2. [**kuams**](https://github.com/kzm784/kuams) のセットアップ:
   ```bash
   mkdir -p ~/kuams_ws/src
   cd ~/kuams_ws/src
   git clone https://github.com/kzm784/kuams.git
   cd ~/kuams_ws
   rosdep update && rosdep install --from-paths src --ignore-src -y
   colcon build
    ```

3. [**ros2_whill**](https://github.com/kzm784/ros2_whill) のセットアップ:
    ```bash
    sudo apt install ros-humble-xacro
    cd ~/kuams_ws/src
    git clone -b crystal-devel https://github.com/WHILL/ros2_whill_interfaces.git
    git clone https://github.com/kzm784/ros2_whill.git
    cd ~/kuams_ws
    rosdep update && rosdep install --from-paths src --ignore-src -y
    colcon build 
    ```
4. [**Livox SDK2**](https://github.com/Livox-SDK/Livox-SDK2.git) のセットアップ:
   ```bash
   git clone https://github.com/Livox-SDK/Livox-SDK2.git
   cd ~/Livox-SDK2/
   mkdir build
   cd build
   cmake .. && make -j4
   sudo make install
   ```

5. [**livox_ros_driver2**](https://github.com/Livox-SDK/livox_ros_driver2) のセットアップ:
   ```bash
   cd ~/kuams_ws/src
   git clone https://github.com/Livox-SDK/livox_ros_driver2.git
   mv livox_ros_driver2/package_ROS2.xml livox_ros_driver2/package.xml
   cd ~/kuams_ws
   colcon build --packages-select livox_ros_driver2 --cmake-args -DROS_EDITION="ROS2" -DHUMBLE_ROS="humble" --symlink-install
    ```

6. [**waypoint_manager**](https://github.com/kzm784/waypoint_manager) のセットアップ:
    ```bash
   cd ~/kuams_ws/src
   git clone https://github.com/kzm784/waypoint_manager.git
   cd ~/kuams_ws
   rosdep update && rosdep install --from-paths src --ignore-src 
   colcon build
    ```

7. [**lidar_localization_ros2**](https://github.com/rsasaki0109/lidar_localization_ros2) のセットアップ:
    ```bash
   cd ~/kuams_ws/src
   git clone https://github.com/rsasaki0109/lidar_localization_ros2.git
   git clone https://github.com/rsasaki0109/ndt_omp_ros2.git
   cd ~/kuams_ws
   rosdep update && rosdep install --from-paths src --ignore-src 
   colcon build
    ```

## 使用方法
- **kuamsの起動**:    
    ⚠️ **注意**: 初期セットアップ時にudevルールを編集し、USBデバイスのシンボリックリンクを作成してください。
    ```bash
    sudo mv ~/kuams_ws/src/kuams/docs/99-whill-serial.rules /etc/udev/rules.d/
    sudo udevadm control --reload
    ```
    WHILL Model CRとPCをシリアル接続し、以下のコマンドを実行して各種センサを含むkuamsの実機を起動します。
    ```bash
    cd kuams_ws
    source install/setup.bash
    ros2 launch kuams_bringup kuams.launch.py
    ```

- **Joyコントローラーを用いたkuams3の操縦**:
    JoyコントローラーとPCを接続した後、以下のコマンドを実行しkuamsを操縦することができます。
    ```bash
    cd kuams_ws
    source install/setup.bash
    ros2 launch kuams_teleop kuams3_teleop.launch.py
    ```
    ボタンの割当、速度調節のパラメータは`kuams_teleop/config/config_kuams_teleop.yaml`を編集してください。
    ```yaml
    kuams_teleop:
        ros__parameters:
            axis_linear_x: 1     # 前後方向の速度を操作するジョイスティック軸
            axis_angular: 0      # 回転速度を操作するジョイスティック軸
            axis_deadman: 5      # デッドマンスイッチのボタン番号
            scale_linear: 0.3    # 直線速度のスケール（最大速度）
            scale_angular: 0.9   # 回転速度のスケール（最大回転速度）
    ```

- **Navigation2を用いたウェイポイントナビゲーション**:  
    ⚠️ **注意**: ホームディレクトリに Navigation_data ディレクトリを作成し、ウェイポイントナビゲーションに必要なデータをその中に準備してください。
    ```
    naviagtion_data
        │
        ├── rinpukan
        │       ├── rinpukan.pcd        # 3次元地図
        │       ├── rinpukan.pgm        # 2次元地図
        │       ├── rinpukan.yaml       # 2次元地図情報設定ファイル
        │       ├── rinpukan_wp.csv     # ウェイポイントデータ
        │       └── rinpukan_mc.csv     # 地図切り替え設定ファイル (オプション)
        │
        └── ... # 以降も同じ形式
    ```
    必要なデータを準備したら、以下のコマンドで環境変数を設定してください。
    ```bash
    echo 'export NAVIGATION_DATA_DIR=/home/$USER/navigation_data' >> ~/.bashrc
    echo 'export NAVIGATION_DATA_NAME=rinpukan' >> ~/.bashrc
    ```

