# Selim Tools

세림전자 업무 효율화를 위해 개발한 Windows 프로그램의 공식 배포 저장소입니다.

**Selim Tools** 하나만 설치하면 아래 프로그램을 모두 설치할 수 있고, 실행할 때마다 최신 버전으로 맞춰 줍니다.

<p align="center">
  <img src="assets/hub.png" width="96" alt="Selim Tools 아이콘">
</p>

---

## 시작하기

1. [최신 릴리스](https://github.com/minsangOh/Selim-Tools/releases/latest)에서 `SelimTools-Setup-x.y.z.exe`를 내려받아 실행합니다. 관리자 권한은 필요 없습니다.
2. 바탕화면이나 시작 메뉴의 **Selim Tools**를 엽니다.
3. 쓰려는 프로그램의 버튼을 누릅니다.

| 버튼 | 동작 |
|---|---|
| **설치** | 처음 한 번 내려받아 설치한 뒤 실행합니다 |
| **업데이트 후 실행** | 새 버전으로 바꾼 뒤 실행합니다 |
| **실행** | 이미 최신 버전이면 바로 실행합니다 |

- Selim Tools 자신도 새 버전이 나오면 창 위쪽에 알림이 뜨고, **지금 업데이트**를 누르면 바뀐 뒤 다시 열립니다.
- 인터넷에 연결되지 않으면 마지막으로 받은 목록을 보여 주고, 설치된 버전을 그대로 실행합니다.
- 실행 중인 프로그램은 바꿀 수 없으므로 그대로 실행하고, 업데이트는 다음 실행 때 합니다.
- 받은 파일은 목록에 적힌 크기와 SHA-256 해시가 맞을 때만 설치합니다.

> 설치 파일이 코드 서명되지 않아 처음 실행할 때 Windows SmartScreen 경고가 나올 수 있습니다. 파일 이름이 `SelimTools-Setup-…exe`인지 확인한 뒤 **추가 정보 → 실행**을 누르세요.

---

## 포함된 프로그램

<table>
  <tr>
    <td align="center" width="96"><img src="assets/wim.ico" width="56" alt=""></td>
    <td><strong>작업지도서 자재 소요량</strong><br>작업지도서 Excel에서 전선·터미널·부자재 소요량을 모아 결과 파일로 만듭니다.</td>
  </tr>
  <tr>
    <td align="center"><img src="assets/ctq.ico" width="56" alt=""></td>
    <td><strong>CTQ 승인원 자동입력</strong><br>새 승인원의 CTQ 시트에 DB의 측정값과 사진을 채웁니다. 에어컨·냉장고용이며 Microsoft Excel이 필요합니다.</td>
  </tr>
  <tr>
    <td align="center"><img src="assets/fileRay_Selim.png" width="56" alt=""></td>
    <td><strong>FileRay</strong><br>등록한 폴더의 파일명과 문서 본문을 인터넷 없이 빠르게 검색합니다.</td>
  </tr>
  <tr>
    <td align="center"><img src="assets/Diff_PDF.ico" width="56" alt=""></td>
    <td><strong>Selim PDF Diff</strong><br>두 PDF 도면을 같은 좌표로 겹쳐 비교하고 바뀐 부분을 표시합니다.</td>
  </tr>
</table>

버전별 변경 내용은 Selim Tools의 **변경 내용** 링크나 [전체 릴리스](https://github.com/minsangOh/Selim-Tools/releases)에서 볼 수 있습니다.

### <img src="assets/ctq.ico" width="28" align="center" alt=""> CTQ 승인원 자동입력

Selim Tools로 설치한 CTQ는 `%LOCALAPPDATA%\SelimTools\apps\ctq\`에서 실행됩니다. 전에 exe 옆의 `DB\` 폴더를 쓰고 있었다면, CTQ 화면에서 DB 폴더를 그 위치(또는 팀 NAS)로 한 번 지정하세요. 지정한 위치는 업데이트 후에도 유지됩니다.

### <img src="assets/fileRay_Selim.png" width="28" align="center" alt=""> FileRay

사용자가 등록한 로컬 폴더의 파일명과 문서 본문을 인덱싱하여 필요한 업무 자료를 빠르게 검색하고 미리 볼 수 있는 Windows용 오프라인 문서 검색 프로그램입니다. 검색 데이터와 문서 정보는 사용자 PC에 저장되며 프로그램 사용 시 인터넷 연결이 필요하지 않습니다.

- 파일명 및 문서 본문 검색, 단어 중간에 있는 문자열도 검색
- 결과를 끝까지 이어서 불러오는 목록
- 등록 폴더와 하위 폴더 자동 인덱싱, 파일 추가·수정·삭제 자동 반영
- 파일 형식, 날짜 및 폴더 범위 검색, 결과 내 재검색(포함·제외)
- 문서 내용 미리보기와 검색어 강조, 엑셀 결과의 셀 주소 표시
- 원본 파일 열기, 탐색기에서 파일 위치 열기, 파일 경로 복사
- 문서 북마크, 메모 및 사용자 태그
- 중복 파일 탐지, 검색 결과 CSV 내보내기

| 분류 | 지원 형식 |
|---|---|
| 한글 문서 | `.hwp`, `.hwpx` |
| Microsoft Office | `.docx`, `.pptx`, `.xls`, `.xlsx` |
| 텍스트 | `.txt`, `.md` |
| 이메일 | `.eml` |

### <img src="assets/Diff_PDF.ico" width="28" align="center" alt=""> Selim PDF Diff

두 개의 PDF 도면을 동일한 페이지와 좌표를 기준으로 비교하여 실제로 변경된 부분을 표시합니다. 도면 Revision 변경 검토 시 변경 위치를 빠르게 확인할 수 있도록 개발되었습니다.

- 두 PDF 도면의 동일 좌표 기준 비교, 변경 영역 자동 검출
- 변경 위치 반투명 Highlight 표시, 좌우 Highlight 독립 표시 및 숨김, 투명도 조절
- PDF 파일 Drag & Drop, 페이지 이동 및 확대·축소
- 좌우 화면 위치와 동일 PDF 좌표의 커서 위치 동기화
- 현재 비교 화면 클립보드 복사, 고해상도 디스플레이 지원

---

## 지원 환경과 설치 위치

Windows 10, Windows 11 (64-bit)

| 항목 | 위치 |
|---|---|
| Selim Tools | `%LOCALAPPDATA%\Programs\Selim Tools` |
| 작업지도서 자재 소요량, CTQ 승인원 자동입력 | `%LOCALAPPDATA%\SelimTools\apps\<id>\` (설치 없이 실행하는 exe) |
| FileRay | `%LOCALAPPDATA%\FileRay` |
| Selim PDF Diff | `%LOCALAPPDATA%\Programs\Selim PDF Diff` |
| Selim Tools 기록 | `%LOCALAPPDATA%\SelimTools\hub.log` |

Selim Tools를 제거해도 Selim Tools가 설치한 프로그램과 그 데이터는 남습니다. FileRay와 Selim PDF Diff는 Windows 설정 → 앱에서 따로 제거할 수 있습니다.

---

## 관리자용: 새 버전 배포

Selim Tools는 이 저장소 `master`의 [`manifest.json`](manifest.json)을 읽어 프로그램마다 최신 버전을 판단합니다. 원본 저장소에 릴리스를 만든 뒤 이 저장소에서 다음을 실행하면, Selim-Tools 릴리스 생성부터 `manifest.json` 갱신·푸시까지 한 번에 처리합니다 (gh CLI 로그인 필요).

```powershell
python tools/publish.py ctq                    # 원본 저장소의 Latest 릴리스
python tools/publish.py fileray --tag v0.4.0   # 태그 지정
```

| id | 프로그램 | 원본 저장소 | 형태 |
|---|---|---|---|
| `wim` | 작업지도서 자재 소요량 | work-instruction-materials-gui | exe 하나 |
| `ctq` | CTQ 승인원 자동입력 | CTQ_DB_Tool | exe 하나 |
| `fileray` | FileRay | fileRay_Selim | NSIS 설치 파일 |
| `pdfdiff` | Selim PDF Diff | Diff_PDF | NSIS 설치 파일 |

- 원본 릴리스에는 `.exe` 첨부 파일이 하나만 있어야 합니다. 설치형은 관리자 권한 없이 `/S`로 무인 설치되는 사용자 단위 NSIS여야 합니다.
- 목록보다 낮거나 같은 버전은 올리지 않습니다. 같은 버전이 두 번 올라가거나 목록이 옛 버전으로 되돌아가지 않게 하기 위해서입니다. Selim PDF Diff v2.0.0은 Selim Tools 이전에 올린 이 저장소의 `v2.0.0` 릴리스를 가리킵니다.
- 앱 릴리스의 태그는 `<id>-v<버전>`입니다. Selim Tools 릴리스(`hub-v…`)만 **Latest**로 두어, 위의 "최신 릴리스" 링크가 늘 Selim Tools 설치 파일을 가리키게 합니다.
- `manifest.json`이 바뀌면 각 PC의 Selim Tools는 다음 실행이나 **새로 고침** 때 새 목록을 받습니다 (GitHub 캐시로 몇 분 늦을 수 있습니다).

### Selim Tools 빌드와 배포

```powershell
powershell -ExecutionPolicy Bypass -File hub\build.ps1   # 테스트 → 빌드 → hub\dist\installer\SelimTools-Setup-x.y.z.exe
python tools/publish.py hub --notes-file notes.md
```

버전은 `hub/main.py`의 `APP_VERSION` 하나로 관리합니다. 빌드에는 Python 3.13과 NSIS가 필요합니다 (NSIS를 설치하지 않았다면 Tauri가 받아 둔 NSIS를 씁니다).

### 프로그램 추가

`manifest.json`의 `apps`에 항목(`id`, `name`, `description`, `kind`, `exe`, `icon`, 설치형은 `uninstall_key`)을 넣고, `tools/publish.py`의 `SOURCES`에 원본 저장소를 적은 뒤 publish를 실행합니다. `url`이 빈 항목은 Selim Tools에 나타나지 않으므로 먼저 커밋해도 됩니다. 아이콘은 `assets/`에 둡니다.
