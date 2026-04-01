import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw
import cv2
import numpy as np
import io
import base64

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RhinoVision Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
}
[data-testid="stAppViewContainer"] > .main { background: #ffffff; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 0 2rem 2rem !important; max-width: 1440px !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Header ── */
.rv-header {
    background: #1a2b4a;
    padding: 0 2rem;
    margin: 0 -2rem 0 -2rem;
    height: 64px;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.rv-logo {
    width: 38px; height: 38px;
    background: #0066cc;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem; font-weight: 900; color: white;
    letter-spacing: -1px; flex-shrink: 0;
}
.rv-brand { display: flex; flex-direction: column; }
.rv-name {
    font-size: 1.15rem; font-weight: 800;
    color: #ffffff; letter-spacing: -0.3px; line-height: 1.1;
}
.rv-name span { color: #60a5fa; }
.rv-tagline { font-size: 0.72rem; color: #94a3b8; margin-top: 1px; }
.rv-version {
    margin-left: auto;
    font-size: 0.65rem; color: #64748b;
    background: #243350; padding: 3px 10px; border-radius: 20px;
}

/* ── Panel card ── */
.rv-card {
    background: #ffffff;
    border: 1px solid #e8edf2;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.rv-card-title {
    font-size: 0.65rem; font-weight: 700;
    color: #1a2b4a; text-transform: uppercase;
    letter-spacing: 1.3px; margin-bottom: 0.9rem;
    padding-bottom: 0.5rem; border-bottom: 2px solid #e8edf2;
    display: flex; align-items: center; gap: 0.4rem;
}
.rv-card-title::before {
    content: "";
    display: block; width: 3px; height: 13px;
    background: #0066cc; border-radius: 2px;
}

/* ── Patient info bar ── */
.rv-patient-bar {
    background: #f8fafc;
    border: 1px solid #e8edf2;
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    margin: 1rem 0;
    display: flex; align-items: center; gap: 0.5rem;
}

/* ── Empty photo state ── */
.rv-empty {
    background: #f8fafc;
    border: 2px dashed #cbd5e1;
    border-radius: 12px;
    padding: 3rem 2rem; text-align: center;
    color: #64748b; margin-top: 0.5rem;
}
.rv-empty-icon { font-size: 2.2rem; margin-bottom: 0.5rem; }
.rv-empty-text { font-size: 0.82rem; line-height: 1.6; }

/* ── Slider groups ── */
.rv-slider-group { margin-bottom: 0.25rem; }
.rv-slider-label {
    font-size: 0.75rem; font-weight: 500;
    color: #374151; margin-bottom: -0.6rem;
    display: flex; justify-content: space-between;
}
.rv-slider-val { color: #0066cc; font-weight: 700; font-size: 0.75rem; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important; font-size: 0.85rem !important;
    transition: all 0.15s ease !important;
}
[data-testid="stBaseButton-primary"] {
    background: #0066cc !important; border: none !important;
}
[data-testid="stBaseButton-primary"]:hover {
    background: #0052a3 !important;
    box-shadow: 0 4px 14px rgba(0,102,204,0.35) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stDownloadButton"] > button {
    background: #16a34a !important; color: white !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important;
}

/* ── Streamlit input overrides ── */
[data-testid="stTextInput"] input {
    border-radius: 8px !important; border-color: #cbd5e1 !important;
    font-size: 0.88rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #0066cc !important;
    box-shadow: 0 0 0 3px rgba(0,102,204,0.15) !important;
}
[data-testid="stFileUploader"] {
    border: 2px dashed #bfdbfe !important;
    border-radius: 10px !important;
    background: #eff6ff !important;
}
[data-testid="stSlider"] [role="slider"] {
    background: #0066cc !important; border-color: #0066cc !important;
}

/* ── Disclaimer ── */
.rv-disclaimer {
    font-size: 0.66rem; color: #94a3b8; line-height: 1.7;
    text-align: center; padding: 1rem 3rem;
    background: #f8fafc; border-radius: 10px;
    border-top: 2px solid #e8edf2; margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rv-header">
  <div class="rv-logo">RV</div>
  <div class="rv-brand">
    <div class="rv-name">RhinoVision <span>Pro</span></div>
    <div class="rv-tagline">Профессиональный симулятор ринопластики для пластических хирургов</div>
  </div>
  <div class="rv-version">v2.0 · MVP</div>
</div>
""", unsafe_allow_html=True)

# ─── Session state ────────────────────────────────────────────────────────────
for k, v in {
    "orig": None, "result": None,
    "rc": 0, "last_name": "",
    "annotations": [], "patient_name": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_pil(f):
    if f.name.lower().endswith(".heic"):
        st.error("HEIC формат не поддерживается. Пожалуйста, конвертируйте фото в JPG или PNG.")
        st.stop()
    return Image.open(f).convert("RGB")


def fit(img, mx=500):
    w, h = img.size
    if max(w, h) <= mx:
        return img
    r = mx / max(w, h)
    return img.resize((int(w * r), int(h * r)), Image.LANCZOS)


def transform(img, p):
    """
    Gaussian displacement-field rhinoplasty simulation.
    Multipliers tuned for clearly visible results at ±30 slider units.
    """
    arr = np.array(img, dtype=np.uint8)
    h, w = arr.shape[:2]

    xx = np.tile(np.arange(w, dtype=np.float32), (h, 1))
    yy = np.tile(np.arange(h, dtype=np.float32).reshape(-1, 1), (1, w))
    mx, my = xx.copy(), yy.copy()

    cx, cy = w * 0.50, h * 0.43
    sx, sy = w * 0.15, h * 0.18

    def G(x0, y0, rx, ry):
        return np.exp(-((xx - x0) ** 2 / (2 * rx ** 2) +
                        (yy - y0) ** 2 / (2 * ry ** 2)))

    g_full    = G(cx, cy,          sx,      sy     )
    g_bridge  = G(cx, cy - sy*.75, sx*.55,  sy*.50 )
    g_tip     = G(cx, cy + sy*.65, sx*.50,  sy*.45 )
    g_nostril = G(cx, cy + sy*.95, sx*.75,  sy*.30 )

    # Multipliers 2× stronger than before for visible results
    my -= p["hump"]          * 0.55 * g_bridge
    mx -= p["tip_proj"]      * 0.50 * g_tip
    mx -= p["nose_width"]    * 0.030 * (xx - cx) * g_full
    mx -= p["nostril_width"] * 0.042 * (xx - cx) * g_nostril

    if p["tip_angle"] != 0:
        a  = np.radians(p["tip_angle"] * 0.70)
        tx = xx - cx
        ty = yy - (cy + sy * 0.65)
        mx -= (np.cos(a) * tx - np.sin(a) * ty - tx) * g_tip
        my -= (np.sin(a) * tx + np.cos(a) * ty - ty) * g_tip

    my -= p["nose_length"] * 0.030 * (yy - cy) * g_full

    mx = np.clip(mx, 0, w - 1).astype(np.float32)
    my = np.clip(my, 0, h - 1).astype(np.float32)
    out = cv2.remap(arr, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return Image.fromarray(out)


def apply_annotations(base_img, annotations):
    if not annotations:
        return base_img
    out  = base_img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    for ann in annotations:
        color = ann.get("color", "#FF3333")
        thick = ann.get("thick", 3)
        kind  = ann.get("kind", "circle")
        cx, cy = int(w * ann["rx"]), int(h * ann["ry"])
        r = int(min(w, h) * 0.07)
        if kind == "circle":
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=thick)
        elif kind == "arrow":
            draw.line([cx - r, cy, cx + r, cy], fill=color, width=thick)
            draw.polygon([cx+r, cy-6, cx+r, cy+6, cx+r+12, cy], fill=color)
        elif kind == "line":
            draw.line([cx - r, cy, cx + r, cy], fill=color, width=thick)
    return out


def pil_to_b64(img, fmt="JPEG"):
    buf = io.BytesIO()
    img.save(buf, format=fmt, quality=92)
    return base64.b64encode(buf.getvalue()).decode()


def to_jpg_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def comparison_slider(before_img, after_img, height=420):
    """Render a drag-to-compare before/after slider via HTML/JS."""
    b64_before = pil_to_b64(before_img)
    b64_after  = pil_to_b64(after_img)
    html = f"""
<style>
  .cmp-wrap {{
    position: relative; width: 100%; max-width: 780px;
    height: {height}px; overflow: hidden;
    border-radius: 12px; border: 1px solid #e8edf2;
    user-select: none; cursor: col-resize;
    box-shadow: 0 4px 16px rgba(0,0,0,0.10);
  }}
  .cmp-wrap img {{
    position: absolute; top: 0; left: 0;
    width: 100%; height: 100%; object-fit: cover;
    pointer-events: none; display: block;
  }}
  .cmp-after  {{ clip-path: inset(0 0 0 50%); }}
  .cmp-divider {{
    position: absolute; top: 0; left: 50%; width: 2px;
    height: 100%; background: #ffffff;
    box-shadow: 0 0 6px rgba(0,0,0,0.4);
    pointer-events: none;
  }}
  .cmp-handle {{
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 44px; height: 44px; border-radius: 50%;
    background: #ffffff; box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; pointer-events: none;
  }}
  .cmp-label {{
    position: absolute; top: 12px;
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 1px; text-transform: uppercase;
    padding: 3px 10px; border-radius: 20px;
    pointer-events: none;
  }}
  .cmp-label-before {{
    left: 12px; background: rgba(0,0,0,0.45); color: #e5e7eb;
  }}
  .cmp-label-after {{
    right: 12px; background: rgba(0,102,204,0.75); color: #ffffff;
  }}
</style>
<div class="cmp-wrap" id="cmp">
  <img class="cmp-before" src="data:image/jpeg;base64,{b64_before}" />
  <img class="cmp-after"  src="data:image/jpeg;base64,{b64_after}"  id="cmpAfter" />
  <div class="cmp-divider" id="cmpDiv"></div>
  <div class="cmp-handle"  id="cmpHandle">⇔</div>
  <div class="cmp-label cmp-label-before">ДО</div>
  <div class="cmp-label cmp-label-after">ПОСЛЕ</div>
</div>
<script>
(function() {{
  const wrap   = document.getElementById('cmp');
  const after  = document.getElementById('cmpAfter');
  const divider= document.getElementById('cmpDiv');
  const handle = document.getElementById('cmpHandle');
  let dragging = false;

  function setPos(pct) {{
    pct = Math.min(Math.max(pct, 2), 98);
    after.style.clipPath  = 'inset(0 0 0 ' + pct + '%)';
    divider.style.left    = pct + '%';
    handle.style.left     = pct + '%';
  }}

  wrap.addEventListener('mousedown',  () => dragging = true);
  wrap.addEventListener('touchstart', () => dragging = true, {{passive: true}});
  document.addEventListener('mouseup',   () => dragging = false);
  document.addEventListener('touchend',  () => dragging = false);

  document.addEventListener('mousemove', e => {{
    if (!dragging) return;
    const r = wrap.getBoundingClientRect();
    setPos((e.clientX - r.left) / r.width * 100);
  }});
  document.addEventListener('touchmove', e => {{
    if (!dragging) return;
    const r = wrap.getBoundingClientRect();
    setPos((e.touches[0].clientX - r.left) / r.width * 100);
  }}, {{passive: true}});
}})();
</script>
"""
    components.html(html, height=height + 10, scrolling=False)


# ─── Patient info bar ─────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
pi1, pi2, pi3 = st.columns([4, 3, 3])
with pi1:
    patient_name = st.text_input(
        "👤 Имя пациента",
        value=st.session_state.patient_name,
        placeholder="Введите имя пациента...",
        key=f"pname_{st.session_state.rc}",
    )
    st.session_state.patient_name = patient_name
with pi2:
    st.text_input("📅 Дата консультации", value="", placeholder="дд.мм.гггг", key=f"pdate_{st.session_state.rc}")
with pi3:
    st.text_input("🏥 Врач", value="", placeholder="ФИО хирурга", key=f"pdoc_{st.session_state.rc}")

st.divider()

# ─── Main two-column layout ───────────────────────────────────────────────────
col_l, col_r = st.columns([4, 6], gap="large")

# ══════════════════════════════════════════════════════════════════════════════
# LEFT – photo + annotation tools
# ══════════════════════════════════════════════════════════════════════════════
with col_l:
    st.markdown('<div class="rv-card-title">📸 Фото пациента</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Загрузить фото (JPG · PNG · HEIC)",
        type=["jpg", "jpeg", "png"],
        key=f"up_{st.session_state.rc}",
    )

    if uploaded and uploaded.name != st.session_state.last_name:
        st.session_state.orig        = fit(load_pil(uploaded))
        st.session_state.result      = None
        st.session_state.annotations = []
        st.session_state.last_name   = uploaded.name

    if st.session_state.orig is None:
        st.markdown("""
        <div class="rv-empty">
          <div class="rv-empty-icon">📷</div>
          <div class="rv-empty-text">
            Загрузите фото пациента<br>
            <span style="color:#94a3b8;font-size:0.75rem">JPG · PNG · HEIC · до 500 px</span>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        display_img = apply_annotations(st.session_state.orig, st.session_state.annotations)
        st.image(display_img, width=400)

        # ── Annotation toolbar ──
        st.markdown('<div class="rv-card-title" style="margin-top:0.75rem">🖊 Инструменты разметки</div>',
                    unsafe_allow_html=True)
        tc1, tc2, tc3 = st.columns([3, 2, 2])
        with tc1:
            ann_kind = st.radio(
                "Фигура", ["○ Круг", "╱ Линия", "→ Стрелка"],
                horizontal=False, label_visibility="collapsed",
                key=f"ann_kind_{st.session_state.rc}",
            )
        with tc2:
            ann_color = st.color_picker("Цвет", "#FF3333",
                                        key=f"ann_color_{st.session_state.rc}")
            ann_thick = st.select_slider("Толщина", [1,2,3,5,8], value=3,
                                         key=f"ann_thick_{st.session_state.rc}")
        with tc3:
            ann_x = st.slider("X %", 10, 90, 50, key=f"ann_x_{st.session_state.rc}")
            ann_y = st.slider("Y %", 10, 90, 43, key=f"ann_y_{st.session_state.rc}")

        kind_map = {"○ Круг": "circle", "╱ Линия": "line", "→ Стрелка": "arrow"}
        ab1, ab2 = st.columns(2)
        with ab1:
            if st.button("➕ Добавить", use_container_width=True, key="btn_add_ann"):
                st.session_state.annotations.append({
                    "kind":  kind_map[ann_kind],
                    "color": ann_color, "thick": ann_thick,
                    "rx": ann_x / 100, "ry": ann_y / 100,
                })
                st.rerun()
        with ab2:
            if st.button("🗑 Очистить", use_container_width=True, key="btn_clr_ann"):
                st.session_state.annotations = []
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT – parameters + actions
# ══════════════════════════════════════════════════════════════════════════════
with col_r:
    st.markdown('<div class="rv-card-title">⚙️ Параметры ринопластики</div>', unsafe_allow_html=True)

    rc = st.session_state.rc
    slider_defs = [
        ("hump",          "Высота горбинки (горб спинки)",   -50, 50, 0),
        ("tip_proj",      "Проекция кончика носа",           -50, 50, 0),
        ("nose_width",    "Ширина носа",                     -50, 50, 0),
        ("nostril_width", "Ширина ноздрей",                  -50, 50, 0),
        ("tip_angle",     "Угол наклона кончика",            -30, 30, 0),
        ("nose_length",   "Длина носа",                      -50, 50, 0),
    ]

    params = {}
    for key, label, lo, hi, default in slider_defs:
        val = st.slider(label, lo, hi, default, key=f"{key}_{rc}")
        params[key] = val

    st.divider()

    btn1, btn2 = st.columns(2)
    with btn1:
        gen = st.button("✨ Сгенерировать результат", type="primary",
                        use_container_width=True, key="btn_gen")
    with btn2:
        rst = st.button("🔄 Сбросить всё", use_container_width=True, key="btn_rst")

    if gen:
        if st.session_state.orig is None:
            st.warning("Сначала загрузите фото пациента.")
        else:
            with st.spinner("Применяем изменения…"):
                res = transform(st.session_state.orig, params)
                res = apply_annotations(res, st.session_state.annotations)
                st.session_state.result = res
            st.success("Готово!", icon="✅")

    if rst:
        for k in ["orig", "result", "annotations"]:
            st.session_state[k] = None if k != "annotations" else []
        st.session_state.last_name = ""
        st.session_state.rc += 1
        st.rerun()

    if st.session_state.result is not None:
        st.divider()
        fname = (st.session_state.patient_name.strip().replace(" ", "_") or "patient")
        st.download_button(
            "💾 Сохранить результат (JPG)",
            data=to_jpg_bytes(st.session_state.result),
            file_name=f"rhinovision_{fname}.jpg",
            mime="image/jpeg",
            use_container_width=True,
            key="btn_dl",
        )

# ─── Before / After drag-slider comparison ────────────────────────────────────
if st.session_state.orig is not None and st.session_state.result is not None:
    st.divider()
    st.markdown('<div class="rv-card-title">⚖️ Сравнение До / После — перетащите разделитель</div>',
                unsafe_allow_html=True)

    # Calculate display height proportional to image
    iw, ih = st.session_state.orig.size
    display_h = min(int(ih * 780 / iw), 560)
    comparison_slider(st.session_state.orig, st.session_state.result, height=display_h)

# ─── Disclaimer ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="rv-disclaimer">
  <strong>⚕️ Медицинский дисклеймер.</strong>
  RhinoVision Pro предназначен исключительно для иллюстративных целей и не является
  медицинским прогнозом. Результаты симуляции не гарантируют результатов хирургического
  вмешательства. Все клинические решения принимаются квалифицированным хирургом на основании
  индивидуальной консультации. Симуляция не заменяет профессиональную медицинскую оценку.<br>
  <span style="color:#cbd5e1">© 2025 RhinoVision Pro &nbsp;·&nbsp; Только для медицинского персонала</span>
</div>
""", unsafe_allow_html=True)
