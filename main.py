<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SubCut - 구독 해지 & 가성비 관리</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body { background-color: #f1f5f9; color: #0f172a; display: flex; justify-content: center; min-height: 100vh; }
    .app-container { width: 100%; max-width: 430px; background: #ffffff; min-height: 100vh; display: flex; flex-direction: column; position: relative; box-shadow: 0 0 20px rgba(0,0,0,0.05); }
    
    /* 네비게이션 & 헤더 */
    .header { height: 60px; display: flex; justify-content: space-between; align-items: center; padding: 0 16px; border-bottom: 1px solid #e2e8f0; background: #ffffff; sticky: top; }
    .logo { font-size: 20px; font-weight: 800; color: #1e293b; }
    .header-right { display: flex; align-items: center; gap: 8px; }
    .badge-btn { background: #f1f5f9; color: #475569; border: none; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; cursor: pointer; }
    .avatar { width: 30px; height: 30px; border-radius: 50%; background: #3b82f6; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; }

    /* 화면 전환 (Tab) */
    .screen { display: none; padding: 16px; flex: 1; overflow-y: auto; padding-bottom: 80px; }
    .screen.active { display: block; }

    /* 대시보드 요약 배너 */
    .summary-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; margin-bottom: 20px; }
    .summary-title { font-size: 12px; color: #64748b; margin-bottom: 4px; }
    .summary-price { font-size: 24px; font-weight: 700; color: #0f172a; margin-bottom: 8px; }
    .alert-tag { background: #fef2f2; color: #ef4444; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 4px; display: inline-block; }

    /* 구독 카드 스타일 */
    .card-list { display: flex; flex-direction: column; gap: 12px; }
    .sub-card { background: #ffffff; border-radius: 12px; padding: 16px; border: 2px solid #e2e8f0; }
    .sub-card.good { border-color: #3b82f6; }
    .sub-card.bad { border-color: #ef4444; }
    
    .card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
    .card-info { display: flex; gap: 12px; align-items: center; }
    .icon-box { width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }
    .badge { font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 12px; }
    .badge.blue { background: #eff6ff; color: #2563eb; }
    .badge.red { background: #fef2f2; color: #dc2626; }

    .card-mid { margin-bottom: 12px; font-size: 13px; }
    .bar-bg { width: 100%; height: 8px; background: #e2e8f0; border-radius: 4px; margin-top: 6px; overflow: hidden; }
    .bar-fill { height: 100%; background: #3b82f6; border-radius: 4px; }
    .bar-fill.red { background: #ef4444; }

    .card-bottom { border-top: 1px solid #f1f5f9; padding-top: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #64748b; }
    .link-btn { font-weight: 700; text-decoration: none; cursor: pointer; }
    .link-btn.blue { color: #2563eb; }
    .link-btn.red { color: #dc2626; }

    /* 상세 화면 가성비 그래프 */
    .graph-box { background: white; border-radius: 12px; padding: 16px; border: 1px solid #e2e8f0; margin: 16px 0; display: flex; justify-content: space-around; align-items: flex-end; height: 160px; }
    .bar-group { display: flex; flex-direction: column; align-items: center; gap: 8px; font-size: 11px; color: #64748b; }
    .bar-pillar { width: 32px; border-radius: 4px 4px 0 0; }
    .feedback-box { background: #fef2f2; color: #b91c1c; padding: 12px; border-radius: 8px; font-size: 12px; line-height: 1.4; margin-bottom: 16px; }

    /* 바텀 네비게이션 바 */
    .bottom-nav { position: absolute; bottom: 0; width: 100%; height: 60px; background: #ffffff; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-around; align-items: center; }
    .nav-item { border: none; background: none; color: #64748b; font-size: 11px; display: flex; flex-direction: column; align-items: center; gap: 4px; cursor: pointer; }
    .nav-item.active { color: #3b82f6; font-weight: 700; }
  </style>
</head>
<body>

<div class="app-container">
  <!-- 상단 헤더 -->
  <header class="header">
    <div class="logo">SubCut</div>
    <div class="header-right">
      <button class="badge-btn" onclick="switchScreen('family')">가족 계정 (4명)</button>
      <div class="avatar">나</div>
    </div>
  </header>

  <!-- 1. 메인 대시보드 화면 -->
  <div id="screen-dashboard" class="screen active">
    <div class="summary-card">
      <div class="summary-title">이번 달 결제 예정 총액</div>
      <div class="summary-price">48,500원</div>
      <div class="alert-tag">⚠️ OTT 카테고리 2건 중복 구독 중</div>
    </div>

    <div class="card-list">
      <!-- 알뜰 카드 -->
      <div class="sub-card good" onclick="switchScreen('detail')">
        <div class="card-top">
          <div class="card-info">
            <div class="icon-box" style="background:#e50914;">N</div>
            <div>
              <div style="font-weight:700;">넷플릭스</div>
              <div style="font-size:12px; color:#64748b;">월 17,000원</div>
            </div>
          </div>
          <span class="badge blue">알뜰 이용 중 (상위 15%)</span>
        </div>
        <div class="card-mid">
          <div style="display:flex; justify-content:space-between; color:#64748b; font-size:11px;">
            <span>내 사용: 45시간</span>
            <span>평균: 30시간</span>
          </div>
          <div class="bar-bg"><div class="bar-fill" style="width: 85%;"></div></div>
        </div>
        <div class="card-bottom">
          <span>다음 결제일: 10월 15일</span>
          <a class="link-btn blue" href="https://www.netflix.com/youraccount" target="_blank">해지 이동 URL →</a>
        </div>
      </div>

      <!-- 낭비 카드 -->
      <div class="sub-card bad" onclick="switchScreen('detail')">
        <div class="card-top">
          <div class="card-info">
            <div class="icon-box" style="background:#ff153c;">T</div>
            <div>
              <div style="font-weight:700;">티빙</div>
              <div style="font-size:12px; color:#64748b;">월 13,900원</div>
            </div>
          </div>
          <span class="badge red">낭비 주의 (하위 80%)</span>
        </div>
        <div class="card-mid">
          <div style="color:#dc2626; font-weight:700; font-size:12px;">⚠️ 이번 달 시청 시간 0시간 (D-3)</div>
          <div class="bar-bg"><div class="bar-fill red" style="width: 5%;"></div></div>
        </div>
        <div class="card-bottom">
          <span style="color:#dc2626; font-weight:600;">3일 후 자동 결제</span>
          <a class="link-btn red" href="https://www.tving.com" target="_blank">원클릭 해지하기 🔗</a>
        </div>
      </div>
    </div>
  </div>

  <!-- 2. 구독 등록 화면 -->
  <div id="screen-add" class="screen">
    <h3 style="margin-bottom: 16px;">새 구독 서비스 추가</h3>
    <div style="display:flex; flex-direction:column; gap:12px;">
      <input type="text" placeholder="앱/서비스 검색 (예: 멜론)" style="padding:12px; border:1px solid #cbd5e1; border-radius:8px;">
      <input type="number" placeholder="월 결제 금액 (원)" style="padding:12px; border:1px solid #cbd5e1; border-radius:8px;">
      <div>
        <label style="font-size:12px; color:#64748b;">주간 평균 사용 시간</label>
        <input type="range" min="0" max="20" value="2" style="width:100%; margin-top:8px;">
      </div>
      <button onclick="switchScreen('dashboard')" style="padding:14px; background:#3b82f6; color:white; border:none; border-radius:8px; font-weight:700; margin-top:12px; cursor:pointer;">등록 완료하기</button>
    </div>
  </div>

  <!-- 3. 가성비 분석 상세 화면 -->
  <div id="screen-detail" class="screen">
    <div style="background:#000; color:white; padding:16px; border-radius:8px; text-align:center; margin-bottom:16px;">
      <h2>티빙 프리미엄 요금제</h2>
    </div>
    <h4>가성비 분석 비교</h4>
    <div class="graph-box">
      <div class="bar-group">
        <span>32시간</span>
        <div class="bar-pillar" style="height:100px; background:#8b5cf6;"></div>
        <span>사용자 평균</span>
      </div>
      <div class="bar-group">
        <span>4시간</span>
        <div class="bar-pillar" style="height:20px; background:#ef4444;"></div>
        <span>나의 사용</span>
      </div>
    </div>
    <div class="feedback-box">
      💡 사용자 평균보다 28시간 덜 쓰고 있어요! 1시간당 3,475원을 지불하는 꼴입니다. 해지를 권장합니다.
    </div>
    <a href="https://www.tving.com" target="_blank" style="display:block; text-align:center; background:#ef4444; color:white; padding:14px; border-radius:8px; font-weight:700; text-decoration:none;">해지 페이지 직링크로 이동 ↗</a>
  </div>

  <!-- 4. 가족 통합 관리 화면 -->
  <div id="screen-family" class="screen">
    <h3>우리 가족 구독 지출</h3>
    <p style="font-size:13px; color:#64748b; margin-top:4px; margin-bottom:16px;">월 102,400원 (총 8개 이용 중)</p>

    <div style="background:#fff; border:1px solid #e2e8f0; border-radius:8px; padding:12px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-weight:700; font-size:14px;">엄마 계정: 임영웅 팬클럽</div>
        <div style="font-size:12px; color:#64748b;">다음 결제일: 9월 28일</div>
      </div>
      <button style="background:#f97316; color:white; border:none; padding:8px 10px; border-radius:6px; font-size:11px; font-weight:700; cursor:pointer;">자녀 대리 해지 안내받기</button>
    </div>
  </div>

  <!-- 하단 탭 바 -->
  <nav class="bottom-nav">
    <button class="nav-item active" onclick="switchScreen('dashboard')">🏠<br>홈</button>
    <button class="nav-item" onclick="switchScreen('add')">➕<br>구독 추가</button>
    <button class="nav-item" onclick="switchScreen('family')">👨‍👩‍👧<br>가족 관리</button>
  </nav>
</div>

<script>
  function switchScreen(screenId) {
    document.querySelectorAll('.screen').forEach(el => el.classList.remove('active'));
    document.getElementById('screen-' + screenId).classList.add('active');
  }
</script>
</body>
</html>
