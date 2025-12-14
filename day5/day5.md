---
title: day5 ◯ケモン風バトルゲームを作ろう②
permalink: /day5/
---

# 弾を出そう
弾を発射するためには、いくつかやらなくちゃいけないことがあるけど、とりあえず弾を表示するだけのコードを書いてみよう

弾はシンプルに、pyxel の機能でできる四角形を使おう。
スペースキーが押されたときに、黄色い資格がキャラクターの上に表示されるようにしてみよう。

```python
import pyxel
pyxel.init(120, 120)
pyxel.load("danmaku.pyxres")

character = {
    "x": 120 / 2 - 16 / 2,
    "y": 90,
    "tama": []
}
enemy = {
    "x": 120 / 2 - 16 / 2,
    "y": 20,
    "direction": 1
}

    


def update():
    print(character["tama"])
    enemy["x"] = enemy["x"] + enemy["direction"]
    if enemy["x"] >= 120 - 16 or enemy["x"] <= 16:
        enemy["direction"] = enemy["direction"] * -1
    
    if pyxel.btn(pyxel.KEY_RIGHT) == True:
        character["x"] = character["x"] + 1
        
    elif pyxel.btn(pyxel.KEY_LEFT) == True:
        character["x"] = character["x"] - 1

    if pyxel.btnp(pyxel.KEY_SPACE) == True:
       character["tama"].append([character["x"], character["y"] - 16])
    
    


def draw():
    pyxel.cls(0)
    pyxel.blt(character["x"], character["y"], 0, 0, 0, 16, 16, 0)
    pyxel.blt(enemy["x"], enemy["y"], 0, 16, 0, 16, 16, 0)
    
    for i in character["tama"]:
        pyxel.blt(i[0], i[1], 0, 32, 0, 16, 16, 0)
    
pyxel.run(update, draw)
```
<br><img class="" src="./img/Animation5.gif" alt="" style="width:50%">

弾を動かすために、[tama]の中にある弾丸を、ｙ方向に１づつ移動させよう。この処理をupdate関数の中に追加します

```python
for i in character["tama"]:
    i[1] = i[1] - 1
```
<br>
これで、ゲームっぽくなってきた！！<br>
<img class="" src="./img/move_bullet.gif" alt="動く弾" style="width: 50%"><br>

# 弾を消そう
今ターミナルを見てみると、めちゃくちゃ文字がたくさん出ていて、何がなんだかって感じになってる

<img class="" src="./img/full_bullet_list.gif" alt="full_bullet_list" style="width:50%"><br>

うん、キモい。
これは、update()関数の一番最初に
```python
print(character["tama"])
```
が入っているからなんだけど。tamaリスト、つまり弾丸の座標のリストが、弾を打つたびに増えていってるから。
見て分かる通り、弾が画面外に出たあとも表示されているし、数字が変わっているね。表示場はうまくいってても、裏側では、もう画面上ん存在しない弾の処理を、プログラムがさせられている状態。
「うまくいってるんだからいいじゃん」って言ってこれを放置しておくと、例えばゲーム後半で処理が重くなって、ゲームの動作が不安定になったり、思わぬところでバグが発生したりして、大変なことになりかねない。
じゃあ、必要のない弾を消してしまおう。
弾を消すには、必要ない座標のリストを`tamaリスト`から消してしまえばいいんだけど、どういう条件で弾を消すかを先に考えよう。
- ①画面外に出た弾を消す
- ②敵キャラに当たった弾を消す

この２つを、順番に実装していこう。

  - # 画面外に出た弾を消す
    敵に当たらずに画面外に出るケースを実装しよう。
    画面外に出るということはどういうことか。ｙ方向に移動しているわけだから、弾の座標が -16 になったら画面外に出る。そうなったら用済みなので、弾を消しちゃおう。
    つまり、tamaリストの中から、ｙ軸の数字が -16 以下になっているやつを探して、そいつを削除すればいいわけだ。
    ### リストの性質：先入れ先出し
    tamaリストは、pythonのデータ型の一つ、「リスト」というデータになっている。データを纏めて保存するのに便利な型なんだけど、いくつか特徴がある <br>
    <br><img class="" src="./img/list_index.png" alt="list_index" style="width:50%"><br>
    今回の場合、右側（後ろの方）にデータを追加していってるので、一番古いデータは一番左になる。
    pyxelは毎フレームごとに処理を実行するわけだから、例えば同じフレームで弾が２発打ててしまうことはあり得ない。つまり、毎回tamaリストにある全部の座標をチェックする必要はなくて、一番古いデータをチェックして、座標が-16以下になっていればそれを消す、って感じでOKなわけ。それを実装すると、こんな感じになる

    ```python
    # 一番古い弾のデータをチェック
    if len(character["tama"]) and  character["tama"][0][1] <= -16:
        character["tama"].pop(0)
    ```
    `pop`ていうのがリストから消す働きをしているんだけど、リストの詳しいことなどは今回は深く突っ込まないので、気になる人はリッキーたちに聞いてくれ♪
    <br>
    弾が消えてるかどうか、実行して確認してみよう
    <br><img class="" src="./img/bullet_delete_1.gif" alt="bullet_delete_1" style="width:50%"><br>
    これでおｋ！

  - # 敵に当たった弾を消す
    さて、この仕組みを考えよう
    ### 当たり判定 
    格ゲーとかシューティングゲームにおいて、このあたり判定がうまく調整されているかどうかは、そのゲームが神ゲーになるかクソゲーになるかの大きな決め手。
    いろいろな方法があるけど、今回はその考え方うちの一つを紹介します。
    <details markdown="1">
    <summary>　本来の当たり判定の考え方
    </summary>
    
    <br>
    ちょっと考えてみよう。半径２センチの円と、３センチの円があったとしよう。この２つが当たっているかどうかを判定する条件はなんだろう？
    <br><img class="" src="./img/hit_detection1.png" alt="hit_detection1" style="width:70%"><br>
    そう、中心同士の距離が２＋３＝４センチ以下かどうか、だよね。
    そのとおりなんだけど、pyxelの画面では、こんな感じのｘ座標、ｙ座標で、キャラクターや物体の場所が表される。この２つが当たってるかどうか、どうやって判定する？<br>
    <br><img class="" src="./img/hit_detection2.png" alt="hit_detection2" style="width:70%"><br>

    ### みんな大好き数学の時間だぜ
    三平方の定理を思い出してみよう。
    こういう直角三角形をおいてみると、円の中心同士の距離がわかる
    <br>
    <img class="" src="./img/hit_detection3.png" alt="aaa" style="width=50%">
    <br>
    ？の部分を求めるには
    ```
    ？の２乗 ＝ ４の２乗 ＋ ３の２乗
    ```
    なので、？は５。つまり、当たっとるやないかい！ってこと
    すごいぜ数学！！数学大好き！！！

    当たり判定について、ストリートファイター開発者の人がより詳しいことを解説しているので、読んでみて
    [ストゼミ：当たり判定の基本](https://game.capcom.com/cfn/sfv/column/130393)

    みんなが「なんだよこのクソゲー当たり判定ザルかよｗｗ金返せ！！」って言ってる裏では、プログラマーのいろんな工夫や努力があるわけです
    </details>
    
    今回は弾が長方形で、ちゃんとやると、もうちょっと大変になる。なので、今回は単純に弾の四角が敵に重なってるかどうかで判定します。
    該当部分のコードはこんな感じ。
    ```python
    # 敵に当たった弾を削除
    for i in range(len(character["tama"]) - 1, -1, -1):
        tama_x = character["tama"][i][0]
        tama_y = character["tama"][i][1]
        # 当たり判定：弾と敵の矩形が重なっているかチェック
        if (
            tama_x < enemy["x"] + 16
            and tama_x + 16 > enemy["x"]
            and tama_y < enemy["y"] + 16
            and tama_y + 16 > enemy["y"]
        ):
            character["tama"].pop(i)
    ```
    update関数の中身がバケモンになってきたので、全体のコードを示しておきます。
    ```python

    def update():
        print(character["tama"])

        # 一番古い弾のデータをチェック
        if len(character["tama"]) and character["tama"][0][1] <= -16:
            character["tama"].pop(0)
        # 敵に当たった弾を削除
        for i in range(len(character["tama"]) - 1, -1, -1):
            tama_x = character["tama"][i][0]
            tama_y = character["tama"][i][1]
            # 当たり判定：弾と敵の矩形が重なっているかチェック
            if (
                tama_x < enemy["x"] + 16
                and tama_x + 16 > enemy["x"]
                and tama_y < enemy["y"] + 16
                and tama_y + 16 > enemy["y"]
            ):
                character["tama"].pop(i)

        enemy["x"] = enemy["x"] + enemy["direction"]
        if enemy["x"] >= 120 - 16 or enemy["x"] <= 16:
            enemy["direction"] = enemy["direction"] * -1

        if pyxel.btn(pyxel.KEY_RIGHT) == True:
            character["x"] = character["x"] + 1

        elif pyxel.btn(pyxel.KEY_LEFT) == True:
            character["x"] = character["x"] - 1

        if pyxel.btnp(pyxel.KEY_SPACE) == True:
            character["tama"].append([character["x"], character["y"] - 16])

        for i in character["tama"]:
            i[1] = i[1] - 1


    ```

# 敵ＨＰ・ダメージ、クリア画面の実装
このままではゲームが終わらないので、敵のＨＰがゼロになったらゲームクリア、という感じに実装してみよう

- ## ＨＰの実装と表示
  まずは敵(enemy)キャラにＨＰをもたせよう。enemyの辞書型に「ＨＰ」を追加。ＨＰを１００にしてみよう
  ```python
  enemy = {
      "x": 120 / 2 - 16 / 2,
      "y": 20,
      "direction": 1,
      "HP": 100
  }
  ```
  次に、そのＨＰを表示する処理を追加。表示を担当するdraw関数に、この一行を追加しよう
  ```python
  def draw():
    pyxel.cls(0)
    pyxel.blt(character["x"], character["y"], 0, 0, 0, 16, 16, 0)
    pyxel.blt(enemy["x"], enemy["y"], 0, 16, 0, 16, 16, 0)
    
    # この１行を追加
    pyxel.text(10, 10, f"enemy HP: {enemy["HP"]}", 7)

    for i in character["tama"]:
        pyxel.blt(i[0], i[1], 0, 32, 0, 16, 16, 0)
  ```
  <img class="" src="./img/screen_with_HP.png" alt="" style="width:50%"><br>

  では、敵に当たったときにダメージが入る＝enemy["HP"]が減る処理を追加していこう。当たった弾を消す処理のところに書けば良さげ。
  ```python
  def update():
    print(character["tama"])

    # 一番古い弾のデータをチェック
    if len(character["tama"]) and character["tama"][0][1] <= -16:
        character["tama"].pop(0)
    # 敵に当たった弾を削除
    for i in range(len(character["tama"]) - 1, -1, -1):
        tama_x = character["tama"][i][0]
        tama_y = character["tama"][i][1]
        # 当たり判定：弾と敵の矩形が重なっているかチェック
        if (
            tama_x < enemy["x"] + 16
            and tama_x + 16 > enemy["x"]
            and tama_y < enemy["y"] + 16
            and tama_y + 16 > enemy["y"]
        ):
            character["tama"].pop(i)

            # この一行を追加
            enemy["HP"] = enemy["HP"] - 10

            ＜以下略＞
  ```

  <img class="" src="./img/game_with_damage.gif" alt="" style="width: 50%"><br>

  # クリア演出の追加
  今のままだと敵のＨＰがマイナスになってしまってゲームが終わらないので、ＨＰがゼロ以下になったら「GAME CLEAR!」の表示を出すようにしよう
  
  さて、何をどう判定してクリア表示にするかだけど
  - ゲーム進行中は敵や味方の表示
  - ゲームクリア時は「GAME CLEAR!」の文字
  を表示したいわけなので、ゲームが進行中かどうかわかる変数を新しく追加しよう。
  ゲーム進行中はgame["status"]をTrue, クリア時はFalseにする感じ<br>
  ```python
  import pyxel

  pyxel.init(120, 120)
  pyxel.load("danmaku.pyxres")  
  character = {
      "x": 120 / 2 - 16 / 2, 
      "y": 90, 
      "tama": []
  }
  enemy = {
      "x": 120 / 2 - 16 / 2,
      "y": 20,
      "direction": 1,
      "HP": 100
  }

  # ここを追加
  game = {
      "status": True
  }
  ＜以下略＞
  ```

  敵のＨＰがゼロ以下になったときに、game["status"]をFalseにしよう。
  ```python
  def update():
    print(character["tama"])

    # 一番古い弾のデータをチェック
    if len(character["tama"]) and character["tama"][0][1] <= -16:
        character["tama"].pop(0)
    # 敵に当たった弾を削除
    for i in range(len(character["tama"]) - 1, -1, -1):
        tama_x = character["tama"][i][0]
        tama_y = character["tama"][i][1]
        # 当たり判定：弾と敵の矩形が重なっているかチェック
        if (
            tama_x < enemy["x"] + 16
            and tama_x + 16 > enemy["x"]
            and tama_y < enemy["y"] + 16
            and tama_y + 16 > enemy["y"]
        ):
            character["tama"].pop(i)
            enemy["HP"] = enemy["HP"] - 10

            # ここを追加
            if enemy["HP"] <= 0:
                game["status"] = False
            <以下略>
  ```
  では、draw()関数を書き換え、game["status"]がTrueのときはキャラクターなどを表示して、そうじゃないときは GAME CLEAR!を表示するようにしよう
  ```python
  def draw():
    pyxel.cls(0)
    if game["status"] == True:
        pyxel.cls(0)
        pyxel.blt(character["x"], character["y"], 0, 0, 0, 16, 16, 0)
        pyxel.blt(enemy["x"], enemy["y"], 0, 16, 0, 16, 16, 0)
        pyxel.text(10, 10, f"enemy HP: {enemy["HP"]}", 7)

        for i in character["tama"]:
            pyxel.blt(i[0], i[1], 0, 32, 0, 16, 16, 0)
    else:
        pyxel.text(40, 50, "GAME CLEAR!", 7)
  ```

  <img class="" src="./img/game clear.gif" alt="" style="width: 50%"><br>



















