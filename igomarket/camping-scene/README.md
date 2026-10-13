# 아이고마켓 · 상황형 상품 진열 시범 장면 — "도착 1시간째, 아빠만 아직 설치 중"

> **상태: 구상·검증 단계.** 실제 시안 이미지는 **아직 생성하지 않았다** (이 작업 환경에 이미지 생성 도구가 없음).
> `layout-guide.png`는 구도를 잡기 위한 가이드 그림이지 시안이 아니다.

## 0. 이번 스타일 원칙 (인계 문서에서 바뀐 점)

| 구분 | 인계 문서(초안) | **이번 기준** |
|---|---|---|
| 상품 5개 | 선명한 컬러 | **실사 사진처럼** (재질·광택·질감이 사진 수준) |
| 나머지 전부 (인물·배경·소품) | 흑백/저채도 | **흑백(회색조) 만화 일러스트, 외곽선(테두리) 없는 면 위주 그림체** |
| 구분 방식 | 색 대비 | **컬러 실사 상품 vs 흑백 만화 배경** — 색과 질감 두 가지로 동시에 구분 |

> 스타일 견본: 사용자가 보여준 '호숫가 낚시 캠핑' 이미지 (흑백 만화 인물·풍경 + 컬러 실사 아이스박스·의자·낚싯대·랜턴·태클박스). 단, 견본처럼 **핫스팟 동그라미를 그림에 그려 넣지는 않는다** (웹 UI 레이어로 얹음).

"테두리 없는 만화" = 검은 윤곽선 없이 색면·명암 덩어리로만 형태를 만드는 플랫/페인터리 일러스트 (그림책·모바일 게임 배경 같은 톤). 웹툰처럼 선을 따는 그림체가 아니다.

## 1. 장면 기획

**상황:** 초저녁 캠핑장. 도착한 지 한 시간째인데 텐트는 겨우 섰고, 아빠는 아직 마지막 팩을 박느라 땀을 흘린다. 엄마와 아이는 이미 돗자리에 앉아 과자를 먹으며 아빠를 가리키고 웃는다. 랜턴 옆의 접이식 의자는 비어 있다. 아빠 자리다. 화로대에는 장작만 올려놨고 불은 아직 못 붙였다.

**웃음 포인트:** 아빠 혼자만 분주하다. 조롱이 아니라 "우리 집 얘기네" 하는 공감을 노린다. 글 없이 행동만으로 읽혀야 한다.

### 상품군 5개 (실사로 그릴 대상)

| # | 상품군 | 위치 | 이 위치인 이유 | 클릭 후 목적지 (임시) |
|---|---|---|---|---|
| 1 | 텐트 | 중경 좌측, 설치 완료 | 가장 큰 상품. 장면의 무대 역할. 문이 열려 있어 크기 감이 잡힘 | `category:tent` |
| 2 | 접이식 캠핑 의자 | 전경 우측, **비어 있음** | "아빠 자리" 개그의 핵심. 사람이 안 앉아 있어 의자 전체 형태가 보임 | `category:camping-chair` |
| 3 | 아이스박스 | 전경 좌측 바닥 | 가장 가까워서 크기가 가늠됨 (인계 문서의 "크기 비교" 흐름과 연결) | `category:cooler` |
| 4 | 캠핑 랜턴 | 우측 랜턴 걸이에 매달림 | 해 지는 시간이라 켜져 있는 게 자연스러움. 의자 위를 비추는 위치 | `category:lantern` |
| 5 | 화로대 | 전경 중앙, 장작 옆 | 저녁 준비의 다음 단계. 불을 안 붙여 형태가 그대로 보임 | `category:fire-pit` |

**일부러 상품에서 뺀 것:** 돗자리, 장작, 랜턴 걸이 폴, 망치, 인물의 옷, 먼 이웃 텐트. 이것들은 전부 일러스트로 처리한다. 장면 안에 의자는 **하나만** 둔다. 같은 종류 물건이 실사와 만화로 섞이면 무엇을 눌러야 하는지 헷갈린다.

**사람과 상품을 겹치지 않는다:** 누가 상품을 들거나 그 위에 앉으면 실사/만화 경계가 손이나 몸을 지나가게 되고, 합성 경계가 지저분해진다. 이번 시안에서는 손이 닿는 장면도 피했다.

## 2. 제작 순서 (3단계)

```
① 실사 장면 생성 ──▶ ② 같은 이미지를 '상품 빼고' 만화화 ──▶ ③ 상품 영역만 ① 원본 픽셀로 되돌려 합성
   (구도·광원·크기 확정)      (테두리 없는 일러스트)              (tools/composite.py)
```

**왜 이 순서인가:** 처음부터 "상품만 실사, 나머지는 만화"로 한 번에 그리게 하면 상품이 스티커처럼 떠 보이고 광원·그림자·크기가 어긋나기 쉽다. 실사로 먼저 그리면 한 장면 안에서 투시·조명·접지가 맞춰진다. 그 상태에서 나머지만 그림체를 바꾸면 상품이 장면에 자연스럽게 붙는다.

**③이 필요한 이유:** ② 단계에서 "상품은 그대로 둬"라고 지시해도 생성 AI는 상품까지 조금씩 바꾼다 (질감이 뭉개지거나 형태가 살짝 변한다). 그래서 상품 영역은 ① 원본에서 픽셀째 가져와 덮어쓴다.

### ① 실사 장면 프롬프트 (데스크톱 16:9)

`layout-guide.png`를 **구도 참고 이미지**로 같이 첨부하면 배치가 훨씬 잘 맞는다. (가이드 그림에는 글자가 없다.)

**English (권장: 이미지 모델은 영어 지시를 더 정확히 따름)**

> Photorealistic wide 16:9 photograph of a realistic Korean family campsite at early dusk, soft warm sunset light from the right, gentle blue hour sky. Use the attached layout image only for composition and object placement, not for style.
> Scene: a fully pitched olive-green dome tent (mid-ground, left of center, door open). To the right of the tent a father kneels and hammers the last tent peg into the ground, sweating, focused. In the foreground center-right, a mother and a young child sit on a beige picnic mat eating snacks; the mother points at the father and laughs. An **empty** navy-blue folding camping chair stands in the right foreground, the father's unused seat. Beside it, an orange LED camping lantern hangs from a thin black lantern pole, switched on. In the left foreground on the gravel ground sits a teal hard-shell cooler box with a white lid, lid closed. In the center foreground, a copper-bronze camping fire pit on legs, with a few logs placed on it but no fire yet, next to a small stack of firewood.
> Camera at standing eye height, slightly looking down, 35mm lens, everything in focus. Consistent perspective and shadows, realistic relative sizes (chair seat at knee height of an adult, cooler about knee height). No person touches or covers any of these five objects: tent, folding chair, cooler, lantern, fire pit. Each of the five objects is fully visible with clear empty space around it. Keep the top 18% of the frame as open sky (space for a web title).
> No text, no logos, no brand names, no labels, no watermark, no price tags.

**한국어 (참고용)**

> 초저녁 한국의 현실적인 가족 캠핑장을 찍은 사진, 가로 16:9. 오른쪽에서 들어오는 따뜻한 노을빛. 첨부한 배치 이미지는 구도와 물건 위치만 참고하고 그림체는 따르지 않는다. 중경 왼쪽에 문이 열린 올리브색 돔 텐트가 설치되어 있고, 그 오른쪽에서 아빠가 무릎을 꿇고 땀을 흘리며 마지막 팩을 망치로 박는다. 전경 가운데 오른쪽 돗자리에서 엄마와 아이가 과자를 먹고, 엄마는 아빠를 가리키며 웃는다. 오른쪽 전경에는 **아무도 앉지 않은** 남색 접이식 캠핑 의자, 그 옆 랜턴 걸이에 켜진 주황색 LED 랜턴. 왼쪽 전경 자갈 바닥에 흰 뚜껑의 청록색 하드 아이스박스(닫힘). 가운데 전경에 장작만 올린, 불을 아직 붙이지 않은 구릿빛 화로대와 옆의 작은 장작 더미. 서서 보는 눈높이, 살짝 내려다보는 35mm 시점. 원근·그림자·크기 일관. 사람은 상품 5개(텐트·의자·아이스박스·랜턴·화로대) 어느 것도 만지거나 가리지 않는다. 상단 18%는 하늘 여백. 글자·로고·상표·가격표·워터마크 없음.

**네거티브:** hotspot circles, glowing dots, UI markers, partially colored background objects, text, letters, logo, brand, watermark, price tag, UI button, extra chairs, second cooler, people sitting on the chair, hands touching products, distorted hands, extra fingers, floating objects, wrong shadows, oversized lantern, objects intersecting, cluttered background, advertisement poster look.

### ② 만화화 편집 프롬프트 (① 결과를 입력으로)

가능하면 **마스크 기반 편집(인페인팅)**을 쓴다. 상품 5개를 보호 영역으로 칠하고 나머지만 다시 그리게 한다. 마스크 기능이 없으면 아래 문장으로 지시만 한다. 어느 쪽이든 ③에서 상품을 되돌린다.

> Edit this exact image. Keep the composition, camera, every object's position, size and silhouette, and the lighting direction exactly the same. **Do not change these five objects at all; keep them photorealistic: the olive dome tent, the navy folding chair, the teal cooler box, the orange hanging lantern, the copper fire pit.**
> Redraw everything else (sky, mountains, trees, ground, picnic mat, firewood, lantern pole, and all three people) as a **soft flat painted illustration with no outlines**: no black line art, no contour strokes, shapes defined only by flat color areas and soft shading, like a modern picture-book or cozy game background. Render all of it in **black-and-white grayscale** (no color at all) so only the five photorealistic color objects stand out. Friendly, simple, expressive faces with no line art. No text.

한국어 요지: *같은 이미지를 편집. 구도·위치·크기·윤곽·빛 방향은 그대로. 텐트·의자·아이스박스·랜턴·화로대 5개는 절대 바꾸지 말고 실사로 유지. 나머지(하늘·산·나무·바닥·돗자리·장작·폴·인물 3명)는 **외곽선 없는** 면 위주의 부드러운 일러스트로. 검은 선 따기 금지. 전부 **흑백(회색조)**으로, 컬러는 상품 5개에만.* 그림 안에 동그라미·점·화살표 같은 클릭 표시를 그리지 않는다.

### ③ 합성 (`tools/composite.py`)

```bash
# 1) 대략 영역(scene.js polygon)으로 합성
python3 tools/composite.py --photo step1-photo.png --cartoon step2-cartoon.png

# 2) 권장: 상품별 정밀 마스크(흰색=상품)를 masks/<id>.png 로 따서 사용
#    id: tent, camping-chair, cooler, lantern, fire-pit
python3 tools/composite.py --photo step1-photo.png --cartoon step2-cartoon.png --masks-dir masks
```

결과로 `final.png`(사이트용), `mask.png`, `check.png`(검수용: 상품 영역을 붉게 표시)가 나오고, 마스크에서 다시 계산한 핫스팟·클릭 범위 표가 출력된다.

- polygon은 클릭 영역으로는 충분하지만 합성 마스크로 쓰기에는 거칠다. 상품 주변 바닥이 실사로 남아 후광처럼 보인다. **최종 합성은 정밀 마스크로 한다.** (누끼 도구, 포토샵 '피사체 선택', SAM 등)
- ②에서 구도가 조금이라도 밀리면 경계가 어긋난다. `check.png`에서 붉은 영역이 만화 속 물체와 정확히 겹치는지 확인한다. 어긋나면 ②를 다시 생성한다.
- 실사 상품의 그림자는 만화 바닥 위에 있으므로 일러스트 그림자로 남는다. 상품 마스크에 접지 그림자를 넣을지는 시안을 보고 정한다.

## 3. 웹 인터랙션 레이어 (`index.html`)

로컬에서 `index.html`을 바로 열면 된다 (서버 불필요). `final.png`가 없으면 구도 가이드를 대신 보여준다.

- **이미지에 굽지 않는 것:** 제목, 안내 문구("실물 사진처럼 보이는 물건을 눌러보세요"), 핫스팟 점, 말풍선, 버튼. 전부 HTML 레이어라서 문구를 바꾸기 쉽다.
- **클릭 영역:** 핫스팟 점만이 아니라 **상품 모양 polygon 전체**가 눌린다. 점 버튼 자체도 44px 터치 영역을 갖는다 (랜턴처럼 작은 상품 대비).
- **동작:** 마우스를 올리면 말풍선이 뜨고, 터치하면 말풍선과 "비교 보러 가기" 버튼이 뜬다. 버튼을 누르면 상품군 화면으로 간다. 지금은 임시 식별자만 표시한다.
- **접근성:** 핫스팟은 실제 `<button>`이라 Tab 키로 이동할 수 있고 aria-label이 있다. Esc로 닫는다. '움직임 줄이기' 설정에서는 맥동 없이 고정 링만 보인다.
- **좌표 검수:** [생성 이미지 불러오기]로 실제 시안을 올리고 [영역 편집]에서 상품 외곽과 핫스팟을 다시 찍는다. [검수 완료로 표시]를 누르고 [scene.js 저장]으로 내려받아 덮어쓴다. 같은 `scene.js`를 `composite.py`도 읽는다.
- 현재 `scene.js` 좌표는 **구도 가이드 기준 추정치이며 전부 "검수 필요"** 상태다.

## 4. 모바일

16:9를 390px 폭으로 줄이면 상품 5개의 터치 영역이 서로 붙고 제목이 그림을 가린다. 프로토타입에서도 확인했다. 그래서 **세로 4:5 전용 구성**을 따로 만든다.

- 위쪽: 텐트(중앙) + 랜턴(우상단)
- 가운데: 아빠(텐트 오른쪽) / 엄마·아이 돗자리
- 아래: 아이스박스(좌하단), 화로대(하단 중앙), 빈 의자(우하단)
- 제목은 이미지 위가 아니라 이미지 **바로 위 HTML 영역**에 둔다.
- 데스크톱과 같은 ①→②→③ 과정을 거친다. 좌표는 `scene.js`를 하나 더 둬서 따로 관리한다.

①번 프롬프트에서 `wide 16:9`를 `vertical 4:5`로 바꾸고 위 배치를 문장으로 넣으면 된다. 상단 여백 문장은 뺀다.

## 5. 자체 점검 (실제 시안이 나오면 다시 확인할 항목)

- [ ] 실사로 보이는 물건이 정확히 5개이고, 5개 모두 클릭 대상인가?
- [ ] 실사 물건이 무엇인지 바로 알아볼 수 있는가? (실사라서 오히려 더 잘 보여야 한다)
- [ ] 만화 부분에 외곽선이 생기지 않았는가? (생성 AI가 자주 선을 넣는다)
- [ ] 실사와 만화의 경계에 후광·계단 현상이 없는가? (`check.png` / `--feather` 조정)
- [ ] 인물이 상품을 가리거나 만지지 않는가?
- [ ] 아이스박스·의자·랜턴의 크기가 인물 대비 상식적인가?
- [ ] 핫스팟을 얹어도 그림 분위기가 유지되는가? 모바일에서 터치 영역이 겹치지 않는가?
- [ ] 웃음 포인트(혼자 바쁜 아빠 / 빈 아빠 자리)가 글 없이 읽히는가?

## 파일

| 파일 | 내용 |
|---|---|
| `layout-guide.svg` / `.png` | 구도 가이드 (외곽선 없는 면 일러스트, 글자 없음). ① 생성 시 참고 이미지로 첨부 |
| `scene.js` | 장면·상품 데이터 (제목, 상품 5개, 핫스팟·클릭 영역 % 좌표, 임시 목적지) |
| `index.html` | 핫스팟 프로토타입 + 영역 편집기 |
| `tools/composite.py` | ③ 합성 + 핫스팟 좌표 재계산 (Python 3, Pillow) |
