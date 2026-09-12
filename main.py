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

  <!-- 구글 한국어 폰트 불러오기 -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cute+Font&family=Gamja+Flower&family=GangwonEduModu:wght@400;700&family=Nanum+Gothic:wght@400;700&family=Sunflower:wght@500;700&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --bg-color: #e0f2fe;
      --card-bg: #ffffff;
      --primary-color: #0284c7;
      --text-color: #0f172a;
      --font-family: 'GangwonEduModu', sans-serif;
      --font-scale: 1;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: var(--font-family); }
    html { font-size: calc(16px * var(--font-scale)); }
    body { background-color: var(--bg-color); color: var(--text-color); display: flex; justify-content: center; min-height: 100vh; transition: all 0.3s ease; }
    .app-container { width: 100%; max-width: 430px; background: var(--card-bg); min-height: 100vh; display: flex; flex-direction: column; position: relative; box-shadow: 0 0 20px rgba(0,0,0,0.08); }
    
    .header { height: 60px; display: flex; justify-content: space-between; align-items: center; padding: 0 16px; border-bottom: 1px solid rgba(0,0,0,0.08); background: var(--card-bg); position: sticky; top: 0; z-index: 100; }
    .logo { font-size: 1.4rem; font-weight: 800; color: var(--primary-color); cursor: pointer; user-select: none; }
    .header-right { display: flex; align-items: center; gap: 12px; }
    .icon-btn { background: none; border: none; font-size: 1.25rem; cursor: pointer; position: relative; }
    .notif-badge { position: absolute; top: -2px; right: -2px; width: 8px; height: 8px; background: #ef4444; border-radius: 50%; }
    .avatar { width: 32px; height: 32px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.85rem; cursor: pointer; }

    .screen { display: none; padding: 16px; flex: 1; overflow-y: auto; padding-bottom: 80px; }
    .screen.active { display: block; }

    .summary-card { background: rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.08); border-radius: 16px; padding: 18px; margin-bottom: 16px; }
    .summary-title { font-size: 0.8rem; opacity: 0.7; margin-bottom: 4px; }
    .summary-price { font-size: 1.6rem; font-weight: 700; margin-bottom: 8px; }
    .alert-tag { background: #fef2f2; color: #ef4444; font-size: 0.75rem; font-weight: 700; padding: 6px 10px; border-radius: 6px; display: inline-block; }

    .custom-panel { background: rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; padding: 14px; margin-bottom: 16px; display: flex; flex-direction: column; gap: 10px; font-size: 0.85rem; }
    .custom-row { display: flex; justify-content: space-between; align-items: center; }
    .custom-select { padding: 6px 10px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 0.8rem; background: var(--card-bg); color: var(--text-color); }

    .card-list { display: flex; flex-direction: column; gap: 12px; }
    .sub-card { background: var(--card-bg); border-radius: 14px; padding: 16px; border: 2px solid rgba(0,0,0,0.08); cursor: pointer; transition: transform 0.1s ease; }
    .sub-card:active { transform: scale(0.98); }
    .sub-card.good { border-color: var(--primary-color); }
    .sub-card.bad { border-color: #ef4444; }
    .sub-card.warning { border-color: #f59e0b; }

    .card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .card-info { display: flex; gap: 10px; align-items: center; }
    .app-icon-img { width: 38px; height: 38px; border-radius: 10px; object-fit: cover; background: #f1f5f9; border: 1px solid rgba(0,0,0,0.05); }
    .badge { font-size: 0.7rem; font-weight: 700; padding: 4px 8px; border-radius: 12px; }
    .badge.blue { background: #eff6ff; color: #2563eb; }
    .badge.red { background: #fef2f2; color: #dc2626; }
    .badge.orange { background: #fffbebfb; color: #d97706; }

    .card-mid { margin-bottom: 10px; font-size: 0.8rem; }
    .usage-text { display: flex; justify-content: space-between; font-weight: 600; margin-bottom: 4px; }
    .bar-bg { width: 100%; height: 8px; background: rgba(0,0,0,0.08); border-radius: 4px; overflow: hidden; }
    .bar-fill { height: 100%; background: var(--primary-color); border-radius: 4px; }
    .bar-fill.red { background: #ef4444; }
    .bar-fill.orange { background: #f59e0b; }

    .card-bottom { border-top: 1px solid rgba(0,0,0,0.05); padding-top: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; opacity: 0.8; }
    .link-btn { font-weight: 700; text-decoration: none; color: var(--primary-color); padding: 4px 8px; background: rgba(0,0,0,0.03); border-radius: 6px; }

    .notif-item { padding: 12px; border-bottom: 1px solid rgba(0,0,0,0.08); display: flex; gap: 12px; align-items: flex-start; }
    .notif-icon { font-size: 1.1rem; }
    .notif-title { font-weight: 700; font-size: 0.85rem; }
    .notif-desc { font-size: 0.75rem; opacity: 0.8; margin-top: 2px; }

    .member-tabs { display: flex; gap: 8px; margin-bottom: 16px; overflow-x: auto; padding-bottom: 4px; }
    .mem-btn { padding: 8px 14px; background: rgba(0,0,0,0.05); border: none; border-radius: 20px; font-size: 0.8rem; font-weight: 700; cursor: pointer; white-space: nowrap; opacity: 0.7; color: var(--text-color); }
    .mem-btn.active { background: var(--primary-color); color: white; opacity: 1; }

    .bottom-nav { position: fixed; bottom: 0; width: 100%; max-width: 430px; height: 60px; background: var(--card-bg); border-top: 1px solid rgba(0,0,0,0.08); display: flex; justify-content: space-around; align-items: center; z-index: 100; }
    .nav-item { border: none; background: none; color: #64748b; font-size: 0.7rem; display: flex; flex-direction: column; align-items: center; gap: 3px; cursor: pointer; }
    .nav-item.active { color: var(--primary-color); font-weight: 700; }
  </style>
</head>
<body>

<div class="app-container">
  <header class="header">
    <div class="logo" onclick="switchScreen('dashboard')">ZeroSub</div>
    <div class="header-right">
      <button class="icon-btn" onclick="switchScreen('notif')">
        🔔<span class="notif-badge"></span>
      </button>
      <div class="avatar" onclick="switchScreen('settings')">나</div>
    </div>
  </header>

  <div id="screen-dashboard" class="screen active">
    <div class="summary-card">
      <div class="summary-title">내가 결제하는 월 구독 금액</div>
      <div class="summary-price"><span id="total-price-text">79,300</span>원 <span style="font-size:0.85rem; opacity:0.6; font-weight:400;">(<span id="total-count-text">6</span>개)</span></div>
      <div class="alert-tag">⚠️ 유튜브, 스포티파이 가족 중복 계정 감지!</div>
    </div>

    <div class="card-list" id="main-sub-list">
      <!-- 구독 리스트가 자바스크립트로 동적 생성됩니다 -->
    </div>
  </div>

  <div id="screen-notif" class="screen">
    <h3 style="margin-bottom:16px;">알림 센터</h3>
    <div class="notif-item">
      <div class="notif-icon">🚨</div>
      <div>
        <div class="notif-title">티빙 결제 3일 전 알림</div>
        <div class="notif-desc">이번 달 시청 시간이 0시간 20분입니다. 결제 전 해지하시겠어요?</div>
      </div>
    </div>
    <div class="notif-item">
      <div class="notif-icon">👨‍👩‍👧</div>
      <div>
        <div class="notif-title">가족 중복 구독 발견!</div>
        <div class="notif-desc">아빠 계정과 '유튜브 프리미엄'을 각각 결제 중입니다. 패밀리 요금제로 통합 시 월 9,000원 절약 가능!</div>
      </div>
    </div>
  </div>

  <div id="screen-detail" class="screen">
    <button onclick="switchScreen('dashboard')" style="border:none; background:none; opacity:0.7; font-weight:700; cursor:pointer; margin-bottom:12px;">← 뒤로가기</button>
    <div style="background:#0f172a; color:white; padding:20px; border-radius:12px; text-align:center; margin-bottom:16px;">
      <h2 id="det-title">서비스 이름</h2>
      <p id="det-price" style="color:#94a3b8; margin-top:4px;">월 0원</p>
    </div>
    <h4 style="margin-bottom:8px;">이용 현황 상세 분석</h4>
    <div style="background:var(--card-bg); border:1px solid rgba(0,0,0,0.08); padding:16px; border-radius:12px; margin-bottom:16px;">
      <p style="margin-bottom:8px;"><strong>내 사용량:</strong> <span id="det-use">0</span></p>
      <p style="margin-bottom:8px;"><strong>권장/평균 기준:</strong> <span id="det-avg">0</span></p>
      <p style="margin-bottom:8px;"><strong>진단 상태:</strong> <span id="det-status" style="color:#ef4444; font-weight:700;">-</span></p>
    </div>
    <a id="det-link" href="#" target="_blank" style="display:block; text-align:center; background:#ef4444; color:white; padding:14px; border-radius:10px; font-weight:700; text-decoration:none;">해지/계정 설정 페이지로 이동 ↗</a>
  </div>

  <div id="screen-family" class="screen">
    <h3>우리 가족 구독 지출</h3>
    <p style="font-size:0.8rem; opacity:0.7; margin-top:4px; margin-bottom:16px;">가족 전체 총 148,200원 지출 중</p>

    <div class="member-tabs">
      <button class="mem-btn active" onclick="switchFamily('me', this)">나</button>
      <button class="mem-btn" onclick="switchFamily('mom', this)">엄마 (3개)</button>
      <button class="mem-btn" onclick="switchFamily('dad', this)">아빠 (4개)</button>
      <button class="mem-btn" onclick="switchFamily('sibling', this)">동생 (2개)</button>
    </div>

    <div id="fam-list" class="card-list"></div>
  </div>

  <!-- 새로 등록하기 기능 완벽 동작 -->
  <div id="screen-add" class="screen">
    <h3 style="margin-bottom: 16px;">새 구독 서비스 추가</h3>
    <form onsubmit="addSubscription(event)" style="display:flex; flex-direction:column; gap:12px;">
      <input type="text" id="add-name" placeholder="서비스 이름 (예: 왓챠, 디즈니플러스)" required style="padding:12px; border:1px solid #cbd5e1; border-radius:8px; font-size:0.9rem;">
      <input type="number" id="add-price" placeholder="월 결제 금액 (원) 예: 7900" required style="padding:12px; border:1px solid #cbd5e1; border-radius:8px; font-size:0.9rem;">
      <button type="submit" style="padding:14px; background:var(--primary-color); color:white; border:none; border-radius:8px; font-weight:700; margin-top:12px; cursor:pointer; font-size:0.95rem;">구독 등록하기</button>
    </form>
  </div>

  <div id="screen-settings" class="screen">
    <h3 style="margin-bottom:16px;">내 계정 및 설정</h3>
    
    <div style="background:var(--card-bg); border:1px solid rgba(0,0,0,0.08); border-radius:12px; padding:16px; margin-bottom:16px;">
      <p style="font-weight:700;">홍길동 (gildong@example.com)</p>
      <p style="font-size:0.75rem; opacity:0.7; margin-top:4px;">ZeroSub 프리미엄 가계부 이용 중</p>
    </div>

    <h4 style="margin-bottom:8px;">🎨 화면 스타일 설정</h4>
    <div class="custom-panel">
      <div class="custom-row">
        <span>🎨 배경 테마 색상:</span>
        <select class="custom-select" onchange="changeTheme(this.value)">
          <option value="pastel-blue">파스텔블루 (기본)</option>
          <option value="lime-green">라임그린</option>
          <option value="mystic-pink">미스틱핑크</option>
          <option value="dark">다크 모드</option>
        </select>
      </div>
      <div class="custom-row">
        <span>✏️ 글꼴 종류 선택:</span>
        <select class="custom-select" onchange="changeFont(this.value)">
          <option value="'GangwonEduModu', sans-serif">강원교육모두체 (기본)</option>
          <option value="'Gamja Flower', cursive">감자꽃마을</option>
          <option value="'Nanum Gothic', sans-serif">나눔고딕</option>
          <option value="'Cute Font', cursive">귀여운폰트</option>
          <option value="'Sunflower', sans-serif">스타일리</option>
        </select>
      </div>
      <div class="custom-row">
        <span>🔍 글꼴 크기 조절:</span>
        <select class="custom-select" onchange="changeFontSize(this.value)">
          <option value="1">보통 (기본)</option>
          <option value="0.88">작게</option>
          <option value="1.15">크게</option>
        </select>
      </div>
    </div>

    <h4 style="margin-bottom:8px; margin-top:16px;">자주 묻는 질문 (FAQ)</h4>
    <div style="display:flex; flex-direction:column; gap:8px; font-size:0.8rem;">
      <details style="background:var(--card-bg); padding:10px; border-radius:8px; border:1px solid rgba(0,0,0,0.08);">
        <summary style="font-weight:700; cursor:pointer;">왜 바로 원클릭 해지가 안 되나요?</summary>
        <p style="opacity:0.7; margin-top:6px; font-size:0.75rem;">서비스사 보안 정책상 계정 해지 버튼 연결 URL로 직접 연결해 드립니다.</p>
      </details>
    </div>
  </div>

  <nav class="bottom-nav">
    <button class="nav-item active" onclick="switchScreen('dashboard')">🏠<br>홈</button>
    <button class="nav-item" onclick="switchScreen('add')">➕<br>구독 추가</button>
    <button class="nav-item" onclick="switchScreen('family')">👨‍👩‍👧<br>가족 관리</button>
    <button class="nav-item" onclick="switchScreen('settings')">⚙️<br>설정</button>
  </nav>
</div>

<script>
  // 유명 브랜드 도메인 로고 맵 (자동 아이콘 매칭)
  const domainMap = {
    '넷플릭스': 'netflix.com',
    '유튜브': 'youtube.com',
    '유튜브 프리미엄': 'youtube.com',
    '티빙': 'tving.com',
    '멜론': 'melon.com',
    '스포티파이': 'spotify.com',
    '배민클럽': 'baemin.com',
    '배달의민족': 'baemin.com',
    '왓챠': 'watcha.com',
    '쿠팡': 'coupang.com',
    '쿠팡 와우': 'coupang.com',
    '웨이브': 'wavve.com',
    '디즈니': 'disneyplus.com',
    '디즈니플러스': 'disneyplus.com',
    '애플뮤직': 'apple.com',
    '밀리의서재': 'millie.co.kr'
  };

  function getIconUrl(name) {
    const cleanName = name.replace(/\s+/g, '');
    let domain = 'google.com';
    for (let key in domainMap) {
      if (cleanName.includes(key.replace(/\s+/g, ''))) {
        domain = domainMap[key];
        break;
      }
    }
    if (domain === 'google.com') {
      domain = cleanName.toLowerCase() + '.com';
    }
    return `https://www.google.com/s2/favicons?domain=${domain}&sz=128`;
  }

  // 초기 내 구독 목록 데이터
  let subscriptions = [
    { title: '넷플릭스', price: 17000, type: '영상 스트리밍', use: '32시간 40분', avg: '15시간 00분', fill: '80%', status: '정상 이용 중', url: 'https://www.netflix.com/youraccount', badgeText: '알뜰 활용', badgeClass: 'blue', statusClass: 'good', usageText: '이번 달 시청시간', usageVal: '32시간 40분', dateText: '다음 결제일: 10월 15일' },
    { title: '유튜브 프리미엄', price: 14900, type: '영상/음악', use: '48시간 10분', avg: '20시간 00분', fill: '90%', status: '아빠 계정과 중복 이용 중', url: 'https://www.youtube.com/paid_memberships', badgeText: '가족 중복 주의', badgeClass: 'orange', statusClass: 'warning', usageText: '시청시간', usageVal: '48시간 10분 (아빠도 구독 중!)', dateText: '다음 결제일: 10월 02일' },
    { title: '티빙', price: 13900, type: '영상 스트리밍', use: '0시간 20분', avg: '12시간 00분', fill: '5%', status: '해지 강력 권장 (D-3)', url: 'https://www.tving.com/my/subscription', badgeText: '낭비 경고 (D-3)', badgeClass: 'red', statusClass: 'bad', usageText: '이번 달 시청시간', usageVal: '0시간 20분', dateText: '3일 후 13,900원 자동결제' },
    { title: '멜론', price: 10900, type: '음악 스트리밍', use: '재생 12회', avg: '평균 250회', fill: '8%', status: '스포티파이와 기능 중복', url: 'https://www.melon.com/buy/pamphlet/continue.htm', badgeText: '음악앱 중복', badgeClass: 'red', statusClass: 'bad', usageText: '월간 총 재생 횟수', usageVal: '12회 (방치 중)', dateText: '다음 결제일: 09월 28일' },
    { title: '스포티파이', price: 11900, type: '음악 스트리밍', use: '재생 450회', avg: '평균 200회', fill: '85%', status: '정상 이용 중', url: 'https://www.spotify.com/kr-ko/account/overview/', badgeText: '주력 음악앱', badgeClass: 'blue', statusClass: 'good', usageText: '월간 총 재생 횟수', usageVal: '450회', dateText: '다음 결제일: 10월 05일' },
    { title: '배민클럽', price: 3900, type: '배달 혜택', use: '3회 이용 (혜택 2,100원)', avg: '월 5회 이상 권장', fill: '40%', status: '본전 미달 이용 중', url: 'https://www.baemin.com', badgeText: '본전 미달', badgeClass: 'orange', statusClass: 'warning', usageText: '이번 달 주문 할인', usageVal: '3회 (구독료 미달)', dateText: '다음 결제일: 10월 11일' }
  ];

  function renderSubscriptions() {
    const container = document.getElementById('main-sub-list');
    container.innerHTML = '';

    let totalPrice = 0;

    subscriptions.forEach((sub, idx) => {
      totalPrice += sub.price;
      const iconUrl = getIconUrl(sub.title);
      
      const card = document.createElement('div');
      card.className = `sub-card ${sub.statusClass}`;
      card.onclick = () => openDetail(sub.title, `${sub.price.toLocaleString()}원`, sub.type, sub.use, sub.avg, sub.fill, sub.status, sub.url);
      
      card.innerHTML = `
        <div class="card-top">
          <div class="card-info">
            <img class="app-icon-img" src="${iconUrl}" onerror="this.src='https://www.google.com/s2/favicons?domain=google.com&sz=128'" alt="${sub.title}">
            <div>
              <div style="font-weight:700;">${sub.title}</div>
              <div style="font-size:0.75rem; opacity:0.7;">월 ${sub.price.toLocaleString()}원</div>
            </div>
          </div>
          <span class="badge ${sub.badgeClass}">${sub.badgeText}</span>
        </div>
        <div class="card-mid">
          <div class="usage-text">
            <span>${sub.usageText}</span>
            <span>${sub.usageVal}</span>
          </div>
          <div class="bar-bg"><div class="bar-fill ${sub.badgeClass === 'red' ? 'red' : (sub.badgeClass === 'orange' ? 'orange' : '')}" style="width: ${sub.fill};"></div></div>
        </div>
        <div class="card-bottom">
          <span>${sub.dateText}</span>
          <span class="link-btn">상세 분석 →</span>
        </div>
      `;
      container.appendChild(card);
    });

    document.getElementById('total-price-text').innerText = totalPrice.toLocaleString();
    document.getElementById('total-count-text').innerText = subscriptions.length;
  }

  // 구독 신규 추가 기능
  function addSubscription(e) {
    e.preventDefault();
    const nameInput = document.getElementById('add-name');
    const priceInput = document.getElementById('add-price');

    const name = nameInput.value.trim();
    const price = parseInt(priceInput.value.trim());

    if(name && !isNaN(price)) {
      subscriptions.unshift({
        title: name,
        price: price,
        type: '신규 구독 서비스',
        use: '이용 데이터 수집 중',
        avg: '분석 중',
        fill: '50%',
        status: '신규 등록 완료',
        url: '#',
        badgeText: '신규 추가',
        badgeClass: 'blue',
        statusClass: 'good',
        usageText: '이용 현황',
        usageVal: '이용 중',
        dateText: '다음 결제일: 등록 완료'
      });

      nameInput.value = '';
      priceInput.value = '';

      renderSubscriptions();
      switchScreen('dashboard');
    }
  }

  function switchScreen(screenId) {
    document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    document.getElementById('screen-' + screenId).classList.add('active');
    
    if(screenId === 'family') {
      switchFamily('me', document.querySelectorAll('.mem-btn')[0]);
    }
  }

  function openDetail(title, price, type, use, avg, fill, status, linkUrl) {
    document.getElementById('det-title').innerText = title;
    document.getElementById('det-price').innerText = "월 " + price + " (" + type + ")";
    document.getElementById('det-use').innerText = use;
    document.getElementById('det-avg').innerText = avg;
    document.getElementById('det-status').innerText = status;
    document.getElementById('det-link').href = linkUrl;
    switchScreen('detail');
  }

  const familyData = {
    me: [],
    mom: [
      { name: '임영웅 팬클럽 영웅시대', price: '15,000원', desc: '다음 결제일: 09월 28일' },
      { name: '쿠팡 와우 멤버십', price: '7,890원', desc: '가족 통합 쇼핑 이용 중' },
      { name: '웨이브 (Wavve)', price: '10,900원', desc: '시청시간: 18시간 10분' }
    ],
    dad: [
      { name: '유튜브 프리미엄', price: '14,900원', desc: '⚠️ 자녀(나)와 중복 구독 중!' },
      { name: '네이버플러스 멤버십', price: '4,900원', desc: '적립 혜택 알뜰 이용 중' },
      { name: '밀리의 서재', price: '9,900원', desc: '월 독서시간: 5시간 20분' },
      { name: '골프존 GDR 패스', price: '25,000원', desc: '이용 횟수: 월 8회' }
    ],
    sibling: [
      { name: '애플 뮤직', price: '8,900원', desc: '재생: 310회' },
      { name: '인스타360 클라우드', price: '4,500원', desc: '용량 70% 사용 중' }
    ]
  };

  function switchFamily(member, btn) {
    document.querySelectorAll('.mem-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const container = document.getElementById('fam-list');
    container.innerHTML = '';

    let list = member === 'me' ? subscriptions : familyData[member];

    list.forEach(item => {
      const card = document.createElement('div');
      card.className = 'sub-card';
      const iconUrl = getIconUrl(item.title || item.name);
      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div style="display:flex; align-items:center; gap:10px;">
            <img class="app-icon-img" src="${iconUrl}" onerror="this.src='https://www.google.com/s2/favicons?domain=google.com&sz=128'">
            <div>
              <div style="font-weight:700;">${item.title || item.name}</div>
              <div style="font-size:0.75rem; opacity:0.7;">${item.desc || ('월 ' + item.price.toLocaleString() + '원')}</div>
            </div>
          </div>
          <div style="font-weight:700;">${item.price ? (typeof item.price === 'number' ? item.price.toLocaleString() + '원' : item.price) : ''}</div>
        </div>
      `;
      container.appendChild(card);
    });
  }

  function changeTheme(theme) {
    const root = document.documentElement;
    if(theme === 'pastel-blue') {
      root.style.setProperty('--bg-color', '#e0f2fe');
      root.style.setProperty('--card-bg', '#ffffff');
      root.style.setProperty('--primary-color', '#0284c7');
      root.style.setProperty('--text-color', '#0f172a');
    } else if(theme === 'lime-green') {
      root.style.setProperty('--bg-color', '#ecfdf5');
      root.style.setProperty('--card-bg', '#ffffff');
      root.style.setProperty('--primary-color', '#10b981');
      root.style.setProperty('--text-color', '#064e3b');
    } else if(theme === 'mystic-pink') {
      root.style.setProperty('--bg-color', '#fdf2f8');
      root.style.setProperty('--card-bg', '#ffffff');
      root.style.setProperty('--primary-color', '#ec4899');
      root.style.setProperty('--text-color', '#831843');
    } else if(theme === 'dark') {
      root.style.setProperty('--bg-color', '#0f172a');
      root.style.setProperty('--card-bg', '#1e293b');
      root.style.setProperty('--primary-color', '#38bdf8');
      root.style.setProperty('--text-color', '#f8fafc');
    }
  }

  function changeFont(font) {
    document.documentElement.style.setProperty('--font-family', font);
  }

  function changeFontSize(scale) {
    document.documentElement.style.setProperty('--font-scale', scale);
  }

  // 초기 로드 시 구독 리스트 출력
  renderSubscriptions();
</script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)
