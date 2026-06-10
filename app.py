cat << 'EOF' > app.py
import streamlit as st
import random

# --- 🖤 モノトーン＆洗練されたミニマルカスタムスタイル ---
st.markdown("""
    <style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main-title {
        font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', sans-serif;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-align: center;
        color: #000000;
        margin-bottom: 0px;
        padding-bottom: 0px;
        letter-spacing: -0.05em;
        animation: fadeInUp 1.0s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }
    .sub-title {
        font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', sans-serif;
        font-size: 0.9rem;
        text-align: center;
        color: #666666;
        margin-top: 5px;
        margin-bottom: 3rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        animation: fadeInUp 1.0s cubic-bezier(0.25, 1, 0.5, 1) 0.2s forwards;
    }
    .result-score-label {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #888888;
        text-align: center;
        letter-spacing: 0.1em;
        margin-bottom: 0px;
    }
    .result-score {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 5.5rem !important;
        font-weight: 900 !important;
        color: #000000;
        text-align: center;
        line-height: 1.1;
        margin-bottom: 5px;
    }
    .result-names {
        font-family: 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #111111;
        text-align: center;
        letter-spacing: 0.05em;
        margin-bottom: 2rem;
    }
    .result-comment {
        font-family: 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', sans-serif;
        font-size: 1.1rem;
        color: #111111;
        text-align: center;
        line-height: 1.8;
        padding: 25px 20px;
        border-top: 1px solid #eaeaea;
        border-bottom: 1px solid #eaeaea;
        margin-bottom: 4rem;
    }
    .section-title {
        font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        color: #000000;
        letter-spacing: 0.1em;
        margin-bottom: 2rem;
        text-align: center;
    }
    .category-label {
        font-family: 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #333333;
        text-align: center;
        margin-bottom: 15px;
    }
    
    /* 🎨 CSSのみで作る美しいカスタムドーナツ型パイグラフの設計 */
    .pie-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 30px;
    }
    .pure-pie {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: inset 0 0 0 1px rgba(0,0,0,0.05);
    }
    .pie-inner-hole {
        width: 90px;
        height: 90px;
        background-color: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 1.4rem;
        font-weight: 900;
        color: #111111;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">How Match</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Brain Synchronization Test</p>', unsafe_allow_html=True)

# 📋 4観点に関する24問の質問プール (各観点6問)
QUESTION_POOL = {
    "興味の方向": [
        {"q": "休日の理想的なバッテリー回復方法は？", "c": ["家で1人でまったり過ごす", "外に出て友人とアクティブに遊ぶ", "カフェなど静かな場所で1人で過ごす", "大人数が集まるイベントやパーティに行く"]},
        {"q": "仕事や学校が終わった後の理想の過ごし方は？", "c": ["真っ著ぐ家に帰って自分の時間を楽しむ", "誰かを誘ってご飯や飲みにいく", "趣味の集まりや習い事に行く", "SNSや動画を見てのんびり夜更かしする"]},
        {"q": "新しく趣味を始めるとしたらどちらに近い？", "c": ["読書や映画、ゲームなどインドアなもの", "旅行やスポーツ、ドライブなどアウトドアなもの", "創作活動や研究など1人で没頭するもの", "サークルやコミュニティなど人と関わるもの"]},
        {"q": "元気が起きない時、どうやってエネルギーを補給する？", "c": ["1人の時間を完全に確保して引きこおる", "信頼できる親しい友人と深く話す", "賑やかな場所に行って刺激をもらう", "とにかく寝るか自分の好きなものを食べる"]},
        {"q": "旅行の同行者として理想的な人数は？", "c": ["自分を含めて2人がベスト", "3人から4人の気の合うグループ", "完全に1人旅が良い", "5人以上の賑やかな大勢グループ"]},
        {"q": "初対面の人ばかりの場に放り込まれたらどうする？", "c": ["壁際で静かに様子を窺う", "近くにいる人に自分から話しかけてみる", "知っている人が来るのをひたすら待つ", "その場の雰囲気に合わせて自然に溶け込む"]}
    ],
    "モノの見方": [
        {"q": "初めての飲食店を選ぶときに一番信用する情報は？", "c": ["有名グルメサイトの点数や口コミの多さ", "自分の直感やお店の店構えの雰囲気", "友人や知人からの直接のおすすめ", "テレビやSNSで話題になっているかどうか"]},
        {"q": "新しいガジェットや服を買うときの決め手は？", "c": ["スペックや素材、価格などの現実的な実用性", "デザインやコンセプト、未来的なワクワク感", "長く使える定番ブランドという実績", "今までにない新しい機能やトレンド感"]},
        {"q": "小説や映画を観るとき、どこに一番惹かれる？", "c": ["現実に起こりそうなリアルな描写や設定", "独自の世界観や伏線、考察の余地があるストーリー", "登場人物の感情表現や美しい人間ドラマ", "迫力のある映像やテンポの良い展開"]},
        {"q": "明日の天気が怪しいとき、あなたはどう行動する？", "c": ["降水確率のデータを細かく見て傘を持つか決める", "空の様子や自分の勘を信じて決める", "とりあえず常に折りたたみ傘を鞄に入れておく", "濡れたらその時考えてコンビニで買う"]},
        {"q": "人からアドバイスをもらうなら、どちらのアプローチが嬉しい？", "c": ["具体的な手順や過去の実例に基づいたアドバイス", "抽象的なヒントや可能性を広げてくれるアドバイス", "自分の状況をすべて肯定してくれるアドバイス", "核心を突いた厳しいフィードバック"]},
        {"q": "「タイムマシン」があったら、行ってみたいのは？", "c": ["歴史上の事実を確かめに過去へ行く", "人類の未来やテクノロジーを見に未来へ行く", "自分の過去に戻って選択をやり直す", "自分の未来を見て人生の答え合わせをする"]}
    ],
    "判断の仕方": [
        {"q": "友人が仕事や恋の悩みを打ち明けてきたとき、最初に意識することは？", "c": ["相手の気持ちに寄り添って共感を示す", "客観的に状況を分析して具体的な解決策を考える", "とにかく話を最後まで否定せずに聴くことに徹する", "自分の経験談を交えてアドバイスをする"]},
        {"q": "話し合いの場で意見が対立したとき、あなたが最優先することは？", "c": ["論理的にどちらが正しいかを明確にすること", "お互いの感情に配慮して丸く収めること", "効率よく結論を出して次のステップへ進むこと", "全員の納得感が得られるまで話し合うこと"]},
        {"q": "買い物をしているとき、予算を少しオーバーしたお気に入りの商品を見つけたら？", "c": ["今回は冷静に諦めて予算内のものを探す", "自分のモチベーションが上がるならと感情に従って買う", "本当に価格に見合う価値があるか徹底的に比較検討する", "次の支出を削るという計画を立ててから買う"]},
        {"q": "人から褒められて一番嬉しい言葉はどちらに近い？", "c": ["「有能だね」「成果が素晴らしい」という能力への言葉", "「優しいね」「一緒にいると落ち着く」という人間性への言葉", "「センスが良いね」「個性的だね」という感性への言葉", "「いつも頑張っているね」というプロセスへの言葉"]},
        {"q": "ルールや規則について、あなたはどう考える？", "c": ["組織や社会の秩序を守るために厳守すべきもの", "状況や関わる人の事情に応じて柔軟に変えて良いもの", "効率を落とす原因になるなら見直すべきもの", "全員が不快な思いをしないために存在するもの"]},
        {"q": "旅行中に急なトラブル（電車の遅延など）が発生したとき、どう思う？", "c": ["すぐに次の最適なルートや代替案を冷静に探す", "パニックになったり、不穏な空気にならないよう周囲を気遣う", "これも旅の醍醐味としてトラブル自体を楽しむ", "計画が狂ったことに少しイライラしてしまう"]}
    ],
    "モノの決め方": [
        {"q": "旅行に行くときのスケジュールの立て方は？", "c": ["時間ごとに行く場所や店をキッチリ決めておく", "目的地だけ決めて、当日の気分で柔軟に動く", "ある程度の候補を挙げておき、大まかな流れだけ決める", "ノープランで行き当たりばったりの旅を楽しむ"]},
        {"q": "部屋の片付けや掃除のスタイルは？", "c": ["定期的にスケジュールを決めて綺麗に保つ", "散らかってきたと感じたら一気にまとめて片付ける", "常に使ったものは元の場所に戻す習慣がある", "来客があるなど、必要に迫られないとなかなかやらない"]},
        {"q": "仕事や課題、提出物に対する取り組み方は？", "c": ["締め切りから逆算して、計画的に余裕を持って終わらせる", "締め切り直前にならないと火がつかないが、爆発力で終わらせる", "毎日少しずつ均等に進めていく", "その日の気分やモチベーションに左右されやすい"]},
        {"q": "レストランで注文するメニューを決めるときは？", "c": ["席に着く前、あるいはメニューを見てすぐに直感で決める", "他の人の注文や全体のバランスを見てじっくり悩んで決める", "いつも頼むお気に入りの定番メニューを迷わず頼む", "その日の限定メニューやおすすめから選ぶ"]},
        {"q": "週末の予定が直前にキャンセルになったら、どう感じる？", "c": ["予定が狂ってしまい、少し損をした気分になる", "自分の自由時間が突然手に入ったと思って嬉しくなる", "すぐに別の友人や次の予定を入れようと動く", "特に何も気にせず、その場でやることを考える"]},
        {"q": "約束の時間に対するあなたの感覚は？", "c": ["5分から10分前には確実に到着していたい", "ぴったり、あるいは数分の遅れなら許容範囲だと思う", "相手が遅れても自分が遅れてもあまり気にしない", "遅れそうなときは事前に必ず連絡を入れる"]}
    ]
}

# ⚙️ セッション状態の管理
if 'step' not in st.session_state:
    st.session_state.step = "setup"
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'p1_answers' not in st.session_state:
    st.session_state.p1_answers = []
if 'p2_answers' not in st.session_state:
    st.session_state.p2_answers = []

# --- 1. 設定画面 ---
if st.session_state.step == "setup":
    st.subheader("PLAYER REGISTRATION")
    
    name1 = st.text_input("Player 1", placeholder="名前を入力")
    name2 = st.text_input("Player 2", placeholder="名前を入力")
    
    if st.button("START"):
        if name1 and name2:
            st.session_state.name1 = name1
            st.session_state.name2 = name2
            
            q_list = []
            for category, num in [("興味の方向", 2), ("モノの見方", 2), ("判断の仕方", 3), ("モノの決め方", 3)]:
                chosen = random.sample(QUESTION_POOL[category], num)
                for q in chosen:
                    q_list.append({"category": category, "q": q["q"], "c": q["c"]})
            random.shuffle(q_list)
            
            st.session_state.selected_questions = q_list
            st.session_state.step = "p1_turn"
            st.session_state.current_q = 0
            st.session_state.p1_answers = []
            st.session_state.p2_answers = []
            st.rerun()
        else:
            st.warning("両方の名前を入力してください。")

# --- 2. プレイヤー1の回答ターン ---
elif st.session_state.step == "p1_turn":
    idx = st.session_state.current_q
    questions = st.session_state.selected_questions
    
    st.subheader(f"TURN : {st.session_state.name1} ({idx + 1} / 10)")
    st.write(f"注意: {st.session_state.name2} さんに画面を見られないようにしてください。")
    st.progress((idx + 1) / 10)
    
    q_data = questions[idx]
    ans = st.radio(q_data["q"], q_data["c"], key=f"p1_ans_{idx}")
    
    if st.button("LOCK ANSWER"):
        st.session_state.p1_answers.append(ans)
        st.session_state.step = "change_turn"
        st.rerun()

# --- 3. 交代・目隠し画面 ---
elif st.session_state.step == "change_turn":
    st.subheader("PLAYER CHANGE")
    st.write("前のアナタの回答は安全に隠されました。")
    st.write(f"スマートフォンを {st.session_state.name2} さんに渡してください。")
    
    if st.button(f"{st.session_state.name2} の回答を始める"):
        st.session_state.step = "p2_turn"
        st.rerun()

# --- 4. プレイヤー2の回答ターン ---
elif st.session_state.step == "p2_turn":
    idx = st.session_state.current_q
    questions = st.session_state.selected_questions
    
    st.subheader(f"TURN : {st.session_state.name2} ({idx + 1} / 10)")
    st.progress((idx + 1) / 10)
    
    q_data = questions[idx]
    ans = st.radio(q_data["q"], q_data["c"], key=f"p2_ans_{idx}")
    
    if st.button("NEXT"):
        st.session_state.p2_answers.append(ans)
        if idx + 1 < 10:
            st.session_state.current_q += 1
            st.session_state.step = "p1_turn"
        else:
            st.session_state.step = "result"
        st.rerun()

# --- 5. 結果画面 ---
elif st.session_state.step == "result":
    questions = st.session_state.selected_questions
    p1_ans = st.session_state.p1_answers
    p2_ans = st.session_state.p2_answers
    
    categories = ["興味の方向", "モノの見方", "判断の仕方", "モノの決め方"]
    match_data = {cat: {"total": 0, "match": 0} for cat in categories}
    
    for i in range(10):
        cat = questions[i]["category"]
        match_data[cat]["total"] += 1
        if p1_ans[i] == p2_ans[i]:
            match_data[cat]["match"] += 1
            
    rates = {}
    for cat in categories:
        total = match_data[cat]["total"]
        match = match_data[cat]["match"]
        rates[cat] = int((match / total) * 100) if total > 0 else 0
        
    avg_sync_rate = int(sum(rates.values()) / 4)
    
    # ─── 画面上部：ファーストビュー ───
    st.markdown('<p class="result-score-label">SYNCHRONIZATION</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="result-score">{avg_sync_rate}%</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="result-names">{st.session_state.name1}  ×  {st.session_state.name2}</p>', unsafe_allow_html=True)
    
    if avg_sync_rate == 100:
        comment = "完璧に同期した脳内システム。すべての観点が一致する奇跡的な相性です。お互いの思考回路が手に取るようにわかるため、言葉を交わさずとも完璧に連動できる関係です。"
    elif avg_sync_rate >= 70:
        comment = "非常に高いシンクロ率です。物事の捉え方や意思決定のプロセスが酷似しており、一緒にいてストレスが全くありません。リズムが完璧に調和するベストパートナーです。"
    elif avg_sync_rate >= 40:
        comment = "バランスの取れた関係性です。似ている部分と異なる部分が丁度よく混ざり合っています。お互いに無い視点を補い合える、非常に建設的で居心地の良い組み合わせです。"
    else:
        comment = "予測不能な対極の存在です。思考システムが真逆だからこそ、自分には無い強烈な魅力を相手に感じる関係。衝突を繰り返しながらも新しい視点を生み出す刺激的な相性です。"
        
    st.markdown(f'<div class="result-comment">{comment}</div>', unsafe_allow_html=True)
    
    # ─── 画面下部：スクロールエリア ───
    st.markdown('<p class="section-title">DETAILED ANALYSIS</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    for idx, cat in enumerate(categories):
        rate = rates[cat]
        
        # ％によって色を決定
        if rate >= 80:
            graph_color = "#2ECC71" # 緑
        elif rate >= 40:
            graph_color = "#F1C40F" # 黄
        else:
            graph_color = "#E74C3C" # 赤
            
        # 🎨 CSSのconic-gradientを利用してインストール不要の美しい円グラフを生成
        pie_html = f"""
        <div class="pie-container">
            <p class="category-label">{cat}</p>
            <div class="pure-pie" style="background: conic-gradient({graph_color} 0% {rate}%, #EAEAEA {rate}% 100%);">
                <div class="pie-inner-hole">{rate}%</div>
            </div>
        </div>
        """
        
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            st.markdown(pie_html, unsafe_allow_html=True)
            
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    st.write("---")
    if st.button("RETRY"):
        st.session_state.step = "setup"
        st.rerun()
EOF
