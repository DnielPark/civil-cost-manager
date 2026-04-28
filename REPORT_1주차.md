# ✅ 1주차 작업 완료 보고

## 📋 완료 항목

### 1. GitHub 공개 레포 생성
- **URL**: https://github.com/DnielPark/civil-cost-manager
- **설명**: 토목 공사비 관리 데스크탑 애플리케이션

### 2. 기술 스택 확정 (Flask 웹 기반)
| 계층 | 기술 |
|------|------|
| Backend | Flask |
| Frontend | HTML + CSS + Vanilla JS |
| DB | SQLite3 (Python 내장) |
| 엑셀 | openpyxl + pandas |
| 포트 | **8080** (5000번 AirPlay 충돌로 변경) |

### 3. 프로젝트 구조
```
civil-cost-manager/
├── app.py                  # Flask 메인 (127.0.0.1:8080)
├── requirements.txt        # flask, openpyxl, pandas, python-dotenv
├── run.py                  # debug=False 실행 스크립트
├── database/
│   ├── __init__.py
│   └── init_db.py          # SQLite 초기화 (projects, cost_items 테이블)
├── routes/
│   ├── __init__.py
│   ├── main.py             # 페이지 라우트
│   └── api.py              # REST API (JSON)
├── static/
│   ├── css/style.css
│   └── js/app.js
├── templates/
│   ├── index.html          # ✅ 메인 대문 페이지 (완료)
│   ├── projects.html
│   ├── project_detail.html
│   └── error.html
```

### 4. ✅ 메인 대문 페이지 (Dashboard)
- **수정 파일**: `templates/index.html`, `static/css/style.css`
- **메뉴 카드 4개** (2x2 그리드):
  - 📊 프로젝트 관리 → `/projects` (200 OK)
  - 💰 단가 마스터 관리 → `/unit-prices` (404 - 미구현)
  - 📈 내역서 관리 → `/cost-items` (404 - 미구현)
  - 📁 파일 업로드 → `/upload` (404 - 미구현)
- **디자인**: 카드형, flexbox, hover 확대 효과
- **서버**: `http://localhost:8080`

### 5. 로컬 실행/중지 스크립트
```bash
# 서버 시작
cd ~/.openclaw/workspace/skills
./cost-manager-app-on.sh

# 서버 중지
./cost-manager-app-off.sh

# 코드 동기화
./cost-manager-pull.sh    # GitHub → 맥북
./cost-manager-push.sh "메시지"  # 맥북 → GitHub
```

## 📌 커밋 기록
| 커밋 ID | 내용 |
|---------|------|
| `eb1bb24` | Flask 프로젝트 초기 세팅 |
| `72eeb42` | 메인 대문 페이지 (Dashboard) 구현 |

## ⚠️ 이슈
- **포트 5000**: AirPlay 리시버와 충돌 → **8080**으로 변경하여 해결
- **디버그 모드**: `debug=True` 상태에서 포트 충돌 발생 → `run.py`로 분리하여 `debug=False` 실행 가능

## ▶️ 다음 단계 예정
1. config.py 표준화 작업
2. 단가 마스터 관리 페이지
3. 내역서 관리 페이지
4. 파일 업로드 기능
