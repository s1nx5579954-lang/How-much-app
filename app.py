import streamlit as st
import random
import os

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
    .result-type {
        font-family: 'Hiragino Kaku Gothic ProN', sans-serif;
        font-size: 1.6rem;
        font-weight: 900;
        color: #000000;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .result-pair {
        font-family: 'Hiragino Kaku Gothic ProN', sans-serif;
        font-size: 1rem;
        color: #888888;
        text-align: center;
        letter-spacing: 0.1em;
        margin-bottom: 1.5rem;
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
    .dim-row {
        font-family: 'Hiragino Kaku Gothic ProN', sans-serif;
        font-size: 0.95rem;
        color: #333333;
        text-align: center;
        margin-bottom: 0.4rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Mind Match</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Simple 16-Type Synchronizer</p>', unsafe_allow_html=True)

# --- 🧠 質問データ（4つの観点 × 各4問 = 計16問） ---
QUESTIONS = [
    # 1. 興味の方向（EI）
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
    # 2. ものの見方（SN）
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
    # 3. 判断の仕方（TF）
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
    # 4. 外界との接し方（JP）
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

DIM_LABELS = {
    "EI": "興味の方向",
    "SN": "ものの見方",
    "TF": "判断の仕方",
    "JP": "外界との接し方"
}

# --- 🎴 16パターンの相性結果データ ---
RESULT_PATTERNS = {
    "MSEP": {
        "pair": "柴犬 & シベリアンハスキー",
        "title": "ソウルメイト",
        "title_en": "Soul Mate",
        "desc": "ノリ、趣味、価値観、テンポの全てが100%シンクロする奇跡の2人。お互いの考えていることが言葉にしなくても伝わるため、一緒にいて最も脳の体力を使いません。まるで前世から一緒だった「双子」のように、何時間でも同じ空間を共有できる無敵の相性です。"
    },
    "MSEB": {
        "pair": "ウサギ & カメ",
        "title": "ビジネスパートナー",
        "title_en": "Business Partner",
        "desc": "波長や趣味、価値観は完全に一致しているため、おしゃべりの楽しさはピカイチ。ただし、行動のペースだけが凸凹です。一方が急に動きたくなり、もう一方がマイペースに構えることも。お互いのテンポを「それも面白い」と尊重し合えれば、最強の相棒になれます。"
    },
    "MSIP": {
        "pair": "クマ & フクロウ",
        "title": "心から信頼できる親友",
        "title_en": "Trusted Best Friend",
        "desc": "外向的なノリや趣味のツボは同じでいつも楽しそうですが、物事を判断するときの基準だけが違います（感情派と論理派）。だからこそ、2人で悩んだときには、深く寄り添う温かさと、冷静でスマートな解決策のどちらも手に入ります。お互いをリスペクトできる知的な相性です。"
    },
    "MSIB": {
        "pair": "レッサーパンダ & カメレオン",
        "title": "高め合えるライバル",
        "title_en": "Inspiring Rival",
        "desc": "社交性の高さと趣味のツボが同じなので、最初の意気投合は一瞬です。しかし、いざ深く付き合うと価値観や行動ペースのバリエーションに驚くはず。お互いの独特な感性を「自分にないスパイス」として面白がれる、クリエイティブで少しエキサイティングな関係です。"
    },
    "MIEP": {
        "pair": "ネコ & ペンギン",
        "title": "刺激的な友人",
        "title_en": "Exciting Friend",
        "desc": "根本的なノリや心が大切にするものが同じなので、一緒にいてとにかく明るい気持ちになれます。ただ、ものの見方が違うため趣味や興味の対象は完全にバラバラ。「何それ知らない！」とお互いのカルチャーを教え合いながら、どこまでも会話のキャッチボールが弾む楽しい関係です。"
    },
    "MIEB": {
        "pair": "サル & ナマケモノ",
        "title": "居心地の良い遊び仲間",
        "title_en": "Cozy Playmate",
        "desc": "ノリと価値観は一致しているので信頼感は抜群ですが、趣味の対象と行動のテンポが真逆です。突発的なイベントが起きやすく、衝突することもあるかもしれません。しかし、2人でいると絶対に退屈せず、世界が何倍にも広がるようなスリリングな魅力があります。"
    },
    "MICP": {
        "pair": "ライオン & トラ",
        "title": "熱く語り合える同志",
        "title_en": "Passionate Comrade",
        "desc": "社交的で行動力抜群のノリが完全一致。2人が揃うと一気にその場がハッピーな空気になります。視点や判断基準は違うため、意見が真っ二つに分かれることもありますが、そんな違いすらエネルギーに変えて、周囲を巻き込む大きな渦を作れるパワフルな相性です。"
    },
    "MICB": {
        "pair": "イルカ & フラミンゴ",
        "title": "気楽に付き合える知人",
        "title_en": "Casual Acquaintance",
        "desc": "お互い外向的で人と関わるのが好きという点だけが共通しています。趣味も価値観もペースも全く違うため、最初は「本当に仲良くなれる？」と思うかもしれません。しかし、お互いの強みが1ミリも被らないため、合わさると完璧な化学反応を起こす、可能性を秘めた相性です。"
    },
    "SSEP": {
        "pair": "黒ネコ & 白ネコ",
        "title": "以心伝心のパートナー",
        "title_en": "Telepathic Partner",
        "desc": "お互いに一人の時間や自立した距離感を大切にする大人な関係でありながら、趣味のツボや価値観、行動ペースが驚くほど一致しています。ベタベタした付き合いはしませんが、特定のテーマや趣味をやらせたら右に出るものはいない、ディープな信頼で結ばれた関係です。"
    },
    "SSEB": {
        "pair": "カピバラ & コアラ",
        "title": "安定・安心の相棒",
        "title_en": "Stable Buddy",
        "desc": "趣味のツボは同じですが、お互いマイペースに自分の世界を持っています。この2人の空間には、無理に盛り上げるための会話は必要ありません。「言葉がなくても、同じ空間にいるだけでなぜか落ち着く」という、大人の成熟した心地よさがある相性です。"
    },
    "SSIP": {
        "pair": "オオカミ & タカ",
        "title": "無言でも通じ合う理解者",
        "title_en": "Silent Understander",
        "desc": "自立したスタンスと行動ペースは同じで、趣味の同期もしています。ただし、判断の基準だけが異なります。ベタベタした感情論ではなく、「お前がそういうなら間違いない」と実力や行動で認め合うような、ビジネスや共同プロジェクトで最高の成果を出すカッコいいコンビです。"
    },
    "SSIB": {
        "pair": "リス & モモンガ",
        "title": "ほのぼの癒やし合える関係",
        "title_en": "Healing Dynamic",
        "desc": "4つのうち「趣味のツボ」だけが一致しており、あとはお互い完全にマイペース。普段はそれぞれの世界で全く違う生活をしていますが、共通の好きなことの話になると、吊り橋を渡って一気にディープに繋がり合います。お互いを一切縛らない、究極に気楽な相性です。"
    },
    "SIEP": {
        "pair": "柴犬 & 三毛猫",
        "title": "ほどよい距離感の友達",
        "title_en": "Comfortable Distance Friend",
        "desc": "お互い一人の時間を大事にし、趣味も違いますが、価値観の基準と行動ペースが同じです。相手の領域に余計な干渉をしないため、揉め事が一切起きません。空気のように自然体で、一緒にいるだけで日々のストレスが溶けていくような、最高の癒やしをもたらす関係です。"
    },
    "SIEB": {
        "pair": "クジラ & 渡り鳥",
        "title": "語り合える友",
        "title_en": "Deep Thinker",
        "desc": "ノリも趣味も行動のテンポもバラバラ。一見すると接点がなさそうに見えますが、意思決定の基準である「心の奥底で本当に大切にしている価値観」だけが繋がっています。頻繁に会わなくても、人生の節目でなぜか一番に相談したくなるような、深い精神的支柱となる相性です。"
    },
    "SICP": {
        "pair": "キツネ & タヌキ",
        "title": "知的なディベート仲間",
        "title_en": "Intellectual Debater",
        "desc": "無駄なベタベタ感はなく、同じテンポでサクサク進む関係。趣味や価値観は真逆ですが、だからこそ主観に囚われず、お互いの盲点を論理的に補い合えます。旅行の計画から将来のライフプランまで、驚くほど効率的に目標を達成していける現実的な強さを持つ2人です。"
    },
    "SICB": {
        "pair": "ハリネズミ & ヒツジ",
        "title": "ある意味奇跡な2人",
        "title_en": "Miracle Partner",
        "desc": "性質が全て真逆。あなたにないものを相手がすべて持ち、相手にないものをあなたがすべて持っています。普通ならすれ違うはずが、出会ってしまったのは奇跡。お互いへのリスペクトがあれば、2人が合わさることで1つの完璧な宇宙が完成する、強烈な化学反応を秘めた最高峰の凸凹コンビです。"
    },
}

# --- セッション状態の初期化 ---
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


def calc_match_rate(p1_points, p2_points, dim):
    """各観点の一致率（0〜100%）を計算"""
    diff = abs(p1_points[dim] - p2_points[dim])
    return (1.0 - (diff / 16.0)) * 100


def determine_pattern(p1_points, p2_points):
    """4観点の一致率からパターンコードと各観点の一致率を返す"""
    rates = {}
    code = ""
    for dim, high_letter, low_letter in [
        ("EI", "M", "S"),
        ("SN", "S", "I"),
        ("TF", "E", "C"),
        ("JP", "P", "B"),
    ]:
        rate = calc_match_rate(p1_points, p2_points, dim)
        rates[dim] = rate
        code += high_letter if rate >= 50 else low_letter
    return code, rates


# --- 各ステップの処理 ---
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
    display_texts = [o["text"] for o in st.session_state.shuffled_opts]
    selected_text = st.radio(q_data["q"], display_texts, key=f"p1_q_{idx}")

    if st.button("LOCK ANSWER"):
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
    st.write(f"⚠️ {st.session_state.name1} さんの回答を予想するか、あなたの感覚で答えてください！")
    st.progress((idx + 1) / 16)

    q_data = QUESTIONS[idx]
    display_texts = [o["text"] for o in st.session_state.shuffled_opts]
    selected_text = st.radio(q_data["q"], display_texts, key=f"p2_q_{idx}")

    if st.button("NEXT"):
        chosen_opt = next(o for o in st.session_state.shuffled_opts if o["text"] == selected_text)
        st.session_state.p2_points[q_data["dim"]] += chosen_opt["p"]

        if idx + 1 < 16:
            st.session_state.current_q += 1
            opts = QUESTIONS[st.session_state.current_q]["opts"].copy()
            random.shuffle(opts)
            st.session_state.shuffled_opts = opts
            st.session_state.step = "p1_turn"
        else:
            st.session_state.step = "result"
        st.rerun()

elif st.session_state.step == "result":
    code, rates = determine_pattern(st.session_state.p1_points, st.session_state.p2_points)
    pattern = RESULT_PATTERNS[code]

    # 総合シンクロ率（4観点の平均）
    avg_match = int(sum(rates.values()) / 4)

    st.markdown(
        '<p style="text-align:center; font-weight:700; color:#888888; '
        'letter-spacing:0.1em; margin-bottom:0px;">SYNCHRONIZATION</p>',
        unsafe_allow_html=True
    )
    st.markdown(f'<p class="result-score">{avg_match}%</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="result-names">{st.session_state.name1}  ×  {st.session_state.name2}</p>',
        unsafe_allow_html=True
    )

    # --- 🐾 キャラクター画像表示 ---
    image_path = f"assets/{code}.png"
    if os.path.exists(image_path):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image_path, use_container_width=True)
    else:
        st.info(f"画像が見つかりません: {image_path}（assetsフォルダに配置してください）")

    # --- 🏷️ タイプ名表示 ---
    st.markdown(f'<p class="result-type">{pattern["title"]}</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="result-pair">{pattern["title_en"]} ｜ {pattern["pair"]}</p>',
        unsafe_allow_html=True
    )

    # --- 📊 4観点ごとの一致率 ---
    st.markdown("<br>", unsafe_allow_html=True)
    for dim in ["EI", "SN", "TF", "JP"]:
        label = DIM_LABELS[dim]
        rate = rates[dim]
        st.markdown(f'<p class="dim-row">{label}　{int(rate)}%</p>', unsafe_allow_html=True)
        st.progress(rate / 100)

    # --- 📝 診断コメント ---
    st.markdown(f'<div class="result-comment">{pattern["desc"]}</div>', unsafe_allow_html=True)

    if st.button("RETRY"):
        st.session_state.step = "setup"
        st.rerun()
