"""원본 저장소의 릴리스를 Selim-Tools 릴리스로 올리고 manifest.json을 갱신한다.

    python tools/publish.py ctq                          # 원본 저장소의 Latest 릴리스
    python tools/publish.py fileray --tag v0.4.0         # 태그 지정
    python tools/publish.py hub --notes-file notes.md    # hub\\build.ps1로 만든 허브 설치 파일

순서: 파일 준비 → 해시 확인 → Selim-Tools 릴리스 생성 → manifest.json 갱신 → 커밋·푸시.
manifest는 첨부 파일이 올라간 뒤에만 바뀌므로, 허브가 아직 없는 파일을 가리키는 때는 없다.
gh CLI 로그인이 필요하다.
원본 저장소에 정식 릴리스를 만들면 GitHub Actions(.github/workflows/publish.yml)가 이 스크립트를 자동으로 실행한다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "minsangOh/Selim-Tools"
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
# 앱 id → 릴리스를 만드는 원본 저장소. 릴리스 첨부 파일 중 .exe 하나를 올린다
SOURCES = {
    "wim": "minsangOh/work-instruction-materials-gui",
    "ctq": "minsangOh/CTQ_DB_Tool",
    "fileray": "minsangOh/fileRay_Selim",
    "pdfdiff": "minsangOh/Diff_PDF",
}


def run(*args: str, token: str | None = None) -> str:
    env = {**os.environ, "GH_TOKEN": token} if token else None
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env)
    if result.returncode != 0:
        sys.exit(f"실패: {' '.join(args)}\n{result.stderr.strip()}")
    return result.stdout


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fp:
        while chunk := fp.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def version_key(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", text))


def source_release(app_id: str, tag: str | None, folder: Path) -> tuple[str, Path, str, str]:
    """원본 릴리스의 exe를 받는다. (버전, 파일, 릴리스 노트, GitHub에 기록된 sha256)"""
    repo = SOURCES[app_id]
    # GitHub Actions에서는 원본 저장소가 넘겨준 토큰으로 받는다. 원본 저장소는 비공개라 Selim-Tools용 토큰으로는 읽지 못한다
    token = os.environ.get("SOURCE_GH_TOKEN")
    info = json.loads(run("gh", "api", f"repos/{repo}/releases/" + (f"tags/{tag}" if tag else "latest"), token=token))
    exes = [asset for asset in info["assets"] if asset["name"].lower().endswith(".exe")]
    if len(exes) != 1:
        sys.exit(f"{repo} {info['tag_name']}: exe 첨부 파일이 {len(exes)}개입니다. 하나여야 합니다.")
    asset = exes[0]
    run("gh", "release", "download", info["tag_name"], "-R", repo, "-p", asset["name"], "-D", str(folder), token=token)
    return info["tag_name"].lstrip("v"), folder / asset["name"], info["body"] or "", asset.get("digest") or ""


def hub_installer() -> tuple[str, Path]:
    source = (ROOT / "hub" / "main.py").read_text(encoding="utf-8")
    version = re.search(r'^APP_VERSION = "(\d+\.\d+\.\d+)"$', source, re.M).group(1)
    path = ROOT / "hub" / "dist" / "installer" / f"SelimTools-Setup-{version}.exe"
    if not path.exists():
        sys.exit(f"{path.relative_to(ROOT)}이(가) 없습니다. 먼저 hub\\build.ps1을 실행하세요.")
    return version, path


def main() -> None:
    parser = argparse.ArgumentParser(description="원본 릴리스를 Selim-Tools에 올리고 manifest.json을 갱신합니다.")
    parser.add_argument("app", choices=[*SOURCES, "hub"])
    parser.add_argument("--tag", help="원본 릴리스 태그 (기본: 원본 저장소의 Latest)")
    parser.add_argument("--notes-file", type=Path, help="릴리스 노트 파일 (기본: 원본 릴리스의 노트)")
    parser.add_argument("--yes", action="store_true", help="확인 질문 없이 진행")
    args = parser.parse_args()

    if run("git", "status", "--porcelain", "--", "manifest.json").strip():
        sys.exit("manifest.json에 커밋하지 않은 변경이 있습니다. 먼저 정리하세요.")
    run("git", "pull", "--ff-only")
    branch = run("git", "rev-parse", "--abbrev-ref", "HEAD").strip()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entry = manifest["hub"] if args.app == "hub" else next(item for item in manifest["apps"] if item["id"] == args.app)

    with tempfile.TemporaryDirectory() as folder:
        if args.app == "hub":
            version, path = hub_installer()
            notes, expected = "", ""
        else:
            version, path, notes, expected = source_release(args.app, args.tag, Path(folder))
        # 같은 버전을 다시 올리거나 목록을 옛 버전으로 되돌리지 않는다
        if entry["version"] and version_key(version) <= version_key(entry["version"]):
            sys.exit(f"{entry['name']}: 목록에 이미 v{entry['version']}이 있어 v{version}은 올리지 않습니다.")
        digest = sha256(path)
        if expected and expected != f"sha256:{digest}":
            sys.exit(f"{path.name}: 받은 파일의 해시가 GitHub에 기록된 값과 다릅니다.")
        if args.notes_file:
            notes = args.notes_file.read_text(encoding="utf-8")
        tag = f"{args.app}-v{version}"
        size = path.stat().st_size
        print(f"{entry['name']} v{version}: {path.name} ({size:,} bytes)")
        print(f"→ {REPO}에 릴리스 {tag}를 공개하고 manifest.json을 {branch} 브랜치에 푸시합니다.")
        if branch != "master":
            print("  master가 아니므로 허브에는 master에 머지한 뒤에 반영됩니다.")
        if not args.yes and input("계속할까요? [y/N] ").strip().lower() != "y":
            sys.exit("취소했습니다.")

        notes_file = Path(folder) / "notes.md"
        notes_file.write_text(notes or f"{entry['name']} v{version}", encoding="utf-8")
        # 허브 릴리스만 Latest로 둔다. README의 '최신 릴리스' 링크가 늘 허브 설치 파일을 가리키게 하기 위해서다
        run("gh", "release", "create", tag, str(path), "-R", REPO, "--title", f"{entry['name']} v{version}",
            "--notes-file", str(notes_file), f"--latest={'true' if args.app == 'hub' else 'false'}")

    release = json.loads(run("gh", "api", f"repos/{REPO}/releases/tags/{tag}"))
    entry.update(version=version, url=release["assets"][0]["browser_download_url"], sha256=digest, size=size,
                 notes=release["html_url"])
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    run("git", "add", "manifest.json")
    run("git", "commit", "-m", f"Publish {entry['name']} v{version}")
    # 다른 원본 저장소의 배포가 먼저 푸시했으면 그 위로 옮겨 다시 푸시한다
    for _ in range(3):
        if subprocess.run(["git", "push"], cwd=ROOT).returncode == 0:
            break
        run("git", "pull", "--rebase")
    else:
        sys.exit("manifest.json을 푸시하지 못했습니다.")
    print(f"완료: {release['html_url']}")


if __name__ == "__main__":
    main()
