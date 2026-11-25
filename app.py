import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="동네 약국 조제 게임", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>포근한 동네 약국 - 약 조제 게임</title>
    <!-- 손그림 감성과 어울리는 둥글고 따뜻한 한국어 웹폰트 (Jua & Gowun Dodum) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Jua&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- 효과음 생성을 위한 Tone.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
    <style>
        /* 전체 폰트 및 손그림 외곽선/파스텔 톤 스타일 */
        body {
            font-family: 'Gowun Dodum', sans-serif;
            background-color: #f7ebd9;
            color: #4a3525;
            user-select: none;
            overflow-x: hidden;
        }

        h1, h2, h3, .font-jua {
            font-family: 'Jua', sans-serif;
        }

        /* 포근한 상점 벽지 패턴 */
        .cozy-wallpaper {
            background-color: #fcf3e3;
            background-image: 
                radial-gradient(#f2dec4 2px, transparent 2px),
                radial-gradient(#ebd0b0 2px, #fcf3e3 2px);
            background-size: 40px 40px;
            background-position: 0 0, 20px 20px;
        }

        /* 손그림풍 두꺼운 갈색 테두리와 입체 그림자 */
        .hand-drawn-box {
            border: 3.5px solid #593a27;
            box-shadow: 0 5px 0 #593a27;
            border-radius: 20px;
        }

        .hand-drawn-sm {
            border: 3px solid #593a27;
            box-shadow: 0 3px 0 #593a27;
            border-radius: 14px;
        }

        /* 나무 조제대 질감 */
        .wood-counter {
            background: linear-gradient(180deg, #d99b66 0%, #c4814b 100%);
            border-top: 4px solid #593a27;
        }

        .wood-tray-area {
            background-color: #b5733e;
            background-image: repeating-linear-gradient(
                90deg,
                rgba(89, 58, 39, 0.08) 0px,
                rgba(89, 58, 39, 0.08) 4px,
                transparent 4px,
                transparent 36px
            );
            border-top: 4px solid #593a27;
        }

        /* 약 보관함 칸 (레퍼런스 1번 이미지의 토핑 통 스타일) */
        .med-compartment {
            background-color: #fff6e8;
            border: 3.5px solid #593a27;
            box-shadow: inset 0 4px 8px rgba(89, 58, 39, 0.15), 0 4px 0 #593a27;
            border-radius: 18px;
            transition: transform 0.12s ease, background-color 0.15s ease;
        }

        .med-compartment:hover:not(:disabled) {
            transform: translateY(-4px);
            background-color: #fffdf9;
        }

        .med-compartment:active:not(:disabled) {
            transform: translateY(2px);
            box-shadow: inset 0 4px 8px rgba(89, 58, 39, 0.2), 0 1px 0 #593a27;
        }

        .med-compartment.selected {
            background-color: #ffe8a3;
            border-color: #d97706;
        }

        /* 현재 환자에게 필요한 약통 강조 (황금빛 테두리 + 은은한 반짝임) */
        @keyframes pulseGold {
            0%, 100% { box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.45), 0 4px 0 #593a27; }
            50% { box-shadow: 0 0 14px 5px rgba(245, 158, 11, 0.85), 0 4px 0 #593a27; }
        }

        .med-compartment.recommended {
            border-color: #d97706;
            background-color: #fffbeb;
            animation: pulseGold 1.8s infinite ease-in-out;
        }

        .med-compartment.recommended.selected {
            background-color: #fde68a;
            animation: none;
        }

        /* 나무 약 접시 (도마/쟁반 스타일) */
        .wooden-dish {
            background: radial-gradient(circle, #f3c894 60%, #dfa668 100%);
            border: 4px solid #593a27;
            box-shadow: 0 6px 0 #593a27, inset 0 0 12px rgba(139, 83, 41, 0.3);
        }

        /* 애니메이션 효과 */
        @keyframes floatGentle {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-5px); }
        }

        @keyframes popIn {
            0% { transform: scale(0.6); opacity: 0; }
            75% { transform: scale(1.08); opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20%, 60% { transform: translateX(-8px); }
            40%, 80% { transform: translateX(8px); }
        }

        @keyframes patientEnter {
            0% { transform: translateX(-60px) scale(0.95); opacity: 0; }
            100% { transform: translateX(0) scale(1); opacity: 1; }
        }

        .animate-float {
            animation: floatGentle 2.8s ease-in-out infinite;
        }

        .animate-pop {
            animation: popIn 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }

        .animate-shake {
            animation: shake 0.4s ease-in-out;
        }

        .animate-enter {
            animation: patientEnter 0.45s ease-out forwards;
        }

        /* 말풍선 꼬리 */
        .speech-bubble::after {
            content: '';
            position: absolute;
            left: -14px;
            top: 50%;
            transform: translateY(-50%);
            border-width: 10px 14px 10px 0;
            border-style: solid;
            border-color: transparent #593a27 transparent transparent;
        }

        .speech-bubble::before {
            content: '';
            position: absolute;
            left: -9px;
            top: 50%;
            transform: translateY(-50%);
            border-width: 8px 11px 8px 0;
            border-style: solid;
            border-color: transparent #ffffff transparent transparent;
            z-index: 1;
        }

        @media (max-width: 640px) {
            .speech-bubble::after, .speech-bubble::before {
                display: none;
            }
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-center p-2 sm:p-4">

    <!-- 메인 게임 프레임 -->
    <div id="game-app" class="w-full max-w-4xl bg-[#fff9f0] hand-drawn-box overflow-hidden flex flex-col relative">
        
        <!-- 1. 상단 리본 헤더 (레퍼런스 이미지의 분홍 리본 배너 스타일) -->
        <header class="bg-[#e88d72] border-b-4 border-[#593a27] px-4 py-2.5 flex flex-wrap items-center justify-between gap-2 z-20">
            <div class="flex items-center gap-2">
                <span class="bg-[#fff6e8] text-[#593a27] font-jua px-3 py-1 rounded-full border-2 border-[#593a27] text-sm sm:text-base shadow-sm">
                    🌿 포근한 동네 약국
                </span>
                <span id="progress-badge" class="bg-[#ffe49e] text-[#593a27] font-jua px-3 py-1 rounded-full border-2 border-[#593a27] text-sm sm:text-base">
                    환자 1 / 10
                </span>
            </div>

            <div class="flex items-center gap-2 sm:gap-3">
                <!-- 점수 표시 -->
                <div class="bg-[#fff6e8] px-3 py-1 rounded-full border-2 border-[#593a27] flex items-center gap-1.5 font-jua text-sm sm:text-base">
                    <span>⭐ 성공:</span>
                    <span id="score-display" class="text-[#d96b43] text-lg">0</span>
                    <span>명</span>
                </div>

                <!-- 알맞은 약 표시 ON/OFF 토글 버튼 -->
                <button id="guide-toggle-btn" onclick="toggleMedicineGuide()" class="bg-[#ffe49e] hover:bg-[#ffd875] active:translate-y-0.5 text-[#3a2618] font-jua px-3 py-1 rounded-full border-2 border-[#593a27] text-sm sm:text-base flex items-center gap-1 transition cursor-pointer shadow-sm">
                    💡 약 표시: ON
                </button>

                <!-- 처방전 도감(레시피) 버튼 -->
                <button id="recipe-btn" onclick="toggleRecipeModal(true)" class="bg-[#a8d5ba] hover:bg-[#95c9aa] active:translate-y-0.5 text-[#3a2618] font-jua px-3 py-1 rounded-full border-2 border-[#593a27] text-sm sm:text-base flex items-center gap-1 transition cursor-pointer shadow-sm">
                    📖 처방전 보기
                </button>
            </div>
        </header>

        <!-- 2. 상단 카운터 뷰 (레퍼런스 2번 이미지: 아늑한 가게 배경 + 환자 + 말풍선) -->
        <section class="cozy-wallpaper relative px-4 pt-5 pb-3 sm:px-8 sm:pt-6 flex flex-col justify-between min-h-[260px] sm:min-h-[290px]">
            
            <!-- 배경 장식 소품 (선반, 화분, 액자 등) -->
            <div class="absolute top-3 left-6 opacity-80 hidden sm:block pointer-events-none">
                <!-- 벽걸이 허브 리스 SVG -->
                <svg width="58" height="58" viewBox="0 0 60 60">
                    <circle cx="30" cy="30" r="22" fill="none" stroke="#789c6a" stroke-width="8" stroke-dasharray="6 4"/>
                    <circle cx="30" cy="30" r="22" fill="none" stroke="#593a27" stroke-width="2"/>
                    <circle cx="16" cy="18" r="4" fill="#f2b84b" stroke="#593a27" stroke-width="1.5"/>
                    <circle cx="44" cy="20" r="4" fill="#e88d72" stroke="#593a27" stroke-width="1.5"/>
                    <circle cx="28" cy="50" r="4" fill="#f2b84b" stroke="#593a27" stroke-width="1.5"/>
                </svg>
            </div>

            <div class="absolute top-3 right-6 opacity-85 hidden sm:block pointer-events-none">
                <!-- 약초 병 선반 SVG -->
                <svg width="95" height="65" viewBox="0 0 100 70">
                    <rect x="5" y="52" width="90" height="8" rx="3" fill="#c4814b" stroke="#593a27" stroke-width="2.5"/>
                    <rect x="16" y="24" width="22" height="28" rx="5" fill="#d4e8d1" stroke="#593a27" stroke-width="2.5"/>
                    <rect x="20" y="18" width="14" height="6" rx="2" fill="#8c583a" stroke="#593a27" stroke-width="2"/>
                    <rect x="52" y="28" width="26" height="24" rx="6" fill="#fce1a6" stroke="#593a27" stroke-width="2.5"/>
                    <rect x="57" y="22" width="16" height="6" rx="2" fill="#8c583a" stroke="#593a27" stroke-width="2"/>
                </svg>
            </div>

            <!-- 환자 캐릭터 및 증상 말풍선 영역 -->
            <div class="relative z-10 flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-7 my-auto">
                
                <!-- 환자 일러스트 컨테이너 -->
                <div id="patient-container" class="flex flex-col items-center animate-enter">
                    <div id="patient-avatar" class="w-32 h-32 sm:w-36 sm:h-36 flex items-center justify-center animate-float">
                        <!-- 자바스크립트에서 사용자1, 2, 3 SVG 일러스트가 렌더링됩니다 -->
                    </div>
                    <span id="patient-name-tag" class="mt-1 bg-[#593a27] text-[#fff6e8] font-jua text-sm px-3.5 py-0.5 rounded-full tracking-wide shadow">
                        사용자 1
                    </span>
                </div>

                <!-- 환자 대사 말풍선 -->
                <div id="speech-box" class="speech-bubble relative bg-white hand-drawn-sm px-5 py-3.5 max-w-xs sm:max-w-sm text-center sm:text-left animate-pop">
                    <div class="flex items-center justify-center sm:justify-start gap-2 mb-1">
                        <span id="symptom-badge" class="bg-[#ffe2d9] text-[#b84325] font-jua text-xs sm:text-sm px-2.5 py-0.5 rounded-full border border-[#593a27]">
                            증상: 배 아픔
                        </span>
                    </div>
                    <p id="patient-dialogue" class="font-jua text-lg sm:text-xl text-[#4a3525] leading-snug">
                        "아이고... 배가 너무 콕콕 쑤시고 아파요!"
                    </p>
                    <!-- 현재 환자에게 필요한 약 자동 표시 메모 -->
                    <div id="auto-rx-box" class="mt-2.5 bg-[#fff8e7] border-2 border-dashed border-[#d97706] rounded-xl px-3 py-1.5 flex items-center justify-center sm:justify-start gap-2">
                        <span class="font-jua text-xs sm:text-sm text-[#92400e]">📋 필요한 약:</span>
                        <div id="required-meds-badges" class="flex items-center gap-1.5 font-jua text-sm sm:text-base">
                            <!-- 자바스크립트에서 현재 환자의 정답 약 배지(예: [ㄱ] + [ㄴ])가 표시됩니다 -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- 피드백 오버레이 알림 (정답/오답 시 화면 중앙 팝업) -->
            <div id="feedback-banner" class="hidden absolute inset-0 z-30 flex items-center justify-center bg-black/20 backdrop-blur-[1px]">
                <div id="feedback-card" class="bg-white hand-drawn-box px-7 py-5 text-center max-w-xs mx-4 animate-pop">
                    <div id="feedback-emoji" class="text-5xl mb-2">😊</div>
                    <h3 id="feedback-title" class="font-jua text-2xl text-[#4a3525] mb-1">처방 성공!</h3>
                    <p id="feedback-desc" class="text-sm text-[#6b4f3a]">환자의 아픔이 싹 나았어요!</p>
                </div>
            </div>
        </section>

        <!-- 3. 카운터 테이블 & 조제 접시 영역 -->
        <section class="wood-counter px-4 py-3.5 sm:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 relative z-10">
            
            <!-- 왼쪽: 카운터 장식 화분 & 안내 -->
            <div class="hidden md:flex items-center gap-3">
                <!-- 미니 화분 SVG -->
                <svg width="56" height="64" viewBox="0 0 60 68">
                    <path d="M18 42 L42 42 L38 62 L22 62 Z" fill="#e07a5f" stroke="#593a27" stroke-width="2.5"/>
                    <rect x="15" y="37" width="30" height="6" rx="2" fill="#e88d72" stroke="#593a27" stroke-width="2.5"/>
                    <path d="M30 37 C30 22, 16 20, 18 10 C26 12, 30 24, 30 37 Z" fill="#81b29a" stroke="#593a27" stroke-width="2"/>
                    <path d="M30 37 C30 20, 44 18, 42 8 C34 10, 30 22, 30 37 Z" fill="#6a9c83" stroke="#593a27" stroke-width="2"/>
                </svg>
                <div class="bg-[#fff6e8]/90 px-3 py-2 rounded-xl border-2 border-[#593a27] text-xs leading-relaxed">
                    <p class="font-jua text-sm text-[#593a27]">💡 조제 방법</p>
                    <p>아래 약통에서 <b>2가지 약</b>을 눌러</p>
                    <p>접시에 담은 뒤 <b>처방하기</b>를 누르세요!</p>
                </div>
            </div>

            <!-- 중앙: 약 조제 접시 (선택된 약 2개가 올라가는 공간) -->
            <div class="flex flex-col items-center">
                <span class="text-xs font-jua text-[#fff6e8] bg-[#593a27]/80 px-3 py-0.5 rounded-full mb-1.5">
                    처방 접시 (<span id="selected-count">0</span> / 2)
                </span>
                <div id="medicine-plate" class="wooden-dish w-56 h-24 sm:w-64 sm:h-28 rounded-full flex items-center justify-center gap-4 px-4 relative">
                    <!-- 슬롯 1 -->
                    <div id="plate-slot-0" class="w-16 h-16 sm:w-20 sm:h-20 rounded-full border-2 border-dashed border-[#8c583a]/60 bg-[#fff6e8]/40 flex flex-col items-center justify-center transition">
                        <span class="text-xs text-[#8c583a]/70 font-jua">약 1</span>
                    </div>
                    <!-- 슬롯 2 -->
                    <div id="plate-slot-1" class="w-16 h-16 sm:w-20 sm:h-20 rounded-full border-2 border-dashed border-[#8c583a]/60 bg-[#fff6e8]/40 flex flex-col items-center justify-center transition">
                        <span class="text-xs text-[#8c583a]/70 font-jua">약 2</span>
                    </div>
                </div>
            </div>

            <!-- 오른쪽: 비우기 & 처방하기 버튼 -->
            <div class="flex sm:flex-col gap-2.5 w-full sm:w-auto justify-center">
                <button id="give-btn" onclick="submitPrescription()" disabled class="flex-1 sm:flex-initial bg-[#7eb88a] disabled:bg-[#b8b0a4] hover:bg-[#6ca878] active:translate-y-0.5 text-white font-jua text-base sm:text-lg px-5 py-2.5 rounded-xl border-3 border-[#593a27] shadow-[0_4px_0_#593a27] disabled:shadow-none transition cursor-pointer disabled:cursor-not-allowed flex items-center justify-center gap-1.5">
                    <span>💊 처방하기</span>
                </button>
                <button id="clear-btn" onclick="clearPlate()" class="flex-1 sm:flex-initial bg-[#f4a261] hover:bg-[#e8914d] active:translate-y-0.5 text-[#3a2618] font-jua text-sm sm:text-base px-4 py-2 rounded-xl border-3 border-[#593a27] shadow-[0_3px_0_#593a27] transition cursor-pointer flex items-center justify-center gap-1">
                    <span>🔄 다시 담기</span>
                </button>
            </div>
        </section>

        <!-- 4. 하단 약 보관함 트레이 (레퍼런스 1번 이미지: 칸칸이 나뉜 나무 상자 속 재료들 스타일) -->
        <section class="wood-tray-area p-4 sm:p-6">
            <div class="flex items-center justify-between mb-3">
                <h2 class="font-jua text-base sm:text-lg text-[#fff6e8] drop-shadow-[0_2px_0_#593a27] flex items-center gap-2">
                    <span>🧰 조제 약 보관함 (클릭해서 접시에 담기)</span>
                </h2>
                <span class="text-xs text-[#fff6e8] bg-[#593a27]/70 px-2.5 py-1 rounded-lg">
                    순서는 상관없어요!
                </span>
            </div>

            <!-- 5가지 약 (ㄱ, ㄴ, ㄷ, ㄹ, ㅁ) 그리드 -->
            <div id="medicine-trays" class="grid grid-cols-5 gap-2 sm:gap-4">
                <!-- 자바스크립트에서 ㄱ, ㄴ, ㄷ, ㄹ, ㅁ 약통이 렌더링됩니다 -->
            </div>
        </section>

        <!-- 5. 처방전 도감 모달 (언제든 규칙을 확인할 수 있는 팝업) -->
        <div id="recipe-modal" class="hidden fixed inset-0 z-50 bg-black/45 flex items-center justify-center p-4">
            <div class="bg-[#fff9f0] hand-drawn-box w-full max-w-md p-5 sm:p-6 relative animate-pop">
                <div class="flex items-center justify-between border-b-2 border-dashed border-[#c4a484] pb-3 mb-4">
                    <h3 class="font-jua text-2xl text-[#593a27] flex items-center gap-2">
                        📖 동네 약국 처방 안내서
                    </h3>
                    <button onclick="toggleRecipeModal(false)" class="bg-[#e88d72] text-white font-jua w-8 h-8 rounded-full border-2 border-[#593a27] flex items-center justify-center cursor-pointer hover:bg-[#d97a5f]">
                        ✕
                    </button>
                </div>

                <div class="space-y-3">
                    <!-- 사용자 1 규칙 -->
                    <div class="bg-[#fff2e2] p-3 rounded-xl border-2 border-[#593a27] flex items-center justify-between">
                        <div class="flex items-center gap-2.5">
                            <span class="font-jua bg-[#f2b84b] text-[#4a3525] px-2.5 py-1 rounded-lg border border-[#593a27] text-sm">사용자 1</span>
                            <div>
                                <p class="font-jua text-base text-[#4a3525]">배가 아플 때</p>
                                <p class="text-xs text-[#7a5c43]">속을 달래주는 조합</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-1.5 font-jua text-lg">
                            <span class="bg-white px-3 py-1 rounded-lg border-2 border-[#593a27] text-[#d96b43]">ㄱ</span>
                            <span>+</span>
                            <span class="bg-white px-3 py-1 rounded-lg border-2 border-[#593a27] text-[#3b82f6]">ㄴ</span>
                        </div>
                    </div>

                    <!-- 사용자 2 규칙 -->
                    <div class="bg-[#fff2e2] p-3 rounded-xl border-2 border-[#593a27] flex items-center justify-between">
                        <div class="flex items-center gap-2.5">
                            <span class="font-jua bg-[#a8d5ba] text-[#4a3525] px-2.5 py-1 rounded-lg border border-[#593a27] text-sm">사용자 2</span>
                            <div>
                                <p class="font-jua text-base text-[#4a3525]">머리가 아플 때</p>
                                <p class="text-xs text-[#7a5c43]">지끈거림을 잡는 조합</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-1.5 font-jua text-lg">
                            <span class="bg-white px-3 py-1 rounded-lg border-2 border-[#593a27] text-[#10b981]">ㄷ</span>
                            <span>+</span>
                            <span class="bg-white px-3 py-1 rounded-lg border-2 border-[#593a27] text-[#8b5cf6]">ㄹ</span>
                        </div>
                    </div>

                    <!-- 사용자 3 규칙 -->
                    <div class="bg-[#fff2e2] p-3 rounded-xl border-2 border-[#593a27] flex items-center justify-between">
                        <div class="flex items-center gap-2.5">
                            <span class="font-jua bg-[#f4a261] text-[#4a3525] px-2.5 py-1 rounded-lg border border-[#593a27] text-sm">사용자 3</span>
                            <div>
                                <p class="font-jua text-base text-[#4a3525]">가슴이 아플 때</p>
                                <p class="text-xs text-[#7a5c43]">답답함을 풀어주는 조합</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-1.5 font-jua text-lg">
                            <span class="bg-white px-3 py-1 rounded-lg border-2 border-[#593a27] text-[#3b82f6]">ㄴ</span>
                            <span>+</span>
                            <span class="bg-white px-3 py-1 rounded-lg border-2 border-[#593a27] text-[#ec4899]">ㅁ</span>
                        </div>
                    </div>
                </div>

                <button onclick="toggleRecipeModal(false)" class="mt-5 w-full bg-[#7eb88a] hover:bg-[#6ca878] text-white font-jua text-lg py-2.5 rounded-xl border-3 border-[#593a27] shadow-[0_3px_0_#593a27] cursor-pointer">
                    확인했어요!
                </button>
            </div>
        </div>

        <!-- 6. 최종 결과 화면 (10명 완료 후 표시) -->
        <div id="result-modal" class="hidden fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
            <div class="bg-[#fff9f0] hand-drawn-box w-full max-w-md p-6 text-center animate-pop">
                <div id="result-badge-icon" class="text-6xl mb-2">🏆</div>
                <h2 class="font-jua text-3xl text-[#593a27] mb-1">오늘의 약국 영업 종료!</h2>
                <p id="result-subtitle" class="text-sm text-[#7a5c43] mb-5">총 10명의 환자분을 모두 진료했습니다.</p>

                <div class="bg-[#fff2e2] hand-drawn-sm p-4 mb-5">
                    <p class="text-sm text-[#6b4f3a] mb-1">정확하게 처방한 환자 수</p>
                    <p class="font-jua text-4xl text-[#d96b43]">
                        <span id="final-score">0</span> <span class="text-2xl text-[#593a27]">/ 10명</span>
                    </p>
                    <p id="result-comment" class="mt-2 font-jua text-base text-[#4a3525]">
                        동네 최고의 명의 약사님이시네요!
                    </p>
                </div>

                <!-- 환자별 기록 요약 배지 -->
                <div id="history-summary" class="flex flex-wrap justify-center gap-1.5 mb-6">
                    <!-- 1~10번 O/X 결과가 표시됩니다 -->
                </div>

                <button onclick="startNewGame()" class="w-full bg-[#e88d72] hover:bg-[#db7c60] active:translate-y-0.5 text-white font-jua text-xl py-3 rounded-xl border-3 border-[#593a27] shadow-[0_4px_0_#593a27] cursor-pointer transition">
                    🔄 다시 시작하기 (새로운 10명)
                </button>
            </div>
        </div>

    </div>

    <script>
        // ==========================================
        // 1. 게임 데이터 정의 (환자 유형 및 5가지 약)
        // ==========================================

        // 5가지 약 (ㄱ, ㄴ, ㄷ, ㄹ, ㅁ) 데이터 및 커스텀 손그림풍 SVG 아이콘
        const MEDICINES = {
            'ㄱ': {
                id: 'ㄱ',
                name: 'ㄱ 약',
                desc: '따뜻한 알약',
                color: '#f97316',
                svg: `
                    <svg viewBox="0 0 64 64" class="w-11 h-11 sm:w-14 sm:h-14 drop-shadow-sm">
                        <g transform="rotate(-30 32 32)">
                            <rect x="12" y="20" width="40" height="24" rx="12" fill="#ff9e6d" stroke="#593a27" stroke-width="3.5"/>
                            <path d="M32 20 L40 20 A12 12 0 0 1 40 44 L32 44 Z" fill="#fff3d6" stroke="#593a27" stroke-width="3.5"/>
                            <ellipse cx="22" cy="27" rx="4" ry="2" fill="#ffffff" opacity="0.7"/>
                        </g>
                    </svg>
                `
            },
            'ㄴ': {
                id: 'ㄴ',
                name: 'ㄴ 약',
                desc: '파란 물약병',
                color: '#3b82f6',
                svg: `
                    <svg viewBox="0 0 64 64" class="w-11 h-11 sm:w-14 sm:h-14 drop-shadow-sm">
                        <rect x="25" y="10" width="14" height="8" rx="2" fill="#d99b66" stroke="#593a27" stroke-width="3"/>
                        <path d="M22 18 L42 18 L46 28 L46 50 A6 6 0 0 1 40 56 L24 56 A6 6 0 0 1 18 50 L18 28 Z" fill="#93c5fd" stroke="#593a27" stroke-width="3.5"/>
                        <path d="M19 36 L45 36 L45 50 A5 5 0 0 1 40 55 L24 55 A5 5 0 0 1 19 50 Z" fill="#60a5fa"/>
                        <rect x="24" y="32" width="16" height="12" rx="3" fill="#fffdf7" stroke="#593a27" stroke-width="2"/>
                        <path d="M32 35 V41 M29 38 H35" stroke="#e11d48" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                `
            },
            'ㄷ': {
                id: 'ㄷ',
                name: 'ㄷ 약',
                desc: '초록 약초잎',
                color: '#10b981',
                svg: `
                    <svg viewBox="0 0 64 64" class="w-11 h-11 sm:w-14 sm:h-14 drop-shadow-sm">
                        <path d="M16 48 C14 26, 32 14, 50 14 C50 32, 38 50, 16 48 Z" fill="#6ee7b7" stroke="#593a27" stroke-width="3.5" stroke-linejoin="round"/>
                        <path d="M16 48 C26 38, 36 28, 48 16" fill="none" stroke="#593a27" stroke-width="3" stroke-linecap="round"/>
                        <path d="M28 36 L24 28 M36 28 L42 32" stroke="#593a27" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                `
            },
            'ㄹ': {
                id: 'ㄹ',
                name: 'ㄹ 약',
                desc: '보라 정제약',
                color: '#8b5cf6',
                svg: `
                    <svg viewBox="0 0 64 64" class="w-11 h-11 sm:w-14 sm:h-14 drop-shadow-sm">
                        <circle cx="26" cy="36" r="14" fill="#c4b5fd" stroke="#593a27" stroke-width="3.5"/>
                        <line x1="17" y1="27" x2="35" y2="45" stroke="#593a27" stroke-width="2.5"/>
                        <circle cx="42" cy="24" r="11" fill="#fde047" stroke="#593a27" stroke-width="3.5"/>
                        <line x1="35" y1="24" x2="49" y2="24" stroke="#593a27" stroke-width="2.5"/>
                    </svg>
                `
            },
            'ㅁ': {
                id: 'ㅁ',
                name: 'ㅁ 약',
                desc: '분홍 가루약',
                color: '#ec4899',
                svg: `
                    <svg viewBox="0 0 64 64" class="w-11 h-11 sm:w-14 sm:h-14 drop-shadow-sm">
                        <rect x="16" y="14" width="32" height="38" rx="6" fill="#fbcfe8" stroke="#593a27" stroke-width="3.5"/>
                        <path d="M16 23 L48 23" stroke="#593a27" stroke-width="2.5" stroke-dasharray="4 3"/>
                        <circle cx="32" cy="37" r="7" fill="#fffdf7" stroke="#593a27" stroke-width="2.5"/>
                        <path d="M29 37 L31 39 L35 35" fill="none" stroke="#ec4899" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                `
            }
        };

        // 3명의 환자 유형 정의 (정해진 증상 및 정답 약 조합)
        const PATIENT_TYPES = [
            {
                id: 'user1',
                name: '사용자 1',
                symptomLabel: '증상: 배 아픔 (복통)',
                dialogue: '"아이고... 배가 너무 콕콕 쑤시고 아파요!"',
                requiredMeds: ['ㄱ', 'ㄴ'],
                // 배를 움켜쥔 귀여운 손그림 스타일 환자 SVG
                svg: `
                    <svg viewBox="0 0 140 140" class="w-full h-full">
                        <!-- 몸통 (노란 스웨터) -->
                        <path d="M32 132 C32 98, 108 98, 108 132 Z" fill="#f6bd60" stroke="#593a27" stroke-width="3.5"/>
                        <!-- 목 -->
                        <rect x="61" y="82" width="18" height="18" rx="6" fill="#f9dcc4" stroke="#593a27" stroke-width="3"/>
                        <!-- 얼굴 -->
                        <circle cx="70" cy="56" r="32" fill="#f9dcc4" stroke="#593a27" stroke-width="3.5"/>
                        <!-- 머리카락 (갈색 단발) -->
                        <path d="M36 56 C34 24, 106 24, 104 56 C102 40, 88 34, 70 36 C52 34, 38 40, 36 56 Z" fill="#6f4e37" stroke="#593a27" stroke-width="3.5"/>
                        <!-- 아픈 눈썹 & 찡그린 눈 -->
                        <path d="M50 47 L60 51 M90 47 L80 51" stroke="#593a27" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M51 57 L59 54 M51 54 L59 57" stroke="#593a27" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M81 57 L89 54 M81 54 L89 57" stroke="#593a27" stroke-width="2.5" stroke-linecap="round"/>
                        <!-- 볼 홍조 & 식은땀 -->
                        <ellipse cx="48" cy="64" rx="5" ry="3" fill="#f28482" opacity="0.7"/>
                        <ellipse cx="92" cy="64" rx="5" ry="3" fill="#f28482" opacity="0.7"/>
                        <path d="M98 38 C101 43, 101 47, 98 47 C95 47, 95 43, 98 38 Z" fill="#93c5fd" stroke="#593a27" stroke-width="1.5"/>
                        <!-- 아픈 입 모양 -->
                        <path d="M62 72 Q70 66 78 72" fill="none" stroke="#593a27" stroke-width="3" stroke-linecap="round"/>
                        <!-- 배를 감싼 두 손 -->
                        <ellipse cx="58" cy="118" rx="11" ry="8" fill="#f9dcc4" stroke="#593a27" stroke-width="3"/>
                        <ellipse cx="82" cy="118" rx="11" ry="8" fill="#f9dcc4" stroke="#593a27" stroke-width="3"/>
                    </svg>
                `
            },
            {
                id: 'user2',
                name: '사용자 2',
                symptomLabel: '증상: 머리 아픔 (두통)',
                dialogue: '"으으... 머리가 지끈지끈 울리고 어지러워요!"',
                requiredMeds: ['ㄷ', 'ㄹ'],
                // 머리를 짚고 있는 귀여운 손그림 스타일 환자 SVG
                svg: `
                    <svg viewBox="0 0 140 140" class="w-full h-full">
                        <!-- 몸통 (민트색 가디건) -->
                        <path d="M30 132 C30 96, 110 96, 110 132 Z" fill="#84a59d" stroke="#593a27" stroke-width="3.5"/>
                        <path d="M70 100 L70 132" stroke="#593a27" stroke-width="3"/>
                        <!-- 목 -->
                        <rect x="61" y="82" width="18" height="18" rx="6" fill="#f8edeb" stroke="#593a27" stroke-width="3"/>
                        <!-- 얼굴 -->
                        <circle cx="70" cy="56" r="32" fill="#f8edeb" stroke="#593a27" stroke-width="3.5"/>
                        <!-- 머리카락 (곱슬 펌 스타일) -->
                        <path d="M36 52 C32 22, 108 22, 104 52 C96 34, 44 34, 36 52 Z" fill="#9c6644" stroke="#593a27" stroke-width="3.5"/>
                        <!-- 어지러운 눈 & 찡그린 표정 -->
                        <circle cx="55" cy="56" r="4" fill="#593a27"/>
                        <circle cx="85" cy="56" r="4" fill="#593a27"/>
                        <path d="M49 48 L61 51 M91 48 L79 51" stroke="#593a27" stroke-width="2.5" stroke-linecap="round"/>
                        <!-- 물결 입 -->
                        <path d="M60 72 Q65 68 70 72 Q75 76 80 72" fill="none" stroke="#593a27" stroke-width="2.8" stroke-linecap="round"/>
                        <!-- 이마를 짚은 손 & 반짝 통증 표시 -->
                        <ellipse cx="95" cy="44" rx="10" ry="8" transform="rotate(-20 95 44)" fill="#f8edeb" stroke="#593a27" stroke-width="3"/>
                        <path d="M26 30 L34 34 M24 40 L33 40 M30 22 L36 29" stroke="#e88d72" stroke-width="3" stroke-linecap="round"/>
                    </svg>
                `
            },
            {
                id: 'user3',
                name: '사용자 3',
                symptomLabel: '증상: 가슴 아픔 (흉통)',
                dialogue: '"콜록... 가슴이 답답하고 뻐근하게 아파요!"',
                requiredMeds: ['ㄴ', 'ㅁ'],
                // 가슴에 손을 얹은 귀여운 손그림 스타일 환자 SVG
                svg: `
                    <svg viewBox="0 0 140 140" class="w-full h-full">
                        <!-- 몸통 (살구색 니트) -->
                        <path d="M30 132 C30 96, 110 96, 110 132 Z" fill="#f28482" stroke="#593a27" stroke-width="3.5"/>
                        <!-- 목 -->
                        <rect x="61" y="82" width="18" height="18" rx="6" fill="#fae1dd" stroke="#593a27" stroke-width="3"/>
                        <!-- 얼굴 -->
                        <circle cx="70" cy="56" r="32" fill="#fae1dd" stroke="#593a27" stroke-width="3.5"/>
                        <!-- 머리카락 (단정한 짙은 갈색 머리) -->
                        <path d="M37 54 C37 22, 103 22, 103 54 L98 44 L70 38 L42 44 Z" fill="#4a3525" stroke="#593a27" stroke-width="3.5"/>
                        <!-- 동그란 안경 -->
                        <circle cx="55" cy="56" r="9" fill="rgba(255,255,255,0.4)" stroke="#593a27" stroke-width="2.5"/>
                        <circle cx="85" cy="56" r="9" fill="rgba(255,255,255,0.4)" stroke="#593a27" stroke-width="2.5"/>
                        <line x1="64" y1="56" x2="76" y2="56" stroke="#593a27" stroke-width="2.5"/>
                        <!-- 눈과 입 -->
                        <path d="M51 56 Q55 52 59 56" fill="none" stroke="#593a27" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M81 56 Q85 52 89 56" fill="none" stroke="#593a27" stroke-width="2.5" stroke-linecap="round"/>
                        <ellipse cx="70" cy="72" rx="5" ry="4" fill="#e07a5f" stroke="#593a27" stroke-width="2"/>
                        <!-- 가슴에 얹은 손 -->
                        <ellipse cx="70" cy="114" rx="13" ry="9" fill="#fae1dd" stroke="#593a27" stroke-width="3"/>
                    </svg>
                `
            }
        ];

        // ==========================================
        // 2. 게임 상태 변수
        // ==========================================
        const TOTAL_PATIENTS = 10;
        let patientQueue = [];      // 랜덤으로 뽑힌 10명의 환자 리스트
        let currentIndex = 0;       // 현재 환자 번호 (0 ~ 9)
        let selectedMeds = [];      // 현재 접시에 담긴 약 목록 (최대 2개)
        let score = 0;              // 정답 맞힌 횟수
        let historyLog = [];        // 각 환자별 성공/실패 기록
        let isProcessing = false;   // 결과 애니메이션 중 중복 클릭 방지
        let showMedicineGuide = true; // 현재 환자의 알맞은 약 자동 표시 여부

        // ==========================================
        // 3. 효과음 (Tone.js 신디사이저 - 외부 파일 없음)
        // ==========================================
        let synth = null;

        function playSound(type) {
            try {
                if (!synth) {
                    synth = new Tone.PolySynth(Tone.Synth).toDestination();
                    synth.volume.value = -8;
                }
                if (Tone.context.state !== 'running') {
                    Tone.start();
                }

                const now = Tone.now();
                if (type === 'pick') {
                    synth.triggerAttackRelease('C5', '16n', now);
                } else if (type === 'clear') {
                    synth.triggerAttackRelease('A4', '16n', now);
                } else if (type === 'success') {
                    synth.triggerAttackRelease(['C5', 'E5', 'G5'], '8n', now);
                    synth.triggerAttackRelease(['C6'], '4n', now + 0.15);
                } else if (type === 'fail') {
                    synth.triggerAttackRelease(['E4', 'Bb3'], '4n', now);
                }
            } catch (e) {
                // 오디오 컨텍스트 제한 환경에서도 게임 진행에 영향 없도록 예외 처리
            }
        }

        // ==========================================
        // 4. 게임 초기화 및 화면 렌더링
        // ==========================================

        // 새 게임 시작: 사용자 1, 2, 3 중에서 랜덤으로 10명 추출
        function startNewGame() {
            patientQueue = [];
            for (let i = 0; i < TOTAL_PATIENTS; i++) {
                const randomIdx = Math.floor(Math.random() * PATIENT_TYPES.length);
                patientQueue.push(PATIENT_TYPES[randomIdx]);
            }

            currentIndex = 0;
            selectedMeds = [];
            score = 0;
            historyLog = [];
            isProcessing = false;

            document.getElementById('result-modal').classList.add('hidden');
            document.getElementById('feedback-banner').classList.add('hidden');

            loadCurrentPatient();
            renderMedicineTrays();
            updatePlateUI();
            updateHeaderUI();
        }

        // 알맞은 약 자동 표시 ON/OFF 전환
        function toggleMedicineGuide() {
            showMedicineGuide = !showMedicineGuide;
            const btn = document.getElementById('guide-toggle-btn');
            if (showMedicineGuide) {
                btn.textContent = '💡 약 표시: ON';
                btn.classList.remove('bg-[#e5e7eb]', 'text-[#4b5563]');
                btn.classList.add('bg-[#ffe49e]', 'text-[#3a2618]');
            } else {
                btn.textContent = '🙈 약 표시: OFF';
                btn.classList.remove('bg-[#ffe49e]', 'text-[#3a2618]');
                btn.classList.add('bg-[#e5e7eb]', 'text-[#4b5563]');
            }
            updateRequiredMedsBanner();
            renderMedicineTrays();
        }

        // 하단 5개 약 보관함(ㄱ, ㄴ, ㄷ, ㄹ, ㅁ) 생성
        function renderMedicineTrays() {
            const container = document.getElementById('medicine-trays');
            container.innerHTML = '';

            const currentPatient = patientQueue[currentIndex];
            const recommendedMeds = currentPatient ? currentPatient.requiredMeds : [];

            Object.values(MEDICINES).forEach((med) => {
                const isSelected = selectedMeds.includes(med.id);
                const isRecommended = showMedicineGuide && recommendedMeds.includes(med.id);

                const btn = document.createElement('button');
                btn.type = 'button';
                btn.id = `med-btn-${med.id}`;
                btn.onclick = () => selectMedicine(med.id);
                btn.className = `med-compartment p-2 sm:p-3 flex flex-col items-center justify-between cursor-pointer relative ${isSelected ? 'selected' : ''} ${isRecommended ? 'recommended' : ''}`;

                const recommendTag = isRecommended
                    ? `<span class="absolute -top-2.5 right-1 bg-[#f59e0b] text-white font-jua text-[10px] sm:text-xs px-2 py-0.5 rounded-full border-2 border-[#593a27] shadow-sm">필요!</span>`
                    : '';

                btn.innerHTML = `
                    ${recommendTag}
                    <span class="bg-[#593a27] text-[#fff6e8] font-jua text-sm sm:text-base px-2.5 py-0.5 rounded-full mb-1">
                        ${med.id}
                    </span>
                    <div class="my-0.5 flex items-center justify-center">
                        ${med.svg}
                    </div>
                    <span class="text-[11px] sm:text-xs font-bold text-[#6b4f3a] mt-1">
                        ${med.desc}
                    </span>
                `;
                container.appendChild(btn);
            });
        }

        // 현재 환자 말풍선 안의 '필요한 약' 배지 업데이트
        function updateRequiredMedsBanner() {
            const patient = patientQueue[currentIndex];
            const rxBox = document.getElementById('auto-rx-box');
            const badgesContainer = document.getElementById('required-meds-badges');

            if (!showMedicineGuide) {
                rxBox.classList.add('hidden');
                return;
            }

            rxBox.classList.remove('hidden');
            const [med1Id, med2Id] = patient.requiredMeds;
            const med1 = MEDICINES[med1Id];
            const med2 = MEDICINES[med2Id];

            badgesContainer.innerHTML = `
                <span class="bg-white border-2 border-[#593a27] rounded-lg px-2.5 py-0.5 shadow-xs flex items-center gap-1" style="color: ${med1.color}">
                    <span>${med1.id}</span>
                    <span class="text-xs text-[#6b4f3a]">(${med1.desc})</span>
                </span>
                <span class="text-[#593a27]">+</span>
                <span class="bg-white border-2 border-[#593a27] rounded-lg px-2.5 py-0.5 shadow-xs flex items-center gap-1" style="color: ${med2.color}">
                    <span>${med2.id}</span>
                    <span class="text-xs text-[#6b4f3a]">(${med2.desc})</span>
                </span>
            `;
        }

        // 현재 순서의 환자 화면에 표시
        function loadCurrentPatient() {
            const patient = patientQueue[currentIndex];
            const avatarEl = document.getElementById('patient-avatar');
            const containerEl = document.getElementById('patient-container');
            const speechBox = document.getElementById('speech-box');

            // 등장 애니메이션 재실행
            containerEl.classList.remove('animate-enter');
            speechBox.classList.remove('animate-pop');
            void containerEl.offsetWidth; // 리플로우 트리거
            containerEl.classList.add('animate-enter');
            speechBox.classList.add('animate-pop');

            avatarEl.innerHTML = patient.svg;
            document.getElementById('patient-name-tag').textContent = patient.name;
            document.getElementById('symptom-badge').textContent = patient.symptomLabel;
            document.getElementById('patient-dialogue').textContent = patient.dialogue;
            updateRequiredMedsBanner();
        }

        // 상단 진행도 및 점수 UI 업데이트
        function updateHeaderUI() {
            const displayNum = Math.min(currentIndex + 1, TOTAL_PATIENTS);
            document.getElementById('progress-badge').textContent = `환자 ${displayNum} / ${TOTAL_PATIENTS}`;
            document.getElementById('score-display').textContent = score;
        }

        // ==========================================
        // 5. 약 선택, 비우기 및 처방 판정 로직
        // ==========================================

        // 약통에서 약을 클릭했을 때
        function selectMedicine(medId) {
            if (isProcessing) return;

            // 이미 접시에 담긴 약을 다시 누르면 접시에서 빼기 (편의 기능)
            if (selectedMeds.includes(medId)) {
                selectedMeds = selectedMeds.filter(id => id !== medId);
                playSound('clear');
                updatePlateUI();
                renderMedicineTrays();
                return;
            }

            // 최대 2개까지만 접시에 담기
            if (selectedMeds.length >= 2) {
                const plate = document.getElementById('medicine-plate');
                plate.classList.remove('animate-shake');
                void plate.offsetWidth;
                plate.classList.add('animate-shake');
                return;
            }

            selectedMeds.push(medId);
            playSound('pick');
            updatePlateUI();
            renderMedicineTrays();
        }

        // 접시 비우기 버튼
        function clearPlate() {
            if (isProcessing || selectedMeds.length === 0) return;
            selectedMeds = [];
            playSound('clear');
            updatePlateUI();
            renderMedicineTrays();
        }

        // 조제 접시 슬롯 및 처방 버튼 활성화 상태 갱신
        function updatePlateUI() {
            document.getElementById('selected-count').textContent = selectedMeds.length;

            for (let i = 0; i < 2; i++) {
                const slot = document.getElementById(`plate-slot-${i}`);
                const medId = selectedMeds[i];

                if (medId && MEDICINES[medId]) {
                    const med = MEDICINES[medId];
                    slot.className = 'w-16 h-16 sm:w-20 sm:h-20 rounded-full border-3 border-[#593a27] bg-[#fffdf9] flex flex-col items-center justify-center shadow-sm animate-pop cursor-pointer';
                    slot.onclick = () => selectMedicine(medId); // 접시 위 약을 눌러도 제거 가능
                    slot.innerHTML = `
                        <div class="scale-75 sm:scale-90 -my-1">${med.svg}</div>
                        <span class="font-jua text-xs sm:text-sm text-[#593a27] leading-none">${med.id}</span>
                    `;
                } else {
                    slot.className = 'w-16 h-16 sm:w-20 sm:h-20 rounded-full border-2 border-dashed border-[#8c583a]/60 bg-[#fff6e8]/40 flex flex-col items-center justify-center transition';
                    slot.onclick = null;
                    slot.innerHTML = `<span class="text-xs text-[#8c583a]/70 font-jua">약 ${i + 1}</span>`;
                }
            }

            // 2개가 모두 담겼을 때만 '처방하기' 버튼 활성화
            const giveBtn = document.getElementById('give-btn');
            giveBtn.disabled = selectedMeds.length !== 2;
        }

        // 처방하기 버튼 클릭 시 정답 확인
        function submitPrescription() {
            if (isProcessing || selectedMeds.length !== 2) return;
            isProcessing = true;

            const currentPatient = patientQueue[currentIndex];
            const required = currentPatient.requiredMeds;

            // 순서와 무관하게 2개의 약이 정확히 일치하는지 판정
            const isCorrect = required.every(med => selectedMeds.includes(med)) &&
                              selectedMeds.every(med => required.includes(med));

            const feedbackBanner = document.getElementById('feedback-banner');
            const feedbackCard = document.getElementById('feedback-card');
            const feedbackEmoji = document.getElementById('feedback-emoji');
            const feedbackTitle = document.getElementById('feedback-title');
            const feedbackDesc = document.getElementById('feedback-desc');

            if (isCorrect) {
                score++;
                historyLog.push({ patient: currentPatient.name, correct: true });
                playSound('success');

                feedbackEmoji.textContent = '😊✨';
                feedbackTitle.textContent = '처방 성공!';
                feedbackTitle.className = 'font-jua text-2xl text-[#2e7d32] mb-1';
                feedbackDesc.textContent = `${currentPatient.name}님이 고마워하며 기운을 차렸어요!`;
                feedbackCard.className = 'bg-[#f1f8e9] hand-drawn-box px-7 py-5 text-center max-w-xs mx-4 animate-pop';
            } else {
                historyLog.push({ patient: currentPatient.name, correct: false });
                playSound('fail');

                feedbackEmoji.textContent = '💦😵';
                feedbackTitle.textContent = '처방이 달라요!';
                feedbackTitle.className = 'font-jua text-2xl text-[#c62828] mb-1';
                feedbackDesc.innerHTML = `${currentPatient.name}님에게는 <b>[${required[0]}, ${required[1]}]</b> 약이 필요했어요.`;
                feedbackCard.className = 'bg-[#ffebee] hand-drawn-box px-7 py-5 text-center max-w-xs mx-4 animate-shake';
            }

            updateHeaderUI();
            feedbackBanner.classList.remove('hidden');

            // 1.35초 후 다음 환자로 이동 또는 최종 결과 표시
            setTimeout(() => {
                feedbackBanner.classList.add('hidden');
                currentIndex++;

                if (currentIndex < TOTAL_PATIENTS) {
                    selectedMeds = [];
                    isProcessing = false;
                    updateHeaderUI();
                    updatePlateUI();
                    loadCurrentPatient();
                    renderMedicineTrays();
                } else {
                    showFinalResult();
                }
            }, 1350);
        }

        // 10명 완료 후 최종 결과 모달 표시
        function showFinalResult() {
            document.getElementById('final-score').textContent = score;

            const badgeIcon = document.getElementById('result-badge-icon');
            const comment = document.getElementById('result-comment');

            if (score === 10) {
                badgeIcon.textContent = '👑🏆';
                comment.textContent = '완벽해요! 10명 모두 정확하게 치료한 전설의 약사님!';
            } else if (score >= 7) {
                badgeIcon.textContent = '🌟😊';
                comment.textContent = '훌륭해요! 동네 주민들이 믿고 찾는 다정한 약사님!';
            } else {
                badgeIcon.textContent = '🌿📖';
                comment.textContent = '수고하셨어요! 처방전을 참고해서 다시 도전해 볼까요?';
            }

            // 1~10번 환자별 결과 요약 배지 생성
            const historyContainer = document.getElementById('history-summary');
            historyContainer.innerHTML = '';
            historyLog.forEach((item, idx) => {
                const badge = document.createElement('span');
                badge.className = item.correct
                    ? 'bg-[#d8f3dc] text-[#1b4332] border-2 border-[#593a27] rounded-lg px-2 py-1 text-xs font-jua'
                    : 'bg-[#ffe5ec] text-[#9b2226] border-2 border-[#593a27] rounded-lg px-2 py-1 text-xs font-jua';
                badge.textContent = `${idx + 1}번 ${item.correct ? '⭕' : '❌'}`;
                historyContainer.appendChild(badge);
            });

            document.getElementById('result-modal').classList.remove('hidden');
        }

        // 처방전 도감 모달 열기/닫기
        function toggleRecipeModal(show) {
            const modal = document.getElementById('recipe-modal');
            if (show) {
                modal.classList.remove('hidden');
            } else {
                modal.classList.add('hidden');
            }
        }

        // 페이지 로드 시 자동 시작
        window.onload = function() {
            startNewGame();
        };
    </script>
</body>
</html>
