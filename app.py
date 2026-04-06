import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw
import numpy as np
import io
import base64
import json
import re

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Unbounded:wght@700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── Base ── */
[data-testid="stAppViewContainer"] > .main {
    background: #0a0a0a;
}
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 0 2rem 3rem !important; max-width: 1440px !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Header ── */
.rv-header {
    background: rgba(20,20,20,0.95);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255,255,255,0.07);
    padding: 0 2rem;
    margin: 0 -2rem 2rem -2rem;
    height: 68px;
    display: flex;
    align-items: center;
    gap: 1rem;
    position: sticky;
    top: 0;
    z-index: 100;
}
.rv-logo {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, #f4672a 0%, #e04a0f 100%);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem; font-weight: 900; color: white;
    letter-spacing: -1px; flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(244,103,42,0.35);
}
.rv-brand { display: flex; flex-direction: column; }
.rv-name {
    font-family: 'Unbounded', sans-serif;
    font-size: 1.05rem; font-weight: 700;
    color: #e8e8e8; letter-spacing: -0.3px; line-height: 1.15;
}
.rv-name span { color: #f4672a; }
.rv-tagline { font-size: 0.7rem; color: #555; margin-top: 2px; }
.rv-badge {
    font-size: 0.65rem; font-weight: 700;
    color: #f4672a;
    background: rgba(244,103,42,0.12);
    padding: 4px 12px;
    border-radius: 100px;
    border: 1px solid rgba(244,103,42,0.35);
    letter-spacing: 0.5px;
    display: flex; align-items: center; gap: 5px;
}
.rv-badge::before {
    content: "";
    display: block; width: 6px; height: 6px;
    background: #f4672a; border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.6); opacity: 0.35; }
}
.rv-version {
    margin-left: auto;
    font-size: 0.65rem; color: #444;
    background: #141414;
    padding: 4px 12px; border-radius: 100px;
    border: 1px solid rgba(255,255,255,0.07);
}

/* ── Section titles ── */
.rv-card-title {
    font-size: 0.6rem; font-weight: 700; color: #888;
    text-transform: uppercase; letter-spacing: 1.5px;
    margin-bottom: 1rem; padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    display: flex; align-items: center; gap: 0.5rem;
}
.rv-card-title::before {
    content: "";
    display: block; width: 3px; height: 14px;
    background: linear-gradient(180deg, #f4672a 0%, #e04a0f 100%);
    border-radius: 2px;
}

/* ── Cards ── */
.rv-card {
    background: #141414;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.5rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.rv-card:hover {
    border-color: rgba(244,103,42,0.25);
    box-shadow: 0 8px 32px rgba(244,103,42,0.08);
}

/* ── Status badges ── */
.rv-status {
    display: inline-flex; align-items: center; gap: 7px;
    font-size: 0.75rem; font-weight: 600;
    padding: 5px 14px; border-radius: 100px;
    margin: 0.25rem 0 0.75rem;
}
.rv-status-ready  { background: rgba(52,211,153,0.08); color: #34d399; border: 1px solid rgba(52,211,153,0.25); }
.rv-status-nokey  { background: rgba(244,103,42,0.08); color: #f4672a; border: 1px solid rgba(244,103,42,0.25); }
.rv-status-error  { background: rgba(239,68,68,0.08);  color: #f87171; border: 1px solid rgba(239,68,68,0.25); }

/* ── Empty photo state ── */
.rv-empty {
    background: #111;
    border: 2px dashed rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 3.5rem 2rem;
    text-align: center;
    color: #555;
    margin-top: 0.5rem;
    transition: border-color 0.2s;
}
.rv-empty:hover { border-color: rgba(244,103,42,0.3); }
.rv-empty-icon { font-size: 2.5rem; margin-bottom: 0.75rem; opacity: 0.6; }
.rv-empty-text { font-size: 0.85rem; line-height: 1.7; color: #555; }

/* ── Analysis grid ── */
.rv-analysis-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 0.75rem;
}
.rv-analysis-card {
    background: #0f0f0f;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 1rem 1.25rem;
}
.rv-analysis-card h4 {
    font-size: 0.58rem; font-weight: 700; color: #f4672a;
    text-transform: uppercase; letter-spacing: 1.2px;
    margin: 0 0 0.75rem 0;
}
.rv-metric {
    display: flex; justify-content: space-between;
    font-size: 0.8rem; padding: 4px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.rv-metric:last-child { border-bottom: none; }
.rv-metric-key { color: #555; }
.rv-metric-val { color: #e8e8e8; font-weight: 600; }
.rv-surgical-note {
    background: rgba(244,103,42,0.07);
    border: 1px solid rgba(244,103,42,0.2);
    border-radius: 10px;
    padding: 0.875rem 1.25rem;
    margin-top: 0;
    font-size: 0.83rem; color: #ccc; line-height: 1.6;
    grid-column: 1 / -1;
}
.rv-surgical-note strong { color: #f4672a; }

/* ── Streamlit buttons ── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.2px !important;
    transition: all 0.2s !important;
}
[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #f4672a 0%, #e04a0f 100%) !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 4px 20px rgba(244,103,42,0.3) !important;
}
[data-testid="stBaseButton-primary"]:hover {
    opacity: 0.88 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(244,103,42,0.45) !important;
}
[data-testid="stBaseButton-secondary"] {
    background: transparent !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    color: #888 !important;
}
[data-testid="stBaseButton-secondary"]:hover {
    border-color: rgba(244,103,42,0.5) !important;
    color: #f4672a !important;
    background: rgba(244,103,42,0.06) !important;
}
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #f4672a 0%, #e04a0f 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 20px rgba(244,103,42,0.3) !important;
}
[data-testid="stDownloadButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-2px) !important;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input {
    border-radius: 8px !important;
    border-color: rgba(255,255,255,0.1) !important;
    background: #111 !important;
    color: #e8e8e8 !important;
    font-size: 0.88rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #f4672a !important;
    box-shadow: 0 0 0 3px rgba(244,103,42,0.15) !important;
}
[data-testid="stTextInput"] input::placeholder { color: #444 !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(244,103,42,0.25) !important;
    border-radius: 12px !important;
    background: rgba(244,103,42,0.04) !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(244,103,42,0.5) !important;
    background: rgba(244,103,42,0.07) !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] [role="slider"] {
    background: #f4672a !important;
    border-color: #f4672a !important;
    box-shadow: 0 0 0 4px rgba(244,103,42,0.2) !important;
}
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, #f4672a, #e04a0f) !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.07) !important;
    margin: 1.5rem 0 !important;
}

/* ── Select slider / radio ── */
[data-testid="stRadio"] label { color: #888 !important; font-size: 0.83rem !important; }
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p { font-size: 0.83rem !important; }

/* ── Labels ── */
label[data-testid="stWidgetLabel"] p { color: #888 !important; font-size: 0.8rem !important; }

/* ── Warning / Success ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 3px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #141414 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    color: #e8e8e8 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #f4672a; }

/* ── Disclaimer ── */
.rv-disclaimer {
    font-size: 0.67rem; color: #444; line-height: 1.8;
    text-align: center; padding: 1.25rem 3rem;
    background: #111;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
    margin-top: 2rem;
}
.rv-disclaimer strong { color: #666; }
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rv-header">
  <div class="rv-logo">RV</div>
  <div class="rv-brand">
    <div class="rv-name">RhinoVision <span>Pro</span></div>
    <div class="rv-tagline">Профессиональный симулятор ринопластики · AI-анализ + PIL деформация</div>
  </div>
  <div class="rv-badge">Gemini AI</div>
  <div class="rv-version">v4.1 · Secrets</div>
</div>
""", unsafe_allow_html=True)

# ─── Session state ─────────────────────────────────────────────────────────────
_DEFAULTS = {
    "orig": None, "orig_bytes": None, "result": None,
    "analysis": None, "rc": 0, "last_name": "",
    "patient_name": "", "annotations": [],
    "gen_error": None, "analysis_error": None,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Gemini key from Streamlit secrets ────────────────────────────────────────
try:
    _GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    _GEMINI_KEY = ""

# ─── Image utilities ──────────────────────────────────────────────────────────

def load_pil(uploaded_file):
    try:
        return Image.open(uploaded_file).convert("RGB")
    except Exception as exc:
        st.error(f"Ошибка загрузки изображения: {exc}")
        st.stop()


def fit(img, mx=768):
    w, h = img.size
    if max(w, h) <= mx:
        return img
    r = mx / max(w, h)
    return img.resize((int(w * r), int(h * r)), Image.LANCZOS)


def pil_to_bytes(img, quality=92):
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return buf.getvalue()


def pil_to_b64(img):
    return base64.b64encode(pil_to_bytes(img)).decode()


def apply_annotations(base_img, annotations):
    if not annotations:
        return base_img
    out  = base_img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    for ann in annotations:
        color = ann.get("color", "#f4672a")
        thick = ann.get("thick", 3)
        kind  = ann.get("kind",  "circle")
        cx    = int(w * ann["rx"])
        cy    = int(h * ann["ry"])
        r     = int(min(w, h) * 0.07)
        if kind == "circle":
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=thick)
        elif kind == "line":
            draw.line([cx-r, cy, cx+r, cy], fill=color, width=thick)
        elif kind == "arrow":
            draw.line([cx-r, cy, cx+r, cy], fill=color, width=thick)
            draw.polygon([cx+r, cy-6, cx+r, cy+6, cx+r+12, cy], fill=color)
    return out


def comparison_slider(before_img, after_img, height=420):
    b64b = pil_to_b64(before_img)
    b64a = pil_to_b64(after_img)
    html = f"""
<style>
.cmp-wrap {{
  position:relative;width:100%;max-width:800px;height:{height}px;
  overflow:hidden;border-radius:14px;
  border:1px solid rgba(255,255,255,0.07);
  user-select:none;cursor:col-resize;
  box-shadow:0 8px 40px rgba(0,0,0,0.6);
  background:#0a0a0a;
}}
.cmp-wrap img {{
  position:absolute;top:0;left:0;width:100%;height:100%;
  object-fit:cover;pointer-events:none;display:block;
}}
.cmp-after {{ clip-path:inset(0 0 0 50%); }}
.cmp-divider {{
  position:absolute;top:0;left:50%;width:2px;height:100%;
  background:linear-gradient(180deg,#f4672a,#e04a0f);
  box-shadow:0 0 12px rgba(244,103,42,0.6);
  pointer-events:none;
}}
.cmp-handle {{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:46px;height:46px;border-radius:50%;
  background:linear-gradient(135deg,#f4672a,#e04a0f);
  box-shadow:0 4px 20px rgba(244,103,42,0.5);
  display:flex;align-items:center;justify-content:center;
  font-size:1.1rem;color:white;pointer-events:none;
}}
.cmp-label {{
  position:absolute;top:14px;font-size:.62rem;font-weight:700;
  letter-spacing:1.2px;text-transform:uppercase;
  padding:4px 12px;border-radius:100px;pointer-events:none;
}}
.cmp-before-lbl {{ left:14px;background:rgba(0,0,0,0.6);color:#888;border:1px solid rgba(255,255,255,0.1); }}
.cmp-after-lbl  {{ right:14px;background:rgba(244,103,42,0.85);color:#fff; }}
</style>
<div class="cmp-wrap" id="cmp">
  <img src="data:image/jpeg;base64,{b64b}"/>
  <img class="cmp-after" src="data:image/jpeg;base64,{b64a}" id="cmpAfter"/>
  <div class="cmp-divider" id="cmpDiv"></div>
  <div class="cmp-handle" id="cmpHandle">&#8660;</div>
  <div class="cmp-label cmp-before-lbl">ДО</div>
  <div class="cmp-label cmp-after-lbl">ПОСЛЕ</div>
</div>
<script>
(function(){{
  var w=document.getElementById('cmp'),
      a=document.getElementById('cmpAfter'),
      d=document.getElementById('cmpDiv'),
      h=document.getElementById('cmpHandle'),
      drag=false;
  function pos(p){{
    p=Math.min(Math.max(p,2),98);
    a.style.clipPath='inset(0 0 0 '+p+'%)';
    d.style.left=p+'%'; h.style.left=p+'%';
  }}
  w.addEventListener('mousedown',function(){{drag=true;}});
  w.addEventListener('touchstart',function(){{drag=true;}},{{passive:true}});
  document.addEventListener('mouseup',function(){{drag=false;}});
  document.addEventListener('touchend',function(){{drag=false;}});
  document.addEventListener('mousemove',function(e){{
    if(!drag)return;
    var r=w.getBoundingClientRect();
    pos((e.clientX-r.left)/r.width*100);
  }});
  document.addEventListener('touchmove',function(e){{
    if(!drag)return;
    var r=w.getBoundingClientRect();
    pos((e.touches[0].clientX-r.left)/r.width*100);
  }},{{passive:true}});
}})();
</script>
"""
    components.html(html, height=height + 10, scrolling=False)

# ─── Nose warp (PIL + NumPy, no OpenCV) ───────────────────────────────────────

def warp_nose(img, params):
    arr = np.array(img, dtype=np.float32)
    h, w = arr.shape[:2]

    xx = np.tile(np.arange(w, dtype=np.float32), (h, 1))
    yy = np.tile(np.arange(h, dtype=np.float32).reshape(-1, 1), (1, w))

    cx, cy = w * 0.50, h * 0.43
    sx, sy = w * 0.15, h * 0.18

    def G(x0, y0, rx, ry):
        return np.exp(-((xx - x0)**2 / (2 * rx**2) +
                        (yy - y0)**2 / (2 * ry**2)))

    g_full    = G(cx, cy,           sx,       sy      )
    g_bridge  = G(cx, cy - sy*.75,  sx*.55,   sy*.50  )
    g_tip     = G(cx, cy + sy*.65,  sx*.50,   sy*.45  )
    g_nostril = G(cx, cy + sy*.95,  sx*.75,   sy*.30  )

    mx = xx.copy()
    my = yy.copy()

    my -= params["hump"] * 0.55 * g_bridge
    mx -= params["tip_proj"] * 0.50 * g_tip
    mx -= params["nose_width"] * 0.030 * (xx - cx) * g_full
    mx -= params["nostril_width"] * 0.042 * (xx - cx) * g_nostril

    if params["tip_angle"] != 0:
        angle  = np.radians(params["tip_angle"] * 0.70)
        tx = xx - cx
        ty = yy - (cy + sy * 0.65)
        mx -= (np.cos(angle)*tx - np.sin(angle)*ty - tx) * g_tip
        my -= (np.sin(angle)*tx + np.cos(angle)*ty - ty) * g_tip

    my -= params["nose_length"] * 0.030 * (yy - cy) * g_full

    mx = np.clip(mx, 0, w - 1)
    my = np.clip(my, 0, h - 1)

    x0 = np.floor(mx).astype(np.int32)
    y0 = np.floor(my).astype(np.int32)
    x1 = np.minimum(x0 + 1, w - 1)
    y1 = np.minimum(y0 + 1, h - 1)
    wx = (mx - x0)[..., np.newaxis]
    wy = (my - y0)[..., np.newaxis]

    out = (arr[y0, x0] * (1 - wx) * (1 - wy)
         + arr[y0, x1] *      wx  * (1 - wy)
         + arr[y1, x0] * (1 - wx) *      wy
         + arr[y1, x1] *      wx  *      wy).astype(np.uint8)

    return Image.fromarray(out)

# ─── Gemini face analysis ──────────────────────────────────────────────────────

_ANALYSIS_PROMPT = """You are a rhinoplasty planning assistant. Analyze this facial photograph and return ONLY a valid JSON object — no markdown, no extra text, no code fences.

Required structure:
{
  "nose": {
    "bridge_width": "narrow|medium|wide",
    "dorsal_hump": "absent|mild|moderate|severe",
    "tip_projection": "deprojected|average|projected",
    "nostril_width": "narrow|medium|wide",
    "nose_length": "short|average|long",
    "tip_rotation": "downward|neutral|upward",
    "skin_thickness": "thin|medium|thick",
    "tip_definition": "refined|average|bulbous",
    "symmetry": "symmetric|mild asymmetry|asymmetric"
  },
  "face": {
    "face_shape": "oval|round|square|heart|diamond",
    "skin_tone": "fair|light|medium|olive|tan|dark",
    "complexion": "clear|mild texture|combination",
    "estimated_age": "18-25|25-35|35-45|45+"
  },
  "photo": {
    "lighting_quality": "excellent|good|fair|poor",
    "lighting_direction": "frontal|lateral|overhead|mixed",
    "shadows": "minimal|moderate|harsh",
    "background": "neutral|complex|clinical",
    "framing": "optimal|suboptimal"
  },
  "surgical_notes": "One concise professional sentence about key rhinoplasty considerations."
}"""


def _parse_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def _gemini_error(err_str):
    e = err_str.lower()
    if "api_key_invalid" in e or ("invalid" in e and "key" in e):
        return "Неверный API ключ. Проверьте ключ на aistudio.google.com"
    if "quota" in e or "429" in e or "resource_exhausted" in e:
        return "Превышен лимит Gemini API. Подождите минуту и повторите."
    if "safety" in e or "block" in e:
        return "Запрос заблокирован фильтром безопасности. Попробуйте другое фото."
    if "permission" in e or "403" in e:
        return "Нет доступа к Gemini API. Проверьте ключ и регион."
    return f"Ошибка Gemini: {err_str[:200]}"


def analyze_face(api_key, img_bytes):
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                _ANALYSIS_PROMPT,
            ],
        )
        return _parse_json(response.text), None
    except json.JSONDecodeError:
        return None, "Gemini вернул невалидный JSON. Повторите запрос."
    except Exception as exc:
        return None, _gemini_error(str(exc))


def render_analysis(analysis):
    if not analysis:
        return
    nose  = analysis.get("nose", {})
    face  = analysis.get("face", {})
    photo = analysis.get("photo", {})
    notes = analysis.get("surgical_notes", "")

    def m(label, value):
        v = value or "—"
        return (f'<div class="rv-metric">'
                f'<span class="rv-metric-key">{label}</span>'
                f'<span class="rv-metric-val">{v}</span></div>')

    nose_html = (
        m("Ширина спинки",       nose.get("bridge_width"))
        + m("Горбинка",          nose.get("dorsal_hump"))
        + m("Проекция кончика",  nose.get("tip_projection"))
        + m("Ширина ноздрей",    nose.get("nostril_width"))
        + m("Длина носа",        nose.get("nose_length"))
        + m("Ротация кончика",   nose.get("tip_rotation"))
        + m("Толщина кожи",      nose.get("skin_thickness"))
        + m("Кончик носа",       nose.get("tip_definition"))
        + m("Симметрия",         nose.get("symmetry"))
    )
    env_html = (
        m("Форма лица",    face.get("face_shape"))
        + m("Тон кожи",    face.get("skin_tone"))
        + m("Кожа",        face.get("complexion"))
        + m("Возраст",     face.get("estimated_age"))
        + m("Освещение",   photo.get("lighting_quality"))
        + m("Тени",        photo.get("shadows"))
        + m("Кадрирование",photo.get("framing"))
    )
    note_html = (
        f'<div class="rv-surgical-note"><strong>Хирургические заметки:</strong> {notes}</div>'
        if notes else ""
    )
    st.markdown(f"""
<div class="rv-analysis-grid">
  <div class="rv-analysis-card"><h4>Параметры носа</h4>{nose_html}</div>
  <div class="rv-analysis-card"><h4>Лицо и условия фото</h4>{env_html}</div>
  {note_html}
</div>""", unsafe_allow_html=True)

# ─── Patient info bar ──────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
pi1, pi2, pi3 = st.columns([4, 3, 3])
with pi1:
    _pname = st.text_input("👤 Имя пациента",
                           value=st.session_state.patient_name,
                           placeholder="Введите имя пациента...",
                           key=f"pname_{st.session_state.rc}")
    st.session_state.patient_name = _pname
with pi2:
    st.text_input("📅 Дата консультации", placeholder="дд.мм.гггг",
                  key=f"pdate_{st.session_state.rc}")
with pi3:
    st.text_input("🏥 Врач", placeholder="ФИО хирурга",
                  key=f"pdoc_{st.session_state.rc}")

st.divider()

# ─── Main layout ───────────────────────────────────────────────────────────────
col_l, col_r = st.columns([4, 6], gap="large")

# ═══════════════════ LEFT — photo + annotation tools ═══════════════════════════
with col_l:
    st.markdown('<div class="rv-card-title">📸 Фото пациента</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Загрузить фото (JPG · PNG, до 200 МБ)",
        type=["jpg", "jpeg", "png"],
        key=f"up_{st.session_state.rc}",
    )

    if uploaded and uploaded.name != st.session_state.last_name:
        img = fit(load_pil(uploaded))
        st.session_state.orig         = img
        st.session_state.orig_bytes   = pil_to_bytes(img, quality=95)
        st.session_state.result       = None
        st.session_state.analysis     = None
        st.session_state.annotations  = []
        st.session_state.last_name    = uploaded.name
        st.session_state.gen_error    = None
        st.session_state.analysis_error = None

    if st.session_state.orig is None:
        st.markdown("""
<div class="rv-empty">
  <div class="rv-empty-icon">📷</div>
  <div class="rv-empty-text">Загрузите фото пациента<br>
    <span style="color:#444;font-size:.75rem">JPG · PNG · фронтальный вид</span>
  </div>
</div>""", unsafe_allow_html=True)
    else:
        st.image(apply_annotations(st.session_state.orig, st.session_state.annotations),
                 width=400)

        # Annotation toolbar
        st.markdown('<div class="rv-card-title" style="margin-top:.75rem">🖊 Разметка</div>',
                    unsafe_allow_html=True)
        tc1, tc2, tc3 = st.columns([3, 2, 2])
        with tc1:
            ann_kind = st.radio("Фигура", ["○ Круг", "╱ Линия", "→ Стрелка"],
                                horizontal=False, label_visibility="collapsed",
                                key=f"ann_kind_{st.session_state.rc}")
        with tc2:
            ann_color = st.color_picker("Цвет", "#f4672a",
                                        key=f"ann_color_{st.session_state.rc}")
            ann_thick = st.select_slider("Толщина", [1, 2, 3, 5, 8], value=3,
                                         key=f"ann_thick_{st.session_state.rc}")
        with tc3:
            ann_x = st.slider("X %", 10, 90, 50, key=f"ann_x_{st.session_state.rc}")
            ann_y = st.slider("Y %", 10, 90, 43, key=f"ann_y_{st.session_state.rc}")

        kind_map = {"○ Круг": "circle", "╱ Линия": "line", "→ Стрелка": "arrow"}
        ab1, ab2 = st.columns(2)
        with ab1:
            if st.button("➕ Добавить", use_container_width=True, key="btn_ann_add"):
                st.session_state.annotations.append({
                    "kind": kind_map[ann_kind], "color": ann_color,
                    "thick": ann_thick, "rx": ann_x / 100, "ry": ann_y / 100,
                })
                st.rerun()
        with ab2:
            if st.button("🗑 Очистить", use_container_width=True, key="btn_ann_clr"):
                st.session_state.annotations = []
                st.rerun()

# ═══════════════════ RIGHT — sliders + actions ════════════════════════════════
with col_r:

    if not _GEMINI_KEY:
        st.markdown('<div class="rv-status rv-status-nokey">⚠ API ключ не настроен — только PIL-деформация</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="rv-status rv-status-ready">✓ Gemini AI активен</div>',
                    unsafe_allow_html=True)

    # ── Rhinoplasty sliders ──
    st.markdown('<div class="rv-card-title">⚙️ Параметры ринопластики</div>', unsafe_allow_html=True)

    rc = st.session_state.rc
    _SLIDERS = [
        ("hump",          "Высота горбинки (горб спинки)",  -50, 50, 0),
        ("tip_proj",      "Проекция кончика носа",          -50, 50, 0),
        ("nose_width",    "Ширина носа",                    -50, 50, 0),
        ("nostril_width", "Ширина ноздрей",                 -50, 50, 0),
        ("tip_angle",     "Угол наклона кончика",           -30, 30, 0),
        ("nose_length",   "Длина носа",                     -50, 50, 0),
    ]
    params = {}
    for skey, label, lo, hi, dflt in _SLIDERS:
        params[skey] = st.slider(label, lo, hi, dflt, key=f"{skey}_{rc}")

    st.divider()

    # ── Action buttons ──
    btn1, btn2 = st.columns(2)
    with btn1:
        do_gen = st.button("✨ Симулировать + Анализ", type="primary",
                           use_container_width=True, key="btn_gen")
    with btn2:
        do_rst = st.button("🔄 Сбросить всё", use_container_width=True, key="btn_rst")

    # ── Generate handler ──
    if do_gen:
        if st.session_state.orig is None:
            st.warning("Сначала загрузите фото пациента.")
        else:
            with st.spinner("🔧 Деформация носа (PIL + NumPy)…"):
                warped = warp_nose(st.session_state.orig, params)
                warped = apply_annotations(warped, st.session_state.annotations)
                st.session_state.result = warped
                st.session_state.gen_error = None

            if _GEMINI_KEY:
                with st.spinner("🔬 Gemini AI анализ лица…"):
                    analysis, aerr = analyze_face(
                        _GEMINI_KEY,
                        st.session_state.orig_bytes,
                    )
                if aerr:
                    st.error(f"Анализ: {aerr}")
                    st.session_state.analysis_error = aerr
                else:
                    st.session_state.analysis = analysis
                    st.session_state.analysis_error = None
                    st.success("✅ Готово!")
            else:
                st.success("✅ Деформация применена!")

    # ── Reset handler ──
    if do_rst:
        for k, v in _DEFAULTS.items():
            st.session_state[k] = v
        st.session_state.rc = st.session_state.get("rc", 0) + 1
        st.rerun()

    # ── Download ──
    if st.session_state.result is not None:
        st.divider()
        fname = (st.session_state.patient_name.strip().replace(" ", "_") or "patient")
        st.download_button(
            "💾 Сохранить результат (JPG)",
            data=pil_to_bytes(st.session_state.result),
            file_name=f"rhinovision_{fname}.jpg",
            mime="image/jpeg",
            use_container_width=True,
            key="btn_dl",
        )

# ─── Before / After drag comparison ───────────────────────────────────────────
if st.session_state.orig is not None and st.session_state.result is not None:
    st.divider()
    st.markdown('<div class="rv-card-title">⚖️ Сравнение До / После — перетащите разделитель</div>',
                unsafe_allow_html=True)
    iw, ih = st.session_state.orig.size
    disp_h  = min(int(ih * 780 / iw), 560)
    comparison_slider(st.session_state.orig, st.session_state.result, height=disp_h)

# ─── Gemini analysis panel ─────────────────────────────────────────────────────
if st.session_state.analysis is not None:
    st.divider()
    with st.expander("🔬 AI Анализ лица (Gemini)", expanded=True):
        render_analysis(st.session_state.analysis)

# ─── Medical disclaimer ────────────────────────────────────────────────────────
st.markdown("""
<div class="rv-disclaimer">
  <strong>⚕️ Медицинский дисклеймер.</strong>
  RhinoVision Pro предназначен исключительно для иллюстративных целей и не является медицинским прогнозом.
  Результаты симуляции не гарантируют результатов хирургического вмешательства.
  AI-анализ носит справочный характер. Все клинические решения принимаются квалифицированным хирургом.<br>
  <span style="color:#333">© 2025 RhinoVision Pro &nbsp;·&nbsp; Только для медицинского персонала &nbsp;·&nbsp; v4.1 PIL+NumPy+Gemini</span>
</div>
""", unsafe_allow_html=True)
