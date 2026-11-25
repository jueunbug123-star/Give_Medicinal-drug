import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="동네 약국 조제 게임", layout="wide")

html_code = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>동네 약국 조제 게임</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

  * {
    box-sizing: border-box;
    user-select: none;
    font-family: 'Jua', sans-serif;
  }

  body {
    margin: 0;
    padding: 15px;
    background-color: #f6e6d0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
  }

  .game-container {
    width: 100%;
    max-width: 820px;
    background-color: #fff8ee;
    border: 5px solid #6b4423;
    border-radius: 24px;
    box-shadow: 0 10px 25px rgba(107, 68, 35, 0.25);
    overflow: hidden;
  }

  /* 상단 정보 바 */
  .header-bar {
    background-color: #e8998d;
    border-bottom: 4px solid #6b4423;
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
  }

  .title-badge {
    background-color: #fff8ee;
    border: 3px solid #6b4423;
    border-radius: 15px;
    padding: 5px 15px;
    font-size: 20px;
    color: #5c3a21;
  }

  .status-group {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }

  .stat-pill {
    background-color: #fff3d6;
    border: 3px solid #6b4423;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 16px;
    color: #5c3a21;
  }

  .btn-small {
    background-color: #ffd166;
    border: 3px solid #6b4423;
    border-radius: 14px;
    padding: 6px 12px;
    font-size: 15px;
    color: #5c3a21;
    cursor: pointer;
    transition: transform 0.1s;
  }

  .btn-small:active {
    transform: scale(0.95);
  }

  .btn-hint-on {
    background-color: #a8e6cf;
  }

  /* 상단 카운터(손님 영역) */
  .shop-scene {
    position: relative;
    background: repeating-linear-gradient(
      90deg,
      #fcebd5,
      #fcebd5 35px,
      #f8dec0 35px,
      #f8dec0 70px
    );
    height: 290px;
    border-bottom: 5px solid #6b4423;
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    padding: 20px 25px 0 25px;
  }

  .customer-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 2;
    transition: transform 0.3s ease;
  }

  .customer-name-tag {
    background-color: #6b4423;
    color: #fff8ee;
    padding: 4px 14px;
    border-radius: 12px;
    font-size: 16px;
    margin-bottom: -8px;
    z-index: 3;
  }

  .customer-avatar {
    width: 145px;
    height: 175px;
  }

  /* 말풍선 */
  .speech-bubble {
    position: relative;
    background-color: #ffffff;
    border: 4px solid #6b4423;
    border-radius: 22px;
    padding: 16px 22px;
    max-width: 440px;
    width: 100%;
    margin-bottom: 35px;
    box-shadow: 4px 4px 0px rgba(107, 68, 35, 0.15);
  }

  .speech-bubble::before {
    content: "";
    position: absolute;
    left: -20px;
    bottom: 30px;
    border-width: 12px 20px 12px 0;
    border-style: solid;
    border-color: transparent #6b4423 transparent transparent;
  }

  .speech-bubble::after {
    content: "";
    position: absolute;
    left: -13px;
    bottom: 33px;
    border-width: 9px 15px 9px 0;
    border-style: solid;
    border-color: transparent #ffffff transparent transparent;
  }

  .symptom-title {
    font-size: 22px;
    color: #d9534f;
    margin: 0 0 6px 0;
  }

  .symptom-desc {
    font-size: 18px;
    color: #4a3525;
    margin: 0 0 10px 0;
  }

  .recipe-hint-box {
    background-color: #fff6d6;
    border: 2px dashed #d49b35;
    border-radius: 12px;
    padding: 8px 12px;
    font-size: 16px;
    color: #7a4e13;
  }

  /* 조제대(나무 테이블) 영역 */
  .counter-area {
    background-color: #c98a55;
    padding: 18px 20px 24px 20px;
  }

  .tray-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #b0723e;
    border: 4px solid #6b4423;
    border-radius: 18px;
    padding: 12px 18px;
    margin-bottom: 18px;
    flex-wrap: wrap;
    gap: 12px;
  }

  .plate-wrapper {
    display: flex;
    align-items: center;
    gap: 15px;
  }

  .plate-label {
    color: #fff8ee;
    font-size: 18px;
    text-shadow: 1px 1px 0 #6b4423;
  }

  .medicine-plate {
    display: flex;
    gap: 10px;
    background-color: #f7ead7;
    border: 4px solid #6b4423;
    border-radius: 50px;
    padding: 8px 20px;
    min-width: 170px;
    min-height: 62px;
    align-items: center;
    justify-content: center;
  }

  .plate-slot {
    background-color: #ffd166;
    border: 3px solid #6b4423;
    border-radius: 12px;
    padding: 5px 14px;
    font-size: 20px;
    color: #5c3a21;
  }

  .plate-empty {
    color: #a68b72;
    font-size: 15px;
  }

  .action-buttons {
    display: flex;
    gap: 10px;
  }

  .btn-clear {
    background-color: #f4a261;
    border: 3px solid #6b4423;
    border-radius: 14px;
    padding: 10px 16px;
    font-size: 17px;
    color: #fff;
    cursor: pointer;
    box-shadow: 0 3px 0 #6b4423;
  }

  .btn-give {
    background-color: #52b788;
    border: 3px solid #6b4423;
    border-radius: 14px;
    padding: 10px 22px;
    font-size: 18px;
    color: #fff;
    cursor: pointer;
    box-shadow: 0 3px 0 #6b4423;
  }

  .btn-clear:active, .btn-give:active {
    transform: translateY(2px);
    box-shadow: 0 1px 0 #6b4423;
  }

  /* 약 보관함 5칸 */
  .medicine-shelf {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
  }

  @media (max-width: 600px) {
    .medicine-shelf {
      grid-template-columns: repeat(3, 1fr);
    }
    .shop-scene {
      flex-direction: column;
      height: auto;
      align-items: center;
      padding-top: 15px;
    }
    .speech-bubble::before, .speech-bubble::after {
      display: none;
    }
  }

  .med-box {
    position: relative;
    background-color: #f9eedc;
    border: 4px solid #6b4423;
    border-radius: 18px;
    padding: 12px 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: transform 0.12s, background-color 0.2s;
    box-shadow: 0 4px 0 #6b4423;
  }

  .med-box:hover {
    background-color: #fffdf9;
    transform: translateY(-3px);
  }

  .med-box:active {
    transform: translateY(2px);
    box-shadow: 0 1px 0 #6b4423;
  }

  /* 필요한 약 하이라이트 */
  .med-box.recommended {
    border-color: #f59e0b;
    background-color: #fffbe6;
    box-shadow: 0 0 14px rgba(245, 158, 11, 0.75), 0 4px 0 #b45309;
  }

  .need-badge {
    position: absolute;
    top: -10px;
    right: -6px;
    background-color: #f59e0b;
    color: #fff;
    border: 2px solid #6b4423;
    border-radius: 10px;
    padding: 2px 8px;
    font-size: 13px;
  }

  .med-key {
    background-color: #6b4423;
    color: #fff8ee;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 6px;
  }

  .med-desc {
    font-size: 14px;
    color: #5c3a21;
    margin-top: 6px;
    text-align: center;
  }

  /* 피드백 알림 배너 */
  .feedback-banner {
    position: fixed;
    top: 25px;
    left: 50%;
    transform: translateX(-50%);
    padding: 12px 26px;
    border-radius: 20px;
    border: 4px solid #6b4423;
    font-size: 20px;
    color: #fff;
    z-index: 100;
    display: none;
    box-shadow: 0 6px 15px rgba(0,0,0,0.2);
  }

  /* 모달 (처방전 도감 & 최종 결과) */
  .modal-overlay {
    position: fixed;
    inset: 0;
    background-color: rgba(60, 40, 20, 0.6);
    display: none;
    justify-content: center;
    align-items: center;
    z-index: 200;
    padding: 15px;
  }

  .modal-card {
    background-color: #fff8ee;
    border: 5px solid #6b4423;
    border-radius: 24px;
    padding: 24px;
    max-width: 480px;
    width: 100%;
    text-align: center;
    max-height: 85vh;
    overflow-y: auto;
  }

  .modal-title {
    font-size: 24px;
    color: #5c3a21;
    margin-top: 0;
  }

  .recipe-list {
    list-style: none;
    padding: 0;
    margin: 15px 0;
    text-align: left;
  }

  .recipe-list li {
    background-color: #f9eedc;
    border: 3px solid #6b4423;
    border-radius: 14px;
    padding: 10px 14px;
    margin-bottom: 10px;
    font-size: 17px;
    color: #4a3525;
  }

  .result-log {
    text-align: left;
    background-color: #f9eedc;
    border: 3px solid #6b4423;
    border-radius: 14px;
    padding: 10px 14px;
    margin: 12px 0;
    font-size: 15px;
    max-height: 220px;
    overflow-y: auto;
  }
</style>
</head>
<body>

<div id="feedbackBanner" class="feedback-banner"></div>

<div class="game-container">
  <!-- 상단 상태 바 -->
  <div class="header-bar">
    <div class="title-badge">🌿 포근한 동네 약국</div>
    <div class="status-group">
      <div class="stat-pill">손님: <span id="progressText">1</span> / 10명</div>
      <div class="stat-pill">점수: <span id="scoreText">0</span>점</div>
      <button id="hintToggleBtn" class="btn-small btn-hint-on" onclick="toggleHint()">💡 약 표시: ON</button>
      <button class="btn-small" onclick="openRecipeModal()">📖 처방전 보기</button>
    </div>
  </div>

  <!-- 손님 카운터 화면 -->
  <div class="shop-scene">
    <div class="customer-box" id="customerBox">
      <div class="customer-name-tag" id="customerNameTag">김씨 환자</div>
      <div class="customer-avatar" id="customerSvg"></div>
    </div>

    <div class="speech-bubble">
      <div class="symptom-title" id="symptomTitle">배가 너무 아파요!</div>
      <div class="symptom-desc" id="symptomDesc">"속이 쓰리고 배가 살살 아파서 왔어요."</div>
      <div class="recipe-hint-box" id="recipeHintBox">📋 필요한 약: ㄱ + ㄴ</div>
    </div>
  </div>

  <!-- 하단 조제대 및 약 보관함 -->
  <div class="counter-area">
    <div class="tray-section">
      <div class="plate-wrapper">
        <span class="plate-label">🍽️ 약 접시:</span>
        <div class="medicine-plate" id="plateArea">
          <span class="plate-empty">아래에서 약 2개를 선택하세요</span>
        </div>
      </div>
      <div class="action-buttons">
        <button class="btn-clear" onclick="clearPlate()">비우기</button>
        <button class="btn-give" onclick="serveMedicine()">약 건네주기 ✔</button>
      </div>
    </div>

    <div class="medicine-shelf" id="medicineShelf"></div>
  </div>
</div>

<!-- 처방전 도감 모달 -->
<div class="modal-overlay" id="recipeModal">
  <div class="modal-card">
    <h2 class="modal-title">📖 동네 약국 표준 처방전</h2>
    <ul class="recipe-list">
      <li>🤢 <strong>배 아픔 (복통)</strong> ➔ <strong>ㄱ + ㄴ</strong> 약</li>
      <li>🤕 <strong>머리 아픔 (두통)</strong> ➔ <strong>ㄷ + ㄹ</strong> 약</li>
      <li>💓 <strong>가슴 아픔 (흉통)</strong> ➔ <strong>ㄴ + ㅁ</strong> 약</li>
      <li>🤮 <strong>구토 (울렁거림)</strong> ➔ <strong>ㄱ + ㅁ</strong> 약</li>
    </ul>
    <button class="btn-give" onclick="closeRecipeModal()">닫기</button>
  </div>
</div>

<!-- 10명 완료 결과 모달 -->
<div class="modal-overlay" id="resultModal">
  <div class="modal-card">
    <h2 class="modal-title">🎉 오늘의 약국 영업 종료!</h2>
    <p style="font-size: 20px; color: #5c3a21;">최종 점수: <strong id="finalScore">0</strong> / 100점</p>
    <div class="result-log" id="resultLog"></div>
    <button class="btn-give" onclick="initGame()">다시 10명 받기 🔄</button>
  </div>
</div>

<script>
  // 5가지 약 정보
  const MEDICINES = [
    {
      id: "ㄱ",
      name: "따뜻한 알약",
      svg: '<svg width="54" height="54" viewBox="0 0 60 60"><rect x="14" y="20" width="32" height="20" rx="10" fill="#ff7b7b" stroke="#6b4423" stroke-width="3"/><path d="M30 20 H36 A10 10 0 0 1 36 40 H30 Z" fill="#ffd166" stroke="#6b4423" stroke-width="3"/></svg>'
    },
    {
      id: "ㄴ",
      name: "파란 물약병",
      svg: '<svg width="54" height="54" viewBox="0 0 60 60"><rect x="24" y="10" width="12" height="8" rx="2" fill="#d4a373" stroke="#6b4423" stroke-width="3"/><rect x="18" y="18" width="24" height="32" rx="8" fill="#74c0fc" stroke="#6b4423" stroke-width="3"/><circle cx="30" cy="34" r="5" fill="#fff"/></svg>'
    },
    {
      id: "ㄷ",
      name: "초록 약초잎",
      svg: '<svg width="54" height="54" viewBox="0 0 60 60"><path d="M15 42 C15 20, 45 15, 45 15 C45 15, 45 45, 15 42 Z" fill="#8ce99a" stroke="#6b4423" stroke-width="3"/><path d="M15 42 L38 22" stroke="#6b4423" stroke-width="3" stroke-linecap="round"/></svg>'
    },
    {
      id: "ㄹ",
      name: "하얀 정제약",
      svg: '<svg width="54" height="54" viewBox="0 0 60 60"><circle cx="30" cy="30" r="16" fill="#ffffff" stroke="#6b4423" stroke-width="3"/><line x1="18" y1="30" x2="42" y2="30" stroke="#6b4423" stroke-width="3"/></svg>'
    },
    {
      id: "ㅁ",
      name: "보라 가루약",
      svg: '<svg width="54" height="54" viewBox="0 0 60 60"><polygon points="30,12 48,46 12,46" fill="#d0bfff" stroke="#6b4423" stroke-width="3"/><circle cx="30" cy="35" r="4" fill="#fff"/></svg>'
    }
  ];

  // 4가지 증상 및 필요한 약 조합
  const SYMPTOMS = [
    {
      type: "stomach",
      title: "배가 너무 아파요! (복통)",
      desc: "배가 살살 아프고 속이 편하지 않아요.",
      required: ["ㄱ", "ㄴ"],
      shirtColor: "#f4a261",
      svg: '<svg viewBox="0 0 140 160" width="140" height="160"><ellipse cx="70" cy="145" rx="45" ry="25" fill="#f4a261" stroke="#6b4423" stroke-width="4"/><circle cx="70" cy="75" r="38" fill="#ffe0bd" stroke="#6b4423" stroke-width="4"/><path d="M32 68 C32 35, 108 35, 108 68 C95 52, 45 52, 32 68 Z" fill="#5c3a21"/><path d="M52 72 L62 77 L52 82" fill="none" stroke="#6b4423" stroke-width="3" stroke-linecap="round"/><path d="M88 72 L78 77 L88 82" fill="none" stroke="#6b4423" stroke-width="3" stroke-linecap="round"/><path d="M60 95 Q70 88 80 95" fill="none" stroke="#6b4423" stroke-width="3" stroke-linecap="round"/><circle cx="46" cy="84" r="5" fill="#ff9999" opacity="0.7"/><circle cx="94" cy="84" r="5" fill="#ff9999" opacity="0.7"/></svg>'
    },
    {
      type: "head",
      title: "머리가 지끈거려요! (두통)",
      desc: "머리가 욱신거리고 어지러워서 왔어요.",
      required: ["ㄷ", "ㄹ"],
      shirtColor: "#74c0fc",
      svg: '<svg viewBox="0 0 140 160" width="140" height="160"><ellipse cx="70" cy="145" rx="45" ry="25" fill="#74c0fc" stroke="#6b4423" stroke-width="4"/><circle cx="70" cy="75" r="38" fill="#ffe0bd" stroke="#6b4423" stroke-width="4"/><path d="M32 65 C35 30, 105 30, 108 65 Z" fill="#3d2b1f"/><path d="M50 75 Q56 80 62 75" fill="none" stroke="#6b4423" stroke-width="3"/><path d="M78 75 Q84 80 90 75" fill="none" stroke="#6b4423" stroke-width="3"/><path d="M62 94 Q70 90 78 94" fill="none" stroke="#6b4423" stroke-width="3"/><path d="M105 42 L118 32 M110 52 L123 48" stroke="#e03131" stroke-width="3" stroke-linecap="round"/></svg>'
    },
    {
      type: "chest",
      title: "가슴이 답답하고 아파요! (흉통)",
      desc: "가슴 쪽이 콕콕 쑤시고 답답한 느낌이에요.",
      required: ["ㄴ", "ㅁ"],
      shirtColor: "#b197fc",
      svg: '<svg viewBox="0 0 140 160" width="140" height="160"><ellipse cx="70" cy="145" rx="45" ry="25" fill="#b197fc" stroke="#6b4423" stroke-width="4"/><circle cx="70" cy="75" r="38" fill="#ffe0bd" stroke="#6b4423" stroke-width="4"/><path d="M30 70 C30 32, 110 32, 110 70 C90 55, 50 55, 30 70 Z" fill="#7f4f24"/><circle cx="56" cy="75" r="3.5" fill="#6b4423"/><circle cx="84" cy="75" r="3.5" fill="#6b4423"/><ellipse cx="70" cy="94" rx="6" ry="4" fill="#e03131"/><path d="M65 132 C65 126, 75 126, 75 132 C75 138, 70 142, 70 142 C70 142, 65 138, 65 132 Z" fill="#ff6b6b"/></svg>'
    },
    {
      type: "vomit",
      title: "속이 울렁거리고 구토가 나요! (구토)",
      desc: "먹은 게 얹혔는지 계속 토할 것 같아요.",
      required: ["ㄱ", "ㅁ"],
      shirtColor: "#8ce99a",
      svg: '<svg viewBox="0 0 140 160" width="140" height="160"><ellipse cx="70" cy="145" rx="45" ry="25" fill="#8ce99a" stroke="#6b4423" stroke-width="4"/><circle cx="70" cy="75" r="38" fill="#e6f2d5" stroke="#6b4423" stroke-width="4"/><path d="M32 68 C32 34, 108 34, 108 68 Z" fill="#4a3525"/><path d="M51 74 L61 74" stroke="#6b4423" stroke-width="3" stroke-linecap="round"/><path d="M79 74 L89 74" stroke="#6b4423" stroke-width="3" stroke-linecap="round"/><path d="M58 93 Q64 89 70 93 Q76 97 82 93" fill="none" stroke="#6b4423" stroke-width="3" stroke-linecap="round"/><circle cx="70" cy="102" r="9" fill="#ffe0bd" stroke="#6b4423" stroke-width="2.5"/></svg>'
    }
  ];

  // 5가지 랜덤 성씨
  const LAST_NAMES = ["김씨", "박씨", "최씨", "임씨", "이씨"];

  let queue = [];
  let currentIndex = 0;
  let selectedMeds = [];
  let score = 0;
  let showHint = true;
  let historyLogs = [];

  function initGame() {
    queue = [];
    selectedMeds = [];
    currentIndex = 0;
    score = 0;
    historyLogs = [];

    // 10명의 랜덤 환자 생성 (성씨 + 증상 랜덤 조합)
    for (let i = 0; i < 10; i++) {
      const randomName = LAST_NAMES[Math.floor(Math.random() * LAST_NAMES.length)];
      const randomSymptom = SYMPTOMS[Math.floor(Math.random() * SYMPTOMS.length)];
      queue.push({
        name: randomName,
        symptom: randomSymptom
      });
    }

    document.getElementById("resultModal").style.display = "none";
    renderShelf();
    updateUI();
  }

  function renderShelf() {
    const shelf = document.getElementById("medicineShelf");
    shelf.innerHTML = "";
    const currentReq = queue[currentIndex] ? queue[currentIndex].symptom.required : [];

    MEDICINES.forEach(med => {
      const isNeeded = showHint && currentReq.includes(med.id);
      const box = document.createElement("div");
      box.className = "med-box" + (isNeeded ? " recommended" : "");
      box.onclick = () => selectMedicine(med.id);

      box.innerHTML =
        (isNeeded ? '<div class="need-badge">필요!</div>' : '') +
        '<div class="med-key">' + med.id + '</div>' +
        med.svg +
        '<div class="med-desc">' + med.name + '</div>';

      shelf.appendChild(box);
    });
  }

  function updateUI() {
    const current = queue[currentIndex];
    document.getElementById("progressText").innerText = currentIndex + 1;
    document.getElementById("scoreText").innerText = score;
    document.getElementById("customerNameTag").innerText = (currentIndex + 1) + "번째 손님 · " + current.name;
    document.getElementById("customerSvg").innerHTML = current.symptom.svg;
    document.getElementById("symptomTitle").innerText = current.symptom.title;
    document.getElementById("symptomDesc").innerText = '"' + current.symptom.desc + '"';

    const hintBox = document.getElementById("recipeHintBox");
    if (showHint) {
      const reqNames = current.symptom.required.map(id => {
        const found = MEDICINES.find(m => m.id === id);
        return id + " (" + found.name + ")";
      });
      hintBox.style.display = "block";
      hintBox.innerHTML = "📋 <strong>필요한 약:</strong> " + reqNames.join(" + ");
    } else {
      hintBox.style.display = "none";
    }

    renderPlate();
    renderShelf();
  }

  function renderPlate() {
    const plate = document.getElementById("plateArea");
    if (selectedMeds.length === 0) {
      plate.innerHTML = '<span class="plate-empty">아래에서 약 2개를 선택하세요</span>';
      return;
    }
    plate.innerHTML = selectedMeds
      .map(id => '<div class="plate-slot">' + id + ' 약</div>')
      .join("");
  }

  function selectMedicine(id) {
    if (selectedMeds.length >= 2) {
      showBanner("약 접시에는 최대 2개까지만 담을 수 있어요!", "#e03131");
      return;
    }
    selectedMeds.push(id);
    renderPlate();
  }

  function clearPlate() {
    selectedMeds = [];
    renderPlate();
  }

  function serveMedicine() {
    if (selectedMeds.length < 2) {
      showBanner("약 2개를 모두 골라서 접시에 담아주세요!", "#f59e0b");
      return;
    }

    const current = queue[currentIndex];
    const requiredSorted = [...current.symptom.required].sort().join(",");
    const selectedSorted = [...selectedMeds].sort().join(",");
    const isCorrect = requiredSorted === selectedSorted;

    if (isCorrect) {
      score += 10;
      showBanner("정확한 처방이에요! " + current.name + " 손님이 완쾌했습니다 (+10점)", "#2b8a3e");
    } else {
      showBanner("아쉬워요! 정답은 [" + current.symptom.required.join(" + ") + "] 약이었어요.", "#c92a2a");
    }

    historyLogs.push(
      (currentIndex + 1) + ". <strong>" + current.name + "</strong> (" + current.symptom.title.split(" ")[0] + ") ➔ " +
      (isCorrect ? "✅ 성공" : "❌ 오답 (정답: " + current.symptom.required.join("+") + ")")
    );

    selectedMeds = [];
    currentIndex++;

    if (currentIndex >= queue.length) {
      setTimeout(showFinalResult, 700);
    } else {
      updateUI();
    }
  }

  function toggleHint() {
    showHint = !showHint;
    const btn = document.getElementById("hintToggleBtn");
    if (showHint) {
      btn.innerText = "💡 약 표시: ON";
      btn.classList.add("btn-hint-on");
    } else {
      btn.innerText = "💡 약 표시: OFF";
      btn.classList.remove("btn-hint-on");
    }
    updateUI();
  }

  function showBanner(msg, bgColor) {
    const banner = document.getElementById("feedbackBanner");
    banner.innerText = msg;
    banner.style.backgroundColor = bgColor;
    banner.style.display = "block";
    clearTimeout(window.bannerTimer);
    window.bannerTimer = setTimeout(() => {
      banner.style.display = "none";
    }, 1800);
  }

  function openRecipeModal() {
    document.getElementById("recipeModal").style.display = "flex";
  }

  function closeRecipeModal() {
    document.getElementById("recipeModal").style.display = "none";
  }

  function showFinalResult() {
    document.getElementById("finalScore").innerText = score;
    document.getElementById("resultLog").innerHTML = historyLogs.join("<br>");
    document.getElementById("resultModal").style.display = "flex";
  }

  initGame();
</script>
</body>
</html>'''

components.html(html_code, height=820, scrolling=True)
