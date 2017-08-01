#インスペクションの原則
・緊急ボタン
・衝突回避（TCメンバーがロボットの前を横切る）
・ロボットの声が出る（大声で明瞭でなければならない）
・カスタムコンテナ（ボウル、トレイなど）　#なにこれ？
・外部デバイス（ワイヤレスネットワークを含む）がある場合 #DSPLでいるのかな...
・代替ヒューマンロボットインタフェース（3.9.1節）。 #代わりの入力方法みたいなもの 
 (例:音声認識をマーカーにする　ってやつみたいな。

加えて、
SPL競技者は
・外見は綺麗
・作ったまんまの姿で

#去年の流れでは
移動→途中TCが立ちふさがる→どいたら移動→音声認識→移動(退場)

#起動方法--hsr内部で--
・rospeex_inspection.launchを起動(まだ未制作)(rospeex_local.launchとaudiomonitorと認識のnodeを立ち上げる予定)
・自己位置を確認
・inspection_smach_interface.pyを起動(あとは音声に従え。)

#注意事項
rospeex_inspection.launchなんて作ってないので、テストするときは、/ref_talkに"ok"とstringでpublishすればok(のつもり)

#依存関係
・hsrb_interface(ros-indigo-tmc-desktop-full)
・common( https://git.hsr.io/erasers2017/common.git )
・rospeex(現状)

＃なにかあれば、管理者に連絡ー
