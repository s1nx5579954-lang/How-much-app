import streamlit as st
import random

# --- 🖤 洗練されたミニマルカスタムスタイル ---
st.markdown("""
    <style>
    .main-title {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 3rem !important;
        font-weight: 900 !important;
        text-align: center;
        color: #000000;
        margin-bottom: 0px;
        letter-spacing: -0.05em;
    }
    .sub-title {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 0.85rem;
        text-align: center;
        color: #666666;
        margin-top: 5px;
        margin-bottom: 2.5rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }
    .result-score {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 5rem !important;
        font-weight: 900 !important;
        color: #000000;
        text-align: center;
        line-height: 1.1;
    }
    .result-names {
        font-family: 'Hiragino Kaku Gothic ProN', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #111111;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-comment {
        font-family: 'Hiragino Kaku Gothic ProN', sans-serif;
        font-size: 1.05rem;
        color: #111111;
        text-align: center;
        line-height: 1.8;
        padding: 20px;
        border-top: 1px solid #eaeaea;
        border-bottom: 1px solid #eaeaea;
        margin-bottom: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Mind Match</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Simple 16-Type Synchronizer</p>', unsafe_allow_html=True)

# --- 🧠 質問データ（4つの観点 × 各4問 = 計16問） ---
# dimension: 集計先の指標名
# プラス値 = 前者の性質（外交・表面・直感・判断）
# マイナス値 = 後者の性質（内向・深層・論理・知覚）
QUESTIONS = [
    # 1. 興味の方向（外交的 vs 内向的）
    {"dim": "EI", "q": "休日の過ごし方として、より惹かれるのは？", "opts": [
        {"text": "大勢でワイワイイベントやパーティーに参加する", "p": 2},
        {"text": "親しい友人2〜3人とカフェで楽しく話す", "p": 1},
        {"text": "家で1人で好きな映画や本を見て過ごす", "p": -1},
        {"text": "誰とも連絡を絶ち、完全に自分の世界にこもる", "p": -2}
    ]},
    {"dim": "EI", "q": "新しい環境（クラスや職場）に入ったとき、あなたの行動は？", "opts": [
        {"text": "自分から積極的に声をかけて知り合いを増やす", "p": 2},
        {"text": "話しかけられたら明るく楽しく会話を広げる", "p": 1},
        {"text": "まずは周りの様子をじっくり観察する", "p": -1},
        {"text": "自分の席で静かに過ごし、話しかけられるのを待つ", "p": -2}
    ]},
    {"dim": "EI", "q": "元気をチャージ（リフレッシュ）したいとき、どうする？", "opts": [
        {"text": "友達を誘って外に遊びに行く、カラオケに行く", "p": 2},
        {"text": "散歩をしたり、外の空気を吸いに行く", "p": 1},
        {"text": "自分の部屋でお気に入りの音楽を聴く", "p": -1},
        {"text": "ひたすら寝る、または誰にも邪魔されず趣味に没頭する", "p": -2}
    ]},
    {"dim": "EI", "q": "自分の考えや感情を伝えるとき、どちらが楽？", "opts": [
        {"text": "考えるより先に、言葉にして話しながら整理する", "p": 2},
        {"text": "ある程度まとまったら、口頭で伝える", "p": 1},
        {"text": "じっくり文章（LINEやメール）に書いて伝える", "p": -1},
        {"text": "心の中に留めておくことが多く、あまり外に出さない", "p": -2}
    ]},

    # 2. ものの見方（表面的 vs 深層的）
    {"dim": "SN", "q": "映画や小説を見るとき、どこに一番惹かれる？", "opts": [
        {"text": "ハラハラするアクションや、映像の美しさ、分かりやすい面白さ", "p": 2},
        {"text": "登場人物のセリフや、現実的なストーリー展開", "p": 1},
        {"text": "物語の裏に隠された伏線や、登場人物の心理描写", "p": -1},
        {"text": "独特な世界観や、人生の意味を考えさせられる抽象的なテーマ", "p": -2}
    ]},
    {"dim": "SN", "q": "新しい仕事を頼まれたとき、説明として欲しいのは？", "opts": [
        {"text": "具体的な手順、過去の正確なデータ、手本となる見本", "p": 2},
        {"text": "大体の作業の流れと、今の現状の共有", "p": 1},
        {"text": "その仕事が目指す最終的なゴールや将来のビジョン", "p": -1},
        {"text": "目的の本質や概念、自由にアイデアを出せる余白", "p": -2}
    ]},
    {"dim": "SN", "q": "旅行の計画を立てるとき、あなたの頭の中は？", "opts": [
        {"text": "有名スポットの営業時間、移動にかかる正確な時間や費用", "p": 2},
        {"text": "美味しいお店や、現地で実際にすることのリスト", "p": 1},
        {"text": "現地でどんな体験ができそうかというワクワクするイメージ", "p": -1},
        {"text": "もし予定が変わったらどうしようという、あらゆる可能性の妄想", "p": -2}
    ]},
    {"dim": "SN", "q": "人の話を聴くとき、どこに注目しやすい？", "opts": [
        {"text": "相手が話している「事実」や、今起きている出来事そのもの", "p": 2},
        {"text": "相手の表情や言葉のニュアンス、細かいディテール", "p": 1},
        {"text": "相手が本当に言いたい「隠された本音」や意図", "p": -1},
        {"text": "その話が今後どんな展開につながっていくかという未来の予測", "p": -2}
    ]},

    # 3. 判断の仕方（直感的・感情的 vs 論理的・客観的）
    {"dim": "TF", "q": "友人が悩んで泣いているとき、最初にとる行動は？", "opts": [
        {"text": "まずは「大変だったね」と寄り添い、一緒に悲しむ", "p": 2},
        {"text": "相手の話を否定せず、ただじっくり聴いてあげる", "p": 1},
        {"text": "話を聞きながら、心の中で何が原因かを分析する", "p": -1},
        {"text": "どうすればその悩みが解決するか、具体的なアドバイスをする", "p": -2}
    ]},
    {"dim": "TF", "q": "買い物で迷ったとき、最後の決め手になるのは？", "opts": [
        {"text": "見た瞬間のときめき、デザインが好き、自分の直感", "p": 2},
        {"text": "これを持っていると気分が上がりそう、というワクワク感", "p": 1},
        {"text": "価格に見合う価値があるか、今本当に必要かという実用性", "p": -1},
        {"text": "スペック、他社製品との比較、機能面での論理的なメリット", "p": -2}
    ]},
    {"dim": "TF", "q": "話し合いや議論のとき、あなたが大切にしたいのは？", "opts": [
        {"text": "みんなが納得しているか、場の雰囲気や人間関係が壊れないか", "p": 2},
        {"text": "お互いの気持ちや立場が尊重されているか", "p": 1},
        {"text": "効率的に進んでいるか、話が脱線していないか", "p": -1},
        {"text": "感情を抜きにして、何が「正しい事実」であるか、論理的整合性", "p": -2}
    ]},
    {"dim": "TF", "q": "人から褒められて一番嬉しい言葉はどちら？", "opts": [
        {"text": "「いつも優しくて話しやすいね」「あなたがいてくれて良かった」", "p": 2},
        {"text": "「センスが良いね」「あなたの感性が好き」", "p": 1},
        {"text": "「仕事が早くて助かる」「頼りになるね」", "p": -1},
        {"text": "「頭が良いね」「考え方がすごく論理的で分かりやすい」", "p": -2}
    ]},

    # 4. 外界との接し方（判断型 vs 知覚型）
    {"dim": "JP", "q": "宿題や仕事の期限があるとき、どう進める？", "opts": [
        {"text": "最初にきっちりスケジュールを立てて、計画通りに早めに終わらせる", "p": 2},
        {"text": "毎日少しずつ、均等に進めるよう努力する", "p": 1},
        {"text": "期限が近づいてきたら、徐々にエンジンをかけていく", "p": -1},
        {"text": "締め切り直前まで手をつけず、最後の集中力で一気に終わらせる", "p": -2}
    ]},
    {"dim": "JP", "q": "休日に友達と遊ぶ約束をしたとき、事前準備は？", "opts": [
        {"text": "行くお店、ルート、時間、すべて事前に予約・確定させておく", "p": 2},
        {"text": "メインの場所だけ決めておき、他は軽く調べておく", "p": 1},
        {"text": "集合場所と時間だけ決めて、あとは当日の気分で決める", "p": -1},
        {"text": "ノープランで集まり、行き当たりばったりの旅を楽しむ", "p": -2}
    ]},
    {"dim": "JP", "q": "部屋の片付けや整理整頓について、あなたの状態は？", "opts": [
        {"text": "物の定位置が完全に決まっており、使ったらすぐ元の場所に戻す", "p": 2},
        {"text": "散らかる前に、定期的にまとめて掃除をする", "p": 1},
        {"text": "少し散らかってきても、生活に困らなければあまり気にしない", "p": -1},
        {"text": "足の踏み場がなくなるなど、限界が来たら一気に大掃除する", "p": -2}
    ]},
    {"dim": "JP", "q": "ルールや規則についてのあなたの考え方は？", "opts": [
        {"text": "ルールは守るためにある。秩序を保つために絶対に必要だ", "p": 2},
        {"text": "基本的には従うべきで、破ると周りに迷惑がかかると思う", "p": 1},
        {"text": "状況に応じて、柔軟に変えてもいいルールもあると思う", "p": -1},
        {"text": "ルールに縛られたくない。自由な行動を制限するものだと感じる", "p": -2}
    ]}
]

# セッション状態（データ保持）の初期化
if 'step' not in st.session_state:
    st.session_state.step = "setup"
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'p1_points' not in st.session_state:
    st.session_state.p1_points = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}
if 'p2_points' not in st.session_state:
    st.session_state.p2_points = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}
if 'shuffled_opts' not in st.session_state:
    st.session_state.shuffled_opts = []

# 各ステップの処理
if st.session_state.step == "setup":
    st.subheader("PLAYER REGISTRATION")
    name1 = st.text_input("Player 1 (先に答える人)", placeholder="名前を入力")
    name2 = st.text_input("Player 2 (次に答える人)", placeholder="名前を入力")
    if st.button("START"):
        if name1 and name2:
            st.session_state.name1 = name1
            st.session_state.name2 = name2
            st.session_state.step = "p1_turn"
            st.session_state.current_q = 0
            st.session_state.p1_points = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}
            st.session_state.p2_points = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}
            # 最初の質問の選択肢をシャッフル
            opts = QUESTIONS[0]["opts"].copy()
            random.shuffle(opts)
            st.session_state.shuffled_opts = opts
            st.rerun()
        else:
            st.warning("両方の名前を入力してください。")

elif st.session_state.step == "p1_turn":
    idx = st.session_state.current_q
    st.subheader(f"TURN : {st.session_state.name1} ({idx + 1} / 16)")
    st.write(f"⚠️ {st.session_state.name2} さんに画面を見られないようにしてください。")
    st.progress((idx + 1) / 16)
    
    q_data = QUESTIONS[idx]
    
    # ラジオボタンで表示（表示順はシャッフル済み）
    display_texts = [o["text"] for o in st.session_state.shuffled_opts]
    selected_text = st.radio(q_data["q"], display_texts, key=f"p1_q_{idx}")
    
    if st.button("LOCK ANSWER"):
        # 選んだ選択肢のポイントを探して加算
        chosen_opt = next(o for o in st.session_state.shuffled_opts if o["text"] == selected_text)
        st.session_state.p1_points[q_data["dim"]] += chosen_opt["p"]
        
        st.session_state.step = "change_turn"
        st.rerun()

elif st.session_state.step == "change_turn":
    st.subheader("PLAYER CHANGE")
    st.write("回答が記録されました。")
    st.write(f"端末を {st.session_state.name2} さんに渡してください。")
    if st.button(f"{st.session_state.name2} の回答を始める"):
        st.session_state.step = "p2_turn"
        st.rerun()

elif st.session_state.step == "p2_turn":
    idx = st.session_state.current_q
    st.subheader(f"TURN : {st.session_state.name2} ({idx + 1} / 16)")
    st.write(f"⚠️ {st.session_state.name1} さんの感覚で答えてください！")
    st.progress((idx + 1) / 16)
    
    q_data = QUESTIONS[idx]
    
    # Player2でも同じ選択肢順で出すために再利用
    display_texts = [o["text"] for o in st.session_state.shuffled_opts]
    selected_text = st.radio(q_data["q"], display_texts, key=f"p2_q_{idx}")
    
    if st.button("NEXT"):
        # 選んだ選択肢のポイントを探して加算
        chosen_opt = next(o for o in st.session_state.shuffled_opts if o["text"] == selected_text)
        st.session_state.p2_points[q_data["dim"]] += chosen_opt["p"]
        
        if idx + 1 < 16:
            st.session_state.current_q += 1
            # 次の質問の選択肢を新しくシャッフル
            opts = QUESTIONS[st.session_state.current_q]["opts"].copy()
            random.shuffle(opts)
            st.session_state.shuffled_opts = opts
            st.session_state.step = "p1_turn"
        else:
            st.session_state.step = "result"
        st.rerun()

elif st.session_state.step == "result":
    # --- 📐 シンプルで美しい相性計算ロジック ---
    # 各観点（EI, SN, TF, JP）の最大値は 2p × 4問 = 8p、最小値は -8p
    # 2人の合計ポイントの「距離（ズレ）」からシンクロ率を計算します。
    dims = ["EI", "SN", "TF", "JP"]
    total_match = 0
    
    for d in dims:
        p1 = st.session_state.p1_points[d]
        p2 = st.session_state.p2_points[d]
        
        # 1つの観点での最大値と最小値の差は16（+8 から -8 まで）
        # 2人のポイントの絶対的なズレの広さを計算
        diff = abs(p1 - p2)
        
        # ズレが0なら100点、ズレが16なら0点
        dim_match = (1.0 - (diff / 16.0)) * 100
        total_match += dim_match
        
    avg_match = int(total_match / 4)
    
    st.markdown('<p style="text-align:center; font-weight:700; color:#888888; letter-spacing:0.1em; margin-bottom:0px;">SYNCHRONIZATION</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="result-score">{avg_match}%</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="result-names">{st.session_state.name1}  ×  {st.session_state.name2}</p>', unsafe_allow_html=True)
    
    if avg_match >= 85:
        comment = "【ソウルメイト級のシンクロ】物事の捉え方から心のエネルギーの方向、意思決定のタイミングまで、驚くほどそっくりな2人です。言葉にしなくてもお互いの考えていることが手に取るように分かります。"
    elif avg_match >= 65:
        comment = "【名コンビ級の相性】お互いの価値観のベースが非常に近いです。細かい部分での違いは程よいスパイスとなり、一緒にいて最もストレスなく、自然体で笑い合える最高のバランスです。"
    elif avg_match >= 45:
        comment = "【お互いを補い合う関係】異なる視点を持っているからこそ、自分にない部分に気づかせてくれる組み合わせです。お互いの意見を尊重し合うことで、非常に強いチームワークを発揮できます。"
    else:
        comment = "【未知の世界の2人】全く違う性質の星に生まれたような組み合わせ。だからこそ新鮮で、相手のやることなすことが予測不能で面白いと感じるはず。お互いのルールを尊重し合えれば最強です。"
        
    st.markdown(f'<div class="result-comment">{comment}</div>', unsafe_allow_html=True)
    
    if st.button("RETRY"):
        st.session_state.step = "setup"
        st.rerun()
# 〜（中略：スコア計算やデータの定義など）〜

# --- アプリ画面での割合表示部分 ---
st.subheader("📊 4観点のバランス診断結果")
st.write("各指標の割合（％）です。どちらの傾向が強いかチェックしてみましょう！")

# 【注】実際のあなたのコードの計算結果（％の数値）をここに当てはめてください。
# ここでは、前回のロジックに基づいた仮の数値（0〜100）を入れています。
dimensions_pct = {
    "興味の方向": {"left_label": "Extravert (外向)", "right_label": "Introvert (内向)", "val": 65},
    "ものの見方": {"left_label": "Sensing (感覚)", "right_label": "Intuition (直感)", "val": 40},
    "判断の仕方": {"left_label": "Thinking (思考)", "right_label": "Feeling (感情)", "val": 55},
    "外界との接し方": {"left_label": "Judging (判断)", "right_label": "Perceiving (知覚)", "val": 70}
}

# 4つの観点をループで回してメーター形式で表示
for title, data in dimensions_pct.items():
    st.markdown(f"### 🧭 {title}")
    
    # 左右の要素の％を計算
    left_pct = data["val"]
    right_pct = 100 - data["val"]
    
    # テキストで綺麗に割合を表示
    st.write(f"**{data['left_label']}** {left_pct}%  vs  {right_pct}% **{data['right_label']}**")
    
    # 標準機能のプログレスバーでメーターを表示（0.0 〜 1.0 の値にするため 100 で割る）
    st.progress(left_pct / 100)
    st.write("---") # 区切り線
