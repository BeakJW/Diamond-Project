from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
OUT  = ROOT / "notebooks" / "Master_final.ipynb"  # 결과 파일(새 파일)

SOURCES = [
    ("Diamond_final", ROOT / "notebooks" / "Diamond_final.ipynb"),
    ("원본데이터", ROOT / "notebooks" / "jinwoo" / "원본데이터.ipynb"),
    ("전처리", ROOT / "notebooks" / "jinwoo" / "전처리.ipynb"),
    ("교효작용", ROOT / "notebooks" / "seongyu" / "교효작용.ipynb"),
    ("1사분위수_작업", ROOT / "notebooks" / "seongyu" / "1사분위수_작업.ipynb"),
    ("q2", ROOT / "notebooks" / "jinwoo" / "q2.ipynb"),
    ("work1", ROOT / "notebooks" / "jiyoung" / "work1.ipynb"),
    ("명목추가", ROOT / "notebooks" / "sooyoung" / "명목추가.ipynb"),
]

def strip_outputs(nb):
    # diff 깔끔하게: 출력/실행카운트 제거
    for cell in nb.cells:
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    return nb

def main():
    new_nb = nbf.v4.new_notebook()
    new_nb.cells.append(
        nbf.v4.new_markdown_cell("# Master Final Notebook\n\n(자동 생성 파일)\n")
    )

    first_meta = None

    for title, path in SOURCES:
        if not path.exists():
            raise FileNotFoundError(f"Missing source notebook: {path}")

        nb = nbf.read(path, as_version=4)
        if first_meta is None:
            first_meta = nb.get("metadata", {})

        nb = strip_outputs(nb)

        rel = path.relative_to(ROOT).as_posix()
        new_nb.cells.append(nbf.v4.new_markdown_cell(f"\n---\n\n# {title}\n\n**{rel}**\n"))
        new_nb.cells.extend(nb.cells)

    if first_meta:
        new_nb["metadata"] = first_meta

    OUT.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(new_nb, OUT)
    print(f"✅ Wrote: {OUT}")

if __name__ == "__main__":
    main()
