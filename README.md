# Face_Hugster
*Japanese follows English

How to use:

Save Selection Module:

    #This module allows the user to save a wide range of selection into the manager. User can select vertices, 
    #edges, UVs, different geometries, etc.
    
    1)  Selection Manager:
        - Make a selection and use the save button to name and save into the manager. 
        - Click on the name to select the selection set.
        - to delete, click on the name and press the delete key, or use Clear Selection button for all.
        
    2)  Save Selection to File:
        - Saves everything in the selection manager to a text file where your Maya scene is located.
        - To reload the selection, press the load selection button.
        ** - will not work if the Maya file is not saved onto disk.
        
Duplicate From Selection Module:

    #This module allows the user to make a copy of the selected faces into a new geometry. 
    #It duplicates the geometry, renames it, copies the selection, and delete the unselected faces. 
    #If geometry is dense, this will be take time.
    
    1) Duplicate Selection:
        - Select a list from the Selection Manager and click on the button to make a duplicate geometry
          from the selection.
          
Palette Manager Module:

    #This module allows the user to add the geometry to be copied into a list.

    1)  Palette Manager:
        - Select the geometry to be copied and click on Set To Palette to put into the Palette Manager.
        - to delete, click on the name and press the delete key or use Clear Palette for all.
        ** For best results, set a good pivot point. Do not freeze translation transform or geometry
           will not be at correct position.

Run Module:

    #Runs the tool as either instances or duplicates.

    1)  Run Command:
        - To run the tool, please do the following:
           1) Select a list from the Selection Manager that you wish to populate.
           2) Click on a geometry that you wish to copy.
           3) Select whether you want to run as instances or duplicates. Default is duplicate.
           4) Hit run button.
           ** Will not work if face selection is not active in viewport, so remember to 
              select from Selection Manager before running.
              
Rotate Constraint Module:

    #This module allows the user to orient constraint all geometries under a selected group to a locator. 
    #This allows the user flexibility in rotating multiple geometries with one control.
          
    1)  Constrain Geometry:
        - Select the group node and click the button.
        
    2)  Rehook Constrain:
        - This allows the user to re-orient geometries to a previously set locator
          (group name and locator name must match).
      
    3)  Break Constrain:
        - Deletes the constrains after rotation is done. 
          
          

--------------------------------------------------------
Face Hugster

フェースに沿ってオブジェクトを配置する機能です。

使い方：

■Save Selection（選択保存)

    いくつかの要素（頂点、エッジ、フェース、UV）又はオブジェクト（複数同時選択可）を保存しておく機能です。

        1) Selection Manager
            - 選択保存したい要素又はオブジェクトを選択、[Save Selection]ボタンを押し、名前を付けて保存します。
            - Selection Managerから、名前を付けて保存した選択セットを選択することができます。
            - 選択セットを個々に削除するには、Selection Managerから名前を選択し、キーボード[Delete]を押します。
              全ての選択セットを削除したい場合は、[Clear All Selection]ボタンを押します。

        2) Save And Load To File
            - 選択セットは[Save Selection To File]ボタンで、テキストファイルとして書き出し、保存しておくことができます。
             （この時、Selection Managerに表示された全ての選択セットが保存されます。）
              テキストファイルは、現在作業しているMayaのシーンデータが保存された場所と同一パスに保存されます。
            - 保存した選択セットをロードするには、[Load Selection]を押します。
              ※シーンがセーブされていない場合は動作しません。


■Duplicate From Selection（選択セットから複製）

    この機能は、選択保存したフェースを新しいジオメトリとして複製する事のできる機能です。
    ジオメトリーが重たい場合、少し時間がかかります。

        1) Duplicate Selection
            - Selection Managerのリストから複製したい選択セットを選び、[Duplicate Seleciton]を押します。

■Palette Manager（パレットマネージャー）

    ジオメトリーをリストに保存しておく機能です。

        1) Palette Manager
            - 保存したいジオメトリーを選択、[Set To Palette]ボタンを押し、Palette Managerに保存します。
            - 個々に削除するには、Palette Managerから名前を選択し、キーボード[Delete]を押します。
              全てを削除したい場合は、[Clear Palette]ボタンを押します。
              ※最良の結果を出すためには、ピボット位置を正確な位置にしてください。トランスフォームをフリーズする際は、
              0地点で行ってください。

■Run Face Hugster（Face Hugsterの実行）

    Face Hugsterは、フェースに沿ってオブジェクトを配置する機能です。
        [RunCommand: Duplicate Type:]にて、複製配置するオブジェクトがインスタンスかコピーかを選択します。

        1)Run…ツール実行の際は、以下の手順で行ってください。
            1) Selection Managerから、フェースに沿って配置させたい側の選択セットを選択します。
            2) Palette Managerから、フェースに沿って配置したい側のジオメトリを選択します。
            3) [Run Face Hugster/ Duplicate Type:]にて、複製するオブジェクトがインスタンスかコピーかを選択します。
            4) [Run]ボタンを押して実行します。
            ※ビューポート上で、1)と2)で選択したものが選ばれているかどうかを確認してから実行してください。

■Rotate Constraint Module

    選択したグループ内のジオメトリをロケータでオリエントコンストレイントにする機能です。
    複数のジオメトリを1つのコントロールで回転させます。

        1）Constrain Geometry：
            グループノードを選択して、[Constrain Geometry]ボタンを押してください。

        2) Rehook Constrain:
            設定したロケータに、選択したジオメトリを再びオリエントコンストレイントにする機能です。
            (グループの名前とロケータの名前が是非一致して下さい。）

        3) Break Constrain:
            ロケータとジオメトリ間のオリエントコンストレイントを解除します。
