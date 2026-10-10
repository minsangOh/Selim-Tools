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

버전별 변경 내용은 아래 [업데이트 내역](#업데이트-내역)에 정리해 두었습니다. 자세한 내용은 Selim Tools의 **변경 내용** 링크나 [전체 릴리스](https://github.com/minsangOh/Selim-Tools/releases)에서 볼 수 있습니다.

### <img src="assets/ctq.ico" width="28" align="center" alt=""> CTQ 승인원 자동입력

Selim Tools로 설치한 CTQ는 `%LOCALAPPDATA%\SelimTools\apps\ctq\`에서 실행됩니다. 전에 exe 옆의 `DB\` 폴더를 쓰고 있었다면, CTQ 화면에서 DB 폴더를 그 위치(또는 팀 NAS)로 한 번 지정하세요. 지정한 위치는 업데이트 후에도 유지됩니다.

### <img src="assets/fileRay_Selim.png" width="28" align="center" alt=""> FileRay

사용자가 등록한 로컬 폴더의 파일명과 문서 본문을 인덱싱하여 필요한 업무 자료를 빠르게 검색하고 미리 볼 수 있는 Windows용 오프라인 문서 검색 프로그램입니다. 검색 데이터와 문서 정보는 사용자 PC에 저장되며 프로그램 사용 시 인터넷 연결이 필요하지 않습니다.

- 파일명 및 문서 본문 검색, 단어 중간에 있는 문자열도 검색
- 결과를 끝까지 이어서 불러오는 목록
- 등록 폴더와 하위 폴더 자동 인덱싱, 파일 추가·수정·삭제 자동 반영
- 파일 형식, 날짜 및 폴더 범위 검색, 결과 내 재검색(포함·제외, 여러 단계로 이어서)
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

## 업데이트 내역

Selim Tools로 배포하기 시작한 2026-09-27부터의 버전입니다. 새 버전을 위에 적었고, 버전을 누르면 그 릴리스 노트가 열립니다.

### Selim Tools

| 버전 | 날짜 | 바뀐 점 |
|---|---|---|
| [1.0.1](https://github.com/minsangOh/Selim-Tools/releases/tag/hub-v1.0.1) | 2026-09-28 | 설치형 프로그램을 업데이트할 때 사용자가 지운 바탕 화면 바로가기를 되살리지 않음 |
| [1.0.0](https://github.com/minsangOh/Selim-Tools/releases/tag/hub-v1.0.0) | 2026-09-27 | 첫 버전. 네 프로그램을 버튼 하나로 설치·업데이트·실행 |

### 작업지도서 자재 소요량

| 버전 | 날짜 | 바뀐 점 |
|---|---|---|
| [1.3.1](https://github.com/minsangOh/Selim-Tools/releases/tag/wim-v1.3.1) | 2026-09-27 | 폴더(ZIP) 대신 exe 하나로 배포 |

### CTQ 승인원 자동입력

| 버전 | 날짜 | 바뀐 점 |
|---|---|---|
| [1.6.0](https://github.com/minsangOh/Selim-Tools/releases/tag/ctq-v1.6.0) | 2026-10-06 | 제품별 DB 정보·경로 표시, 에어컨 DB 재구축(조합 207개 → 221개) |
| [1.5.1](https://github.com/minsangOh/Selim-Tools/releases/tag/ctq-v1.5.1) | 2026-09-30 | 에어컨 삽입부높이 시트: 도면을 원본 해상도로 더 크게 넣고, 빠지던 기준값(SPEC)을 채움 |
| [1.5.0](https://github.com/minsangOh/Selim-Tools/releases/tag/ctq-v1.5.0) | 2026-09-29 | 승인원 파일 끌어다 놓기, 다른 제품 DB에만 있는 터미널·와이어도 드롭다운에 표시 |
| [1.4.0](https://github.com/minsangOh/Selim-Tools/releases/tag/ctq-v1.4.0) | 2026-09-28 | 시트 선택, 백업 파일 없이 원본에 저장, 속도 개선, 와이어 → 터미널 드롭다운, DB 기본 위치를 팀 NAS로 |
| [1.3.0](https://github.com/minsangOh/Selim-Tools/releases/tag/ctq-v1.3.0) | 2026-09-27 | exe 아이콘·시작 화면·파일 속성 |

### FileRay

| 버전 | 날짜 | 바뀐 점 |
|---|---|---|
| [0.6.0](https://github.com/minsangOh/Selim-Tools/releases/tag/fileray-v0.6.0) | 2026-10-10 | 결과 내 검색을 여러 단계로 이어 가기 (Enter로 조건 고정, 포함·제외 섞기) |
| [0.5.0](https://github.com/minsangOh/Selim-Tools/releases/tag/fileray-v0.5.0) | 2026-10-10 | 영어 화면, Selim Tools 없이 스스로 업데이트 |
| [0.4.0](https://github.com/minsangOh/Selim-Tools/releases/tag/fileray-v0.4.0) | 2026-09-27 | 결과를 끝까지 이어서 불러오기, 단어 중간 문자열 검색, 엑셀 셀 주소, 결과 내 재검색 제외 모드, HWP 표 안 글자 등 검색 누락 수정 |

### Selim PDF Diff

| 버전 | 날짜 | 바뀐 점 |
|---|---|---|
| [2.1.1](https://github.com/minsangOh/Selim-Tools/releases/tag/pdfdiff-v2.1.1) | 2026-10-11 | 기능 변경 없음. 자동 업데이트 동작 확인용 |
| [2.1.0](https://github.com/minsangOh/Selim-Tools/releases/tag/pdfdiff-v2.1.0) | 2026-10-10 | 영어 화면, Selim Tools 없이 스스로 업데이트 |
| [2.0.2](https://github.com/minsangOh/Selim-Tools/releases/tag/pdfdiff-v2.0.2) | 2026-09-28 | 바뀐 부분 음영이 줄무늬로 보이던 문제 수정, 렌더링을 별도 프로세스로 옮겨 확대·축소 끊김 개선 |
| [2.0.1](https://github.com/minsangOh/Selim-Tools/releases/tag/pdfdiff-v2.0.1) | 2026-09-28 | 업데이트할 때 지난 버전의 파일을 지우고 새로 설치 |

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

## 전사 배포: FileRay·Selim PDF Diff

FileRay와 Selim PDF Diff는 Selim Tools 없이 각 프로그램의 설치 파일만 나눠 줘도 됩니다. 두 프로그램은 Selim Tools와 같은 [`manifest.json`](manifest.json)을 직접 확인해 스스로 업데이트합니다. 따라서 릴리스 한 번으로 두 트랙에 함께 반영됩니다.

| 트랙 | 쓰는 PC | 설치 | 업데이트 |
|---|---|---|---|
| 팀 | 작업지도서·CTQ까지 쓰는 PC | Selim Tools | Selim Tools에서 실행할 때 |
| 전사 | FileRay·Selim PDF Diff만 쓰는 PC | 각 프로그램의 설치 파일 | 프로그램이 스스로 |

- 설치 파일은 [전체 릴리스](https://github.com/minsangOh/Selim-Tools/releases)의 `fileray-v…`, `pdfdiff-v…`에 있습니다. 자동 업데이트는 FileRay 0.5.0, Selim PDF Diff 2.1.0부터 들어 있으므로, 그보다 예전 버전이 설치된 PC는 최신 설치 파일로 한 번 다시 설치합니다. 그 뒤로는 스스로 최신 버전을 받습니다. Selim Tools가 없는 PC에서 FileRay 0.5.0 → 0.6.0, Selim PDF Diff 2.1.0 → 2.1.1로 업데이트되는 것을 확인했습니다.
- 프로그램은 시작하고 잠시 뒤 새 버전이 있는지 확인합니다. 새 버전이 있으면 설치 파일을 받아 두었다가 프로그램을 닫을 때 조용히 설치합니다. 업데이트 버튼을 누르면 바로 설치하고 다시 시작합니다. 확인은 켤 때 한 번만 하므로, 새 버전이 나오기 전부터 켜 둔 프로그램은 다시 켜야 받습니다.
- 받은 설치 파일은 목록에 적힌 크기·SHA-256과 같을 때만 설치합니다. 목록과 설치 파일을 받기만 하고, 문서 내용이나 사용 기록은 보내지 않습니다.
- 인터넷에 연결되지 않으면 확인을 건너뛰고 설치된 버전을 그대로 씁니다. 회사 방화벽이 `raw.githubusercontent.com`, `github.com`, `release-assets.githubusercontent.com`(예전 주소 `objects.githubusercontent.com`)로 가는 HTTPS를 막으면 업데이트되지 않습니다.
- 화면 언어는 Windows 표시 언어를 따르고, 한국어가 아니면 영어로 표시합니다. FileRay는 설정 → 일반에서, Selim PDF Diff는 화면 오른쪽의 언어 버튼으로 바꿀 수 있습니다.

---

## 관리자용: 새 버전 배포

Selim Tools는 이 저장소 `master`의 [`manifest.json`](manifest.json)을 읽어 프로그램마다 최신 버전을 판단합니다. FileRay와 Selim PDF Diff도 같은 목록에서 자기 항목(`id`, `version`, `url`, `sha256`, `size`)을 읽어 스스로 업데이트합니다. 이미 배포된 프로그램이 계속 업데이트를 받을 수 있도록, 이 필드와 `schema: 1`은 바꾸지 않습니다. 원본 저장소에 정식 릴리스를 만들면 원본 저장소의 `.github/workflows/selim-tools.yml`이 이 저장소의 [`publish.yml`](.github/workflows/publish.yml)을 부르고, Selim-Tools 릴리스 생성부터 `manifest.json` 갱신·푸시까지 자동으로 처리합니다. 결과는 원본 저장소의 **Actions** 탭에서 볼 수 있습니다. 프리릴리스는 올리지 않습니다.

자동 실행이 실패했거나 지난 릴리스를 올릴 때는 원본 저장소의 **Actions → Selim Tools에 올리기 → Run workflow**에 태그를 넣어 실행합니다. 이 저장소에서 직접 실행해도 됩니다 (gh CLI 로그인 필요).

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

- 원본 릴리스에는 `.exe` 첨부 파일이 하나만 있어야 합니다. 설치형은 관리자 권한 없이 `/S`로 무인 설치되는 사용자 단위 NSIS여야 합니다. 이미 설치된 앱을 업데이트할 때는 `/UPDATE`도 함께 넘깁니다. FileRay 같은 Tauri 설치 파일은 이 옵션이 있으면 사용자가 지운 바로가기를 되살리지 않고, 이 옵션을 모르는 설치 파일은 무시합니다.
- FileRay와 Selim PDF Diff가 스스로 업데이트할 때도 같은 설치 파일을 `/S`로 실행합니다. 프로그램을 닫는 중에 실행하므로 설치 파일은 프로그램이 끝나기를 기다렸다가 덮어써야 합니다. 업데이트 버튼으로 실행할 때는 `/R`을 더 넘기며, 설치 파일은 설치를 마친 뒤 프로그램을 다시 실행해야 합니다. Tauri 설치 파일은 이 동작을 기본으로 지원하고, Selim PDF Diff는 설치 스크립트에서 처리합니다.
- 설치형은 설치 파일이 기록하는 버전(`DisplayVersion`)이 릴리스 태그와 같아야 합니다. 다르면 Selim Tools가 설치를 마친 뒤에도 옛 버전으로 보고 실행할 때마다 다시 설치합니다. 업데이트할 때 지난 버전의 파일을 지우는 것도 설치 파일이 합니다 (예: `_internal`을 비운 뒤 복사).
- 목록보다 낮거나 같은 버전은 올리지 않습니다. 같은 버전이 두 번 올라가거나 목록이 옛 버전으로 되돌아가지 않게 하기 위해서입니다.
- 앱 릴리스의 태그는 `<id>-v<버전>`입니다. Selim Tools 릴리스(`hub-v…`)만 **Latest**로 두어, 위의 "최신 릴리스" 링크가 늘 Selim Tools 설치 파일을 가리키게 합니다.
- `manifest.json`이 바뀌면 각 PC의 Selim Tools는 다음 실행이나 **새로 고침** 때 새 목록을 받습니다 (GitHub 캐시로 몇 분 늦을 수 있습니다).
- 자동 배포는 README를 고치지 않으므로, 배포한 뒤 [업데이트 내역](#업데이트-내역)에 한 줄을 더합니다.

### 자동 배포 설정

원본 저장소의 워크플로가 Selim-Tools에 릴리스를 만들고 푸시하려면 토큰이 필요합니다. 처음 한 번만 설정합니다.

1. GitHub **Settings → Developer settings → Personal access tokens → Fine-grained tokens**에서 토큰을 만듭니다. **Repository access**는 **Only select repositories**에서 `Selim-Tools` 하나만 고르고, **Permissions**는 **Contents: Read and write**를 줍니다.
2. 원본 저장소마다 이 토큰을 Actions 시크릿 `SELIM_TOOLS_TOKEN`으로 등록합니다: `gh secret set SELIM_TOOLS_TOKEN -R minsangOh/<원본 저장소>`

원본 저장소의 릴리스는 그 저장소의 워크플로 토큰으로 받으므로, 이 토큰에는 원본 저장소 권한을 주지 않습니다. 만료 기간을 두었다면 만료되기 전에 새 토큰을 같은 이름으로 다시 등록합니다.

### Selim Tools 빌드와 배포

```powershell
powershell -ExecutionPolicy Bypass -File hub\build.ps1   # 테스트 → 빌드 → hub\dist\installer\SelimTools-Setup-x.y.z.exe
python tools/publish.py hub --notes-file notes.md
```

버전은 `hub/main.py`의 `APP_VERSION` 하나로 관리합니다. 빌드에는 Python 3.13과 NSIS가 필요합니다 (NSIS를 설치하지 않았다면 Tauri가 받아 둔 NSIS를 씁니다).

### 프로그램 추가

`manifest.json`의 `apps`에 항목(`id`, `name`, `description`, `kind`, `exe`, `icon`, 설치형은 `uninstall_key`)을 넣고, `tools/publish.py`의 `SOURCES`에 원본 저장소를 적습니다. 원본 저장소에는 다른 원본 저장소의 `.github/workflows/selim-tools.yml`을 복사해 `app:`만 바꾸고, 시크릿 `SELIM_TOOLS_TOKEN`을 등록합니다. 그 뒤로는 릴리스할 때마다 자동으로 올라가고, 그 전에 만든 릴리스는 publish로 올립니다. `url`이 빈 항목은 Selim Tools에 나타나지 않으므로 먼저 커밋해도 됩니다. 아이콘은 `assets/`에 둡니다.
