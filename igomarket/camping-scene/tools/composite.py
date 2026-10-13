#!/usr/bin/env python3
"""1단계 실사 이미지의 상품 영역만 2단계 만화 이미지 위에 다시 얹는다.

이미지 생성 AI에 "상품만 빼고 만화로 바꿔줘"라고 해도 상품까지 조금씩 그림체가
바뀌는 일이 잦다. 그래서 상품 픽셀은 1단계 실사 원본에서 그대로 가져와 합성한다.
두 이미지는 같은 구도여야 한다(2단계는 1단계를 '편집'해서 만든 결과).

상품 영역은 둘 중 하나로 지정한다.
  - scene.js 의 polygon(% 좌표). index.html [영역 편집]으로 찍은 값.
  - --masks-dir 폴더의 <상품id>.png 흑백 마스크(흰색=상품). 포토샵/누끼 도구로 딴 것.
    해당 파일이 있으면 polygon보다 우선한다. 경계가 훨씬 정확하다.

결과물
  final.png        합성 결과 (사이트에 올릴 이미지)
  mask.png         합성에 쓴 상품 마스크
  check.png        만화 이미지 위에 상품 영역을 붉게 표시한 검수용 이미지
  그리고 마스크에서 다시 계산한 핫스팟/클릭 범위 표를 출력한다.

예)
  python3 tools/composite.py --photo step1-photo.png --cartoon step2-cartoon.png
  python3 tools/composite.py --photo p.png --cartoon c.png --masks-dir masks --feather 4
"""
import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent.parent


def load_scene(path):
    text = Path(path).read_text(encoding="utf-8")
    # scene.js 는 `window.SCENE_DATA = {...};` 형태. 앞뒤 JS를 걷어내고 JSON만 읽는다.
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        sys.exit(f"{path}: 장면 데이터를 찾지 못함")
    return json.loads(m.group(0))


def product_mask(product, size, masks_dir):
    w, h = size
    if masks_dir:
        f = Path(masks_dir) / f"{product['id']}.png"
        if f.exists():
            m = Image.open(f).convert("L")
            if m.size != size:
                m = m.resize(size, Image.LANCZOS)
            return m.point(lambda v: 255 if v >= 128 else 0), "마스크 파일"
    pts = [(x / 100 * w, y / 100 * h) for x, y in product["polygon"]]
    m = Image.new("L", size, 0)
    if len(pts) >= 3:
        ImageDraw.Draw(m).polygon(pts, fill=255)
    return m, "polygon"


def centroid(mask):
    # 마스크 무게중심(% 좌표). 핫스팟 후보로 쓰되 최종 위치는 사람이 확인한다.
    small = mask.copy()
    small.thumbnail((400, 400))
    sw, sh = small.size
    px = small.load()
    sx = sy = n = 0
    for y in range(sh):
        for x in range(sw):
            if px[x, y]:
                sx += x
                sy += y
                n += 1
    if not n:
        return None
    return round((sx / n + 0.5) / sw * 100, 1), round((sy / n + 0.5) / sh * 100, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--photo", required=True, help="1단계: 장면 전체 실사 이미지")
    ap.add_argument("--cartoon", required=True, help="2단계: 상품 외 만화화한 이미지 (같은 구도)")
    ap.add_argument("--scene", default=str(HERE / "scene.js"), help="장면 데이터 (기본: scene.js)")
    ap.add_argument("--masks-dir", help="<상품id>.png 흑백 마스크 폴더 (선택)")
    ap.add_argument("--out-dir", default=str(HERE), help="결과 저장 폴더 (기본: camping-scene/)")
    ap.add_argument("--grow", type=int, default=2, help="마스크를 바깥으로 넓힐 픽셀 (기본 2)")
    ap.add_argument("--feather", type=float, default=3, help="경계 흐림 반경 픽셀 (기본 3)")
    args = ap.parse_args()

    scene = load_scene(args.scene)
    photo = Image.open(args.photo).convert("RGB")
    cartoon = Image.open(args.cartoon).convert("RGB")
    size = photo.size
    if cartoon.size != size:
        ratio_p, ratio_c = size[0] / size[1], cartoon.size[0] / cartoon.size[1]
        if abs(ratio_p - ratio_c) > 0.01:
            sys.exit(f"비율이 다름: 실사 {photo.size}, 만화 {cartoon.size}. 같은 구도의 편집 결과인지 확인하세요.")
        print(f"알림: 만화 이미지 {cartoon.size} → {size} 로 맞춤")
        cartoon = cartoon.resize(size, Image.LANCZOS)

    mask = Image.new("L", size, 0)
    rows = []
    for p in scene["products"]:
        m, src = product_mask(p, size, args.masks_dir)
        if args.grow > 0:
            m = m.filter(ImageFilter.MaxFilter(args.grow * 2 + 1))
        mask = ImageChops.lighter(mask, m)
        bb = m.getbbox()
        c = centroid(m)
        rows.append((p, src, bb, c))

    soft = mask.filter(ImageFilter.GaussianBlur(args.feather)) if args.feather > 0 else mask
    final = Image.composite(photo, cartoon, soft)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    final.save(out / "final.png")
    mask.save(out / "mask.png")
    red = Image.new("RGB", size, (230, 40, 40))
    check = Image.composite(Image.blend(cartoon, red, 0.45), cartoon, mask)
    check.save(out / "check.png")

    w, h = size
    print(f"\n저장: {out/'final.png'}, {out/'mask.png'}, {out/'check.png'}  ({w}x{h})\n")
    print("| # | 상품군 | 영역 출처 | 무게중심 (x, y %) | 클릭 범위 bbox (x, y, 가로, 세로 %) | scene.js 핫스팟 |")
    print("|---|---|---|---|---|---|")
    for p, src, bb, c in rows:
        if not bb:
            print(f"| {p['no']} | {p['name']} | {src} | (영역 없음) | - | {p['hotspot']} |")
            continue
        x0, y0, x1, y1 = bb
        box = f"{x0/w*100:.1f}, {y0/h*100:.1f}, {(x1-x0)/w*100:.1f}, {(y1-y0)/h*100:.1f}"
        print(f"| {p['no']} | {p['name']} | {src} | {c[0]}, {c[1]} | {box} | {p['hotspot']} |")
    print("\n※ 수치는 마스크 기준 계산값. 핫스팟은 상품 위 눈에 잘 띄는 곳으로 사람이 최종 확인할 것.")


if __name__ == "__main__":
    main()
