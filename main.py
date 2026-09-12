import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ZeroSub", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ZeroSub - 스마트 구독 관리</title>

  <!-- 구글 웹폰트 연동 -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=GangwonEduModu:wght@400;700&family=Hi+Melody&family=Nanum+Myeongjo:wght@400;700&family=Poor+Story&family=Gaegu:wght@400;700&family=Cute+Font&display=swap" rel="stylesheet">
  
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    :root {
      --bg-color: #f0fdf4;
      --card-bg: #ffffff;
      --primary-color: #38bdf8;
      --accent-color: #4ade80;
      --text-color: #1e293b;
      --border-color: #334155;
      --font-family: 'GangwonEduModu', sans-serif;
      --font-scale: 1;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: var(--font-family); }
    html { font-size: calc(16px * var(--font-scale)); }
    body { background-color: var(--bg-color); color: var(--text-color); display: flex; justify-content: center; min-height: 100vh; }
    
    .app-container { 
      width: 100%; max-width: 430px; background: #ffffff; min-height: 100vh; 
      display: flex; flex-direction: column; position: relative; 
      border: 2.5px solid var(--border-color); border-radius: 24px; overflow: hidden;
      box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    
    .header { 
      height: 65px; display: flex; justify-content: space-between; align-items: center; 
      padding: 0 18px; border-bottom: 2px dashed #cbd5e1; background: #ffffff; 
      position: sticky; top: 0; z-index: 100; 
    }
    
    /* 마스코트 로고 스타일 */
    .brand-logo { display: flex; align-items: center; gap: 8px; cursor: pointer; }
    .mascot-icon { width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; }
    .logo-text { font-size: 1.4rem; font-weight: 700; color: #0284c7; letter-spacing: -0.5px; }

    .header-right { display: flex; align-items: center; gap: 12px; }
    .icon-btn { background: none; border: none; font-size: 1.3rem; cursor: pointer; position: relative; }
    .notif-badge { position: absolute; top: 0; right: 0; width: 8px; height: 8px; background: #ef4444; border-radius: 50%; }

    .screen { display: none; padding: 18px; flex: 1; overflow-y: auto; padding-bottom: 85px; }
    .screen.active { display: block; }

    /* 이미지 스타일의 귀여운 요약 카드 */
    .summary-card { 
      background: #e0f2fe; border: 2px solid var(--border-color); border-radius: 20px; 
      padding: 18px; margin-bottom: 16px; position: relative; box-shadow: 3px 3px 0px var(--border-color);
    }
    .summary-title { font-size: 0.85rem; font-weight: 700; color: #0369a1; margin-bottom: 4px; }
    .summary-price { font-size: 1.7rem; font-weight: 700; color: #0c4a6e; }
    .alert-tag { 
      background: #ffffff; color: #e11d48; font-size: 0.78rem; font-weight: 700; 
      padding: 6px 12px; border-radius: 12px; border: 1.5px solid var(--border-color);
      display: inline-block; margin-top: 8px; box-shadow: 2px 2px 0px var(--border-color);
    }

    .mascot-speech {
      display: flex; align-items: center; gap: 10px; background: #f0fdf4; 
      border: 2px solid var(--border-color); border-radius: 16px; padding: 10px 14px; 
      margin-bottom: 16px; box-shadow: 2px 2px 0px var(--border-color);
    }
    .speech-bubble { font-size: 0.82rem; font-weight: 700; color: #15803d; }

    .chart-card { 
      background: #ffffff; border: 2px solid var(--border-color); border-radius: 20px; 
      padding: 16px; margin-bottom: 16px; text-align: center; box-shadow: 3px 3px 0px var(--border-color);
    }
    .chart-container { position: relative; width: 100%; max-width: 180px; margin: 0 auto; }

    .card-list { display: flex; flex-direction: column; gap: 14px; }
    
    /* 손그림 스타일 구독 카드 */
    .sub-card { 
      background: #ffffff; border-radius: 18px; padding: 16px; 
      border: 2px solid var(--border-color); cursor: pointer; 
      box-shadow: 3px 3px 0px var(--border-color); transition: transform 0.1s;
    }
    .sub-card:active { transform: translate(2px, 2px); box-shadow: 1px 1px 0px var(--border-color); }
    
    .card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .card-info { display: flex; gap: 10px; align-items: center; }
    .app-icon-img { width: 40px; height: 40px; border-radius: 12px; object-fit: cover; border: 1.5px solid var(--border-color); }
    
    .badge { font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 10px; border: 1.5px solid var(--border-color); }
    .badge.blue { background: #bae6fd; color: #0369a1; }
    .badge.red { background: #fecdd3; color: #be123c; }
    .badge.orange { background: #fde68a; color: #b45309; }

    .card-mid { margin-bottom: 10px; font-size: 0.8rem; }
    .usage-text { display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 6px; }
    .bar-bg { width: 100%; height: 10px; background: #f1f5f9; border-radius: 6px; border: 1.5px solid var(--border-color); overflow: hidden; }
    .bar-fill { height: 100%; background: #38bdf8; border-radius: 4px; }
    .bar-fill.red { background: #f43f5e; }
    .bar-fill.orange { background: #fbbf24; }

    .card-bottom { border-top: 1.5px dashed #cbd5e1; padding-top: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; font-weight: 700; }
    .link-btn { color: #0284c7; padding: 4px 8px; background: #e0f2fe; border-radius: 8px; border: 1px solid var(--border-color); }

    .custom-panel { background: #f8fafc; border: 2px solid var(--border-color); border-radius: 16px; padding: 14px; margin-bottom: 16px; display: flex; flex-direction: column; gap: 10px; font-size: 0.85rem; box-shadow: 2px 2px 0px var(--border-color); }
    .custom-row { display: flex; justify-content: space-between; align-items: center; }
    .custom-select { padding: 6px 10px; border-radius: 8px; border: 1.5px solid var(--border-color); font-size: 0.8rem; background: #ffffff; font-weight: 700; }

    /* 귀여운 핸드드롱 커스텀 하단 네비게이션 */
    .bottom-nav { 
      position: fixed; bottom: 0; width: 100%; max-width: 425px; height: 65px; 
      background: #ffffff; border-top: 2px solid var(--border-color); 
      display: flex; justify-content: space-around; align-items: center; z-index: 100; 
    }
    .nav-item { border: none; background: none; color: #64748b; font-size: 0.75rem; font-weight: 700; display: flex; flex-direction: column; align-items: center; gap: 2px; cursor: pointer; }
    .nav-item.active { color: #0284c7; }
    .nav-icon-svg { width: 24px; height: 24px; stroke: #64748b; fill: none; stroke-width: 2; }
    .nav-item.active .nav-icon-svg { stroke: #0284c7; fill: #e0f2fe; }

    /* SVG 캐릭터 코드 연동용 */
    .mascot-head { fill: #ffffff; stroke: var(--border-color); stroke-width: 2; }
    .clover-leaf { fill: #4ade80; stroke: var(--border-color); stroke-width: 1.5; }
  </style>
</head>
<body>

<div class="app-container">
  <header class="header">
    <div class="brand-logo" onclick="switchScreen('dashboard')">
      <!-- 네잎클로버 얹은 아기곰 '제로' 마스코트 SVG -->
      <div class="mascot-icon">
        <svg width="34" height="34" viewBox="0 0 100 100">
          <!-- 귀 -->
          <circle cx="28" cy="28" r="12" class="mascot-head" />
          <circle cx="72" cy="28" r="12" class="mascot-head" />
          <!-- 얼굴 -->
          <circle cx="50" cy="55" r="35" class="mascot-head" />
          <!-- 눈, 코, 입 -->
          <circle cx="38" cy="50" r="3" fill="#1e293b" />
          <circle cx="62" cy="50" r="3" fill="#1e293b" />
          <ellipse cx="50" cy="58" rx="4" ry="3" fill="#1e293b" />
          <path d="M 46 63 Q 50 67 54 63" stroke="#1e293b" stroke-width="2" fill="none" stroke-linecap="round"/>
          <!-- 볼터치 -->
          <circle cx="32" cy="56" r="4" fill="#fca5a5" opacity="0.6"/>
          <circle cx="68" cy="56" r="4" fill="#fca5a5" opacity="0.6"/>
          <!-- 머리 위 클로버 -->
          <path d="M 50 22 C 45 15, 38 22, 50 27 C 62 22, 55 15, 50 22 Z" class="clover-leaf" />
          <path d="M 50 22 C 43 27, 50 35, 50 27 C 50 35, 57 27, 50 22 Z" class="clover-leaf" />
          <line x1="50" y1="27" x2="50" y2="33" stroke="#1e293b" stroke-width="2"/>
        </svg>
      </div>
      <span class="logo-text">ZeroSub</span>
    </div>
    <div class="header-right">
      <button class="icon-btn" onclick="switchScreen('notif')">
        🔔<span class="notif-badge"></span>
      </button>
      <div style="width:32px; height:32px; border-radius:50%; border:2px solid var(--border-color); background:#bfdbfe; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.8rem; cursor:pointer;" onclick="switchScreen('settings')">나</div>
    </div>
  </header>

  <div id="screen-dashboard" class="screen active">
    <!-- 마스코트 말풍선 안내 -->
    <div class="mascot-speech">
      <svg width="32" height="32" viewBox="0 0 100 100">
        <circle cx="28" cy="28" r="12" class="mascot-head" />
        <circle cx="72" cy="28" r="12" class="mascot-head" />
        <circle cx="50" cy="55" r="35" class="mascot-head" />
        <circle cx="38" cy="50" r="3" fill="#1e293b" />
        <circle cx="62" cy="50" r="3" fill="#1e293b" />
        <ellipse cx="50" cy="58" rx="4" ry="3" fill="#1e293b" />
        <path d="M 46 63 Q 50 67 54 63" stroke="#1e293b" stroke-width="2" fill="none"/>
        <path d="M 50 22 C 45 15, 38 22, 50 27 C 62 22, 55 15, 50 22 Z" class="clover-leaf" />
      </svg>
      <div class="speech-bubble">안녕! 제로가 이번 달 낭비되는 구독을 찾아냈어 ☘️</div>
    </div>

    <div class="summary-card">
      <div class="summary-title">내가 결제하는 월 구독 금액</div>
      <div class="summary-price"><span id="total-price-text">79,300</span>원 <span style="font-size:0.85rem; opacity:0.7; font-weight:400;">(<span id="total-count-text">6</span>개)</span></div>
      <div class="alert-tag">⚠️ 유튜브, 스포티파이 중복 지출 주의!</div>
    </div>

    <div class="chart-card">
      <div style="font-size:0.85rem; font-weight:700; margin-bottom:10px; color:#0369a1;">📊 카테고리별 지출 리포트</div>
      <div class="chart-container">
        <canvas id="subChart"></canvas>
      </div>
    </div>

    <div class="card-list" id="main-sub-list"></div>
  </div>

  <div id="screen-notif" class="screen">
    <h3 style="margin-bottom:16px;">알림 센터 🍀</h3>
    <div style="background:#fff; border:2px solid var(--border-color); border-radius:14px; padding:12px; margin-bottom:10px; box-shadow:2px 2px 0px var(--border-color);">
      <div style="font-weight:700; font-size:0.85rem;">🚨 티빙 결제 3일 전 알림</div>
      <div style="font-size:0.75rem; opacity:0.8; margin-top:2px;">이번 달 시청 시간이 20분 뿐이에요. 해지하시겠어요?</div>
    </div>
    <div style="background:#fff; border:2px solid var(--border-color); border-radius:14px; padding:12px; box-shadow:2px 2px 0px var(--border-color);">
      <div style="font-weight:700; font-size:0.85rem;">👨‍👩‍👧 가족 중복 구독 발견!</div>
      <div style="font-size:0.75rem; opacity:0.8; margin-top:2px;">아빠 계정과 '유튜브'를 각각 결제 중입니다. 통합 시 절약 가능!</div>
    </div>
  </div>

  <div id="screen-detail" class="screen">
    <button onclick="switchScreen('dashboard')" style="border:none; background:none; font-weight:700; cursor:pointer; margin-bottom:12px;">← 뒤로가기</button>
    <div style="background:#e0f2fe; border:2px solid var(--border-color); padding:20px; border-radius:18px; text-align:center; margin-bottom:16px; box-shadow:3px 3px 0px var(--border-color);">
      <h2 id="det-title" style="color:#0c4a6e;">서비스 이름</h2>
      <p id="det-price" style="color:#0369a1; margin-top:4px; font-weight:700;">월 0원</p>
    </div>
    
    <h4 style="margin-bottom:8px;">이용 현황 분석</h4>
    <div style="background:#ffffff; border:2px solid var(--border-color); padding:16px; border-radius:16px; margin-bottom:16px; box-shadow:2px 2px 0px var(--border-color);">
      <div style="height: 130px; position: relative; margin-bottom: 10px;">
        <canvas id="detailCompareChart"></canvas>
      </div>
      <p style="font-size:0.85rem; border-top:1.5px dashed #cbd5e1; padding-top:8px;"><strong>진단 결과:</strong> <span id="det-status" style="color:#ef4444; font-weight:700;">-</span></p>
    </div>
    <a id="det-link" href="#" target="_blank" style="display:block; text-align:center; background:#f43f5e; color:white; padding:14px; border-radius:14px; border:2px solid var(--border-color); font-weight:700; text-decoration:none; box-shadow:3px 3px 0px var(--border-color);">해지 / 계정 설정 페이지로 이동 ↗</a>
  </div>

  <div id="screen-add" class="screen">
    <h3 style="margin-bottom: 16px;">새 구독 서비스 추가 ➕</h3>
    <form onsubmit="addSubscription(event)" style="display:flex; flex-direction:column; gap:12px;">
      <div>
        <label style="font-size:0.78rem; font-weight:700; margin-bottom:4px; display:block;">서비스 이름</label>
        <input type="text" id="add-name" placeholder="예: 왓챠, 디즈니플러스" required style="width:100%; padding:12px; border:2px solid var(--border-color); border-radius:12px; font-size:0.85rem;">
      </div>
      <div>
        <label style="font-size:0.78rem; font-weight:700; margin-bottom:4px; display:block;">결제 금액 (원)</label>
        <input type="number" id="add-price" placeholder="예: 7900" required style="width:100%; padding:12px; border:2px solid var(--border-color); border-radius:12px; font-size:0.85rem;">
      </div>
      <div style="display:flex; gap:10px;">
        <div style="flex:1;">
          <label style="font-size:0.78rem; font-weight:700; margin-bottom:4px; display:block;">결제 주기</label>
          <select id="add-cycle" style="width:100%; padding:12px; border:2px solid var(--border-color); border-radius:12px; font-size:0.85rem; background:#fff;">
            <option value="매월">매월</option>
            <option value="매년">매년</option>
          </select>
        </div>
        <div style="flex:1;">
          <label style="font-size:0.78rem; font-weight:700; margin-bottom:4px; display:block;">다음 결제일</label>
          <input type="date" id="add-date" required style="width:100%; padding:12px; border:2px solid var(--border-color); border-radius:12px; font-size:0.85rem; background:#fff;">
        </div>
      </div>
      <button type="submit" style="padding:14px; background:#38bdf8; color:white; border:2px solid var(--border-color); border-radius:12px; font-weight:700; margin-top:12px; cursor:pointer; font-size:0.95rem; box-shadow:3px 3px 0px var(--border-color);">구독 등록하기</button>
    </form>
  </div>

  <div id="screen-settings" class="screen">
    <h3 style="margin-bottom:16px;">내 계정 및 설정 ⚙️</h3>
    
    <div style="background:#fff; border:2px solid var(--border-color); border-radius:14px; padding:14px; margin-bottom:16px; box-shadow:2px 2px 0px var(--border-color);">
      <p style="font-weight:700;">홍길동 (gildong@example.com)</p>
      <p style="font-size:0.75rem; opacity:0.7; margin-top:2px;">ZeroSub 프리미엄 가계부 이용 중 🍀</p>
    </div>

    <h4 style="margin-bottom:8px;">✏️ 요청하신 폰트 설정</h4>
    <div class="custom-panel">
      <div class="custom-row">
        <span>글꼴 종류 선택:</span>
        <select class="custom-select" onchange="changeFont(this.value)">
          <option value="'GangwonEduModu', sans-serif">강원교육모두체 (기본)</option>
          <option value="'Poor Story', cursive">서툰이야기</option>
          <option value="'Hi Melody', cursive">하이멜로디</option>
          <option value="'Nanum Myeongjo', serif">나눔명조</option>
          <option value="'Gaegu', cursive">개구체 (추천 몽글폰트)</option>
          <option value="'Cute Font', cursive">큐트폰트 (추천 초코버니 느낌)</option>
        </select>
      </div>
      <div class="custom-row">
        <span>글꼴 크기 조절:</span>
        <select class="custom-select" onchange="changeFontSize(this.value)">
          <option value="1">보통 (기본)</option>
          <option value="0.88">작게</option>
          <option value="1.15">크게</option>
        </select>
      </div>
    </div>
  </div>

  <!-- 하단 손그림 네비게이션 아이콘 -->
  <nav class="bottom-nav">
    <button class="nav-item active" onclick="switchScreen('dashboard')">
      <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
      홈
    </button>
    <button class="nav-item" onclick="switchScreen('add')">
      <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M12 4v16m-8-8h16"/></svg>
      구독 추가
    </button>
    <button class="nav-item" onclick="switchScreen('notif')">
      <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
      알림
    </button>
    <button class="nav-item" onclick="switchScreen('settings')">
      <svg class="nav-icon-svg" viewBox="0 0 24 24"><path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
      설정
    </button>
  </nav>
</div>

<script>
  const domainMap = {
    '넷플릭스': 'netflix.com', '유튜브': 'youtube.com', '유튜브 프리미엄': 'youtube.com',
    '티빙': 'tving.com', '멜론': 'melon.com', '스포티파이': 'spotify.com', '배민클럽': 'baemin.com'
  };

  function getIconUrl(name) {
    const cleanName = name.replace(/\s+/g, '');
    let domain = 'google.com';
    for (let key in domainMap) {
      if (cleanName.includes(key.replace(/\s+/g, ''))) {
        domain = domainMap[key]; break;
      }
    }
    return `https://www.google.com/s2/favicons?domain=${domain}&sz=128`;
  }

  let subscriptions = [
    { title: '넷플릭스', price: 17000, category: '영상', cycle: '매월', useVal: 32.6, avgVal: 15.0, unit: '시간', status: '정상 이용 중', url: 'https://www.netflix.com/youraccount', badgeText: '알뜰 활용', badgeClass: 'blue', statusClass: 'good', usageText: '시청시간', usageDisp: '32시간 40분', dateText: '결제일: 10/15' },
    { title: '유튜브 프리미엄', price: 14900, category: '영상', cycle: '매월', useVal: 48.1, avgVal: 20.0, unit: '시간', status: '가족 중복 이용 중', url: 'https://www.youtube.com/paid_memberships', badgeText: '중복 주의', badgeClass: 'orange', statusClass: 'warning', usageText: '시청시간', usageDisp: '48시간 10분', dateText: '결제일: 10/02' },
    { title: '티빙', price: 13900, category: '영상', cycle: '매월', useVal: 0.3, avgVal: 12.0, unit: '시간', status: '해지 권장 (D-3)', url: 'https://www.tving.com/my/subscription', badgeText: '낭비 경고', badgeClass: 'red', statusClass: 'bad', usageText: '시청시간', usageDisp: '0시간 20분', dateText: '3일후 결제' },
    { title: '멜론', price: 10900, category: '음악', cycle: '매월', useVal: 12, avgVal: 250, unit: '회', status: '스포티파이와 중복', url: 'https://www.melon.com', badgeText: '방치 중', badgeClass: 'red', statusClass: 'bad', usageText: '재생 횟수', usageDisp: '12회', dateText: '결제일: 09/28' }
  ];

  let subChartInstance = null;
  let detailChartInstance = null;

  function updateChart() {
    const categories = { '영상': 0, '음악': 0, '기타': 0 };
    subscriptions.forEach(sub => {
      if (categories[sub.category] !== undefined) categories[sub.category] += sub.price;
      else categories['기타'] += sub.price;
    });

    const ctx = document.getElementById('subChart').getContext('2d');
    if (subChartInstance) subChartInstance.destroy();

    subChartInstance = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: Object.keys(categories),
        datasets: [{
          data: Object.values(categories),
          backgroundColor: ['#38bdf8', '#4ade80', '#fbbf24'],
          borderWidth: 2,
          borderColor: '#334155'
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } },
        cutout: '60%'
      }
    });
  }

  function renderSubscriptions() {
    const container = document.getElementById('main-sub-list');
    container.innerHTML = '';
    let totalPrice = 0;

    subscriptions.forEach((sub) => {
      totalPrice += sub.price;
      const iconUrl = getIconUrl(sub.title);
      const card = document.createElement('div');
      card.className = `sub-card`;
      card.onclick = () => openDetail(sub);
      
      const fillPct = Math.min(100, Math.round((sub.useVal / sub.avgVal) * 100));

      card.innerHTML = `
        <div class="card-top">
          <div class="card-info">
            <img class="app-icon-img" src="${iconUrl}" onerror="this.src='https://www.google.com/s2/favicons?domain=google.com&sz=128'">
            <div>
              <div style="font-weight:700;">${sub.title}</div>
              <div style="font-size:0.75rem; opacity:0.7;">${sub.cycle} ${sub.price.toLocaleString()}원</div>
            </div>
          </div>
          <span class="badge ${sub.badgeClass}">${sub.badgeText}</span>
        </div>
        <div class="card-mid">
          <div class="usage-text">
            <span>${sub.usageText}</span>
            <span>${sub.usageDisp}</span>
          </div>
          <div class="bar-bg"><div class="bar-fill ${sub.badgeClass === 'red' ? 'red' : (sub.badgeClass === 'orange' ? 'orange' : '')}" style="width: ${fillPct}%;"></div></div>
        </div>
        <div class="card-bottom">
          <span>${sub.dateText}</span>
          <span class="link-btn">자세히 →</span>
        </div>
      `;
      container.appendChild(card);
    });

    document.getElementById('total-price-text').innerText = totalPrice.toLocaleString();
    document.getElementById('total-count-text').innerText = subscriptions.length;
    updateChart();
  }

  function openDetail(sub) {
    document.getElementById('det-title').innerText = sub.title;
    document.getElementById('det-price').innerText = `${sub.cycle} ${sub.price.toLocaleString()}원`;
    document.getElementById('det-status').innerText = sub.status;
    document.getElementById('det-link').href = sub.url;

    const ctx = document.getElementById('detailCompareChart').getContext('2d');
    if (detailChartInstance) detailChartInstance.destroy();

    detailChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['내 사용량', '평균 기준'],
        datasets: [{
          data: [sub.useVal, sub.avgVal],
          backgroundColor: [sub.badgeClass === 'red' ? '#f43f5e' : '#38bdf8', '#cbd5e1'],
          borderWidth: 1.5,
          borderColor: '#334155',
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { beginAtZero: true }, y: { grid: { display: false } } }
      }
    });

    switchScreen('detail');
  }

  function addSubscription(e) {
    e.preventDefault();
    const name = document.getElementById('add-name').value.trim();
    const price = parseInt(document.getElementById('add-price').value.trim());
    const cycle = document.getElementById('add-cycle').value;
    const dateVal = document.getElementById('add-date').value;

    if(name && !isNaN(price)) {
      subscriptions.unshift({
        title: name, price: price, category: '기타', cycle: cycle,
        useVal: 50, avgVal: 50, unit: '%', status: '등록 완료', url: '#',
        badgeText: '신규', badgeClass: 'blue', statusClass: 'good',
        usageText: '이용 현황', usageDisp: '정상 이용 중',
        dateText: dateVal ? `결제일: ${dateVal.substring(5)}` : '결제일 미정'
      });
      renderSubscriptions();
      switchScreen('dashboard');
    }
  }

  function switchScreen(screenId) {
    document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    document.getElementById('screen-' + screenId).classList.add('active');
    
    const navs = document.querySelectorAll('.nav-item');
    if(screenId === 'dashboard') navs[0].classList.add('active');
    else if(screenId === 'add') navs[1].classList.add('active');
    else if(screenId === 'notif') navs[2].classList.add('active');
    else if(screenId === 'settings') navs[3].classList.add('active');
  }

  function changeFont(font) {
    document.documentElement.style.setProperty('--font-family', font);
  }

  function changeFontSize(scale) {
    document.documentElement.style.setProperty('--font-scale', scale);
  }

  renderSubscriptions();
</script>
</body>
</html>
"""

components.html(html_code, height=880, scrolling=True)
