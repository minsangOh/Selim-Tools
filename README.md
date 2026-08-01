# Selim Tools

업무 효율화를 위해 개발한 Windows 데스크톱 프로그램의 공식 배포 저장소입니다.

설치 파일과 사용자 매뉴얼은 각 프로그램의 GitHub Release에서 다운로드할 수 있습니다.


---

## 프로그램 다운로드

<table>
  <tr>
    <td align="center" width="140">
      <img src="assets/Diff_PDF.ico" width="96" alt="Selim PDF Diff 아이콘">
    </td>
    <td>
      <h3>Selim PDF Diff</h3>
      <p>두 PDF 도면을 비교하여 변경된 영역을 자동으로 표시합니다.</p>
      <p><strong>최신 버전:</strong> v2.0.0</p>
      <a href="https://github.com/minsangOh/Selim-Tools/releases/tag/v2.0.0">
        다운로드 및 사용자 매뉴얼
      </a>
    </td>
  </tr>
  <tr>
    <td align="center" width="140">
      <img src="assets/fileRay_Selim.png" width="96" alt="Selim FileRay 아이콘">
    </td>
    <td>
      <h3>Selim FileRay</h3>
      <p>로컬 업무 문서의 파일명과 본문을 빠르게 검색하고 관리합니다.</p>
      <p><strong>최신 버전:</strong> v0.0.1</p>
      <a href="https://github.com/minsangOh/Selim-Tools/releases/tag/v0.0.1">
        다운로드 및 사용자 매뉴얼
      </a>
    </td>
  </tr>
</table>

[전체 릴리스 보기](https://github.com/minsangOh/Selim-Tools/releases)

---

## <img src="assets/Diff_PDF.ico" width="36" align="center" alt=""> Selim PDF Diff

두 개의 PDF 도면을 동일한 페이지와 좌표를 기준으로 비교하여 실제로 변경된 부분을 표시하는 Windows 데스크톱 프로그램입니다.

도면 Revision 변경 검토 시 변경 위치를 빠르게 확인할 수 있도록 개발되었습니다.

### 주요 기능

- 두 PDF 도면의 동일 좌표 기준 비교
- 변경 영역 자동 검출
- 변경 위치 반투명 Highlight 표시
- 좌우 Highlight 독립 표시 및 숨김
- Highlight 투명도 조절
- PDF 파일 Drag & Drop
- 페이지 이동 및 확대·축소
- 좌우 화면 위치 동기화
- 동일 PDF 좌표의 커서 위치 동기화
- 현재 비교 화면 클립보드 복사
- 고해상도 디스플레이 지원

### 최신 버전

**Version v2.0.0**

[Selim PDF Diff v2.0.0 다운로드](https://github.com/minsangOh/Selim-Tools/releases/tag/v2.0.0)

### 지원 환경

- Windows 10
- Windows 11
- Windows 64-bit

---

## <img src="assets/fileRay_Selim.png" width="36" align="center" alt=""> Selim FileRay

사용자가 등록한 로컬 폴더의 파일명과 문서 본문을 인덱싱하여 필요한 업무 자료를 빠르게 검색하고 미리 볼 수 있는 Windows용 오프라인 문서 검색 프로그램입니다.

검색 데이터와 문서 정보는 사용자 PC에 저장되며 프로그램 사용 시 인터넷 연결이 필요하지 않습니다.

### 주요 기능

- 파일명 및 문서 본문 검색
- 등록 폴더와 하위 폴더 자동 인덱싱
- 파일 추가·수정·삭제 자동 반영
- 여러 검색 폴더 관리
- 파일 형식, 날짜 및 폴더 범위 검색
- 검색 결과 정렬 및 결과 내 재검색
- 문서 내용 미리보기
- 검색어 Highlight 표시
- 원본 파일 열기
- 탐색기에서 파일 위치 열기
- 파일 경로 복사
- 문서 북마크, 메모 및 사용자 태그
- 중복 파일 탐지
- 검색 결과 CSV 내보내기
- 이미지 및 스캔 PDF 오프라인 OCR 지원

### 지원 파일 형식

| 분류 | 지원 형식 |
|---|---|
| 한글 문서 | `.hwp`, `.hwpx` |
| Microsoft Office | `.docx`, `.pptx`, `.xls`, `.xlsx` |
| PDF | `.pdf` |
| 텍스트 | `.txt`, `.md` |
| 이메일 | `.eml` |
| 이미지 | `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tif`, `.tiff` |

이미지와 스캔 PDF의 문자 검색은 OCR 기능을 활성화한 경우 지원됩니다.

### 최신 버전

**Version v0.0.1**

[Selim FileRay v0.0.1 다운로드](https://github.com/minsangOh/Selim-Tools/releases/tag/v0.0.1)

### 지원 환경

- Windows 10
- Windows 11
- Windows 64-bit

---

## 설치 방법

1. 위의 **프로그램 다운로드**에서 사용할 프로그램의 릴리스 페이지를 엽니다.
2. 릴리스 페이지 하단의 **Assets** 항목을 펼칩니다.
3. 프로그램 설치 파일을 다운로드합니다.
4. 다운로드한 설치 파일을 실행합니다.
5. 설치가 완료되면 시작 메뉴 또는 바탕화면 바로가기에서 프로그램을 실행합니다.

자세한 사용 방법은 각 릴리스에 첨부된 사용자 매뉴얼을 참고해 주세요.

> 설치 파일이 코드 서명되지 않은 경우 처음 실행할 때 Windows SmartScreen 경고가 표시될 수 있습니다. 파일의 프로그램명과 버전을 확인한 후 실행해 주세요.

---

## 업데이트 방법

새로운 버전이 배포되면 해당 프로그램의 최신 릴리스에서 설치 파일을 다운로드하여 설치합니다.

프로그램별 버전은 독립적으로 관리되므로 다운로드 전에 프로그램명과 버전을 확인해 주세요.

이전 버전이 필요한 경우 [전체 릴리스](https://github.com/minsangOh/Selim-Tools/releases)에서 다운로드할 수 있습니다.

---

## 릴리스 안내

이 저장소에서는 여러 프로그램의 설치 파일과 사용자 매뉴얼을 함께 관리합니다.

GitHub의 **Latest** 표시는 저장소 전체를 기준으로 하나만 제공되므로 프로그램별 최신 버전은 README 상단의 **프로그램 다운로드**에서 확인해 주세요.

각 릴리스의 제목은 다음 형식으로 관리합니다.

```text
Selim PDF Diff v2.0.0
Selim FileRay v0.0.1
